import csv
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import os
import time
import random

# ==========================================
# 1. YOUR SCRAPER FUNCTION
# ==========================================
def scrape_score_blocks(imslp_url):
    try:
        # Randomize User-Agent slightly to look less like a bot
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(imslp_url, headers=headers, timeout=10)
        
        # If we get a "Too Many Requests" error (429), wait and retry once
        if response.status_code == 429:
            time.sleep(5)
            response = requests.get(imslp_url, headers=headers, timeout=10)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        total_downloads = 0
        blocks = soup.select("div.we_file_download")
        
        for block in blocks:
            downloads_span = block.select_one("span[title^='Total number of downloads']")
            if downloads_span:
                try:
                    count = int(downloads_span["title"].split(":")[1].strip())
                    total_downloads += count
                except (ValueError, IndexError):
                    continue
        return total_downloads

    except Exception:
        return 0

# ==========================================
# 2. THE RESUMABLE CSV LOGIC
# ==========================================

def process_row(row):
    """Worker function for threading"""
    try:
        url = row.get('Permlink', '')
        if url:
            # Add a tiny random sleep to prevent getting banned
            time.sleep(random.uniform(0.1, 0.5))
            row['num_downloads'] = scrape_score_blocks(url)
        else:
            row['num_downloads'] = 0
    except:
        row['num_downloads'] = 0
    return row

def main():
    input_filename = 'processed.csv'
    output_filename = 'processed-40k.csv'
    
    # ⚠️ LOWER CONCURRENCY: 40k requests is a lot. 
    # High concurrency (10+) causes IMSLP to ban you around row 700.
    # We lower this to 5 to be safer.
    MAX_WORKERS = 5

    # 1. Check if we need to Resume
    rows_done = 0
    mode = 'w'
    write_header = True
    
    if os.path.exists(output_filename):
        with open(output_filename, 'r', encoding='utf-8') as f:
            rows_done = sum(1 for _ in f) - 1 # Subtract header
        if rows_done > 0:
            print(f"Found existing file with {rows_done} rows. Resuming...")
            mode = 'a' # Append mode
            write_header = False

    # 2. Read Input Data
    with open(input_filename, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if 'num_downloads' not in fieldnames:
            fieldnames.append('num_downloads')
        
        # Convert to list and SLICE to skip already done rows
        all_rows = list(reader)
        rows_to_process = all_rows[rows_done:]

    if not rows_to_process:
        print(" All rows are already processed!")
        return

    print(f" Starting scrape for {len(rows_to_process)} remaining rows...")

    # 3. Open Output File and Process
    # We open the file ONCE and keep it open to append lines as they finish
    with open(output_filename, mode=mode, encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit tasks
            future_to_row = {executor.submit(process_row, row): row for row in rows_to_process}
            
            completed = 0
            total = len(rows_to_process)
            
            for future in concurrent.futures.as_completed(future_to_row):
                result_row = future.result()
                
                # WRITE IMMEDIATELY - If script crashes, you only lose 1 row
                writer.writerow(result_row)
                # Flush ensures it's actually written to disk, not just memory buffer
                outfile.flush() 

                completed += 1
                if completed % 50 == 0:
                    print(f"Progress: {completed}/{total} (Total saved: {rows_done + completed})")

    print("Done!")

if __name__ == "__main__":
    main()