import requests
from bs4 import BeautifulSoup

TARGET_KEYS = {
    "Instrumentation",
    "Key",
    "Piece Style",
    "First Performance",
    "Year/Date of Composition",
    "Composer Time Period",
    "Average Duration"
}

def scrape_imslp_metadata(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    for row in soup.select("table tr"):
        th = row.find("th")
        td = row.find("td")

        if not th or not td:
            continue

        # 🔑 STRATEGY 1: Look for the specific 'Main Header' class (mh555)
        # This ensures we get "Average Duration" and ignore "Avg. Duration"
        main_label = th.find("span", class_="mh555")
        
        if main_label:
            key = main_label.get_text(strip=True)
        else:
            # 🔑 STRATEGY 2: Fallback for rows without spans (e.g., "Instrumentation")
            # We use stripped_strings to handle any bold/italic tags inside the header
            key = " ".join(th.stripped_strings).strip()

        # Clean up the key (remove trailing colons if any, e.g. "Key:")
        key = key.rstrip(":")

        if key in TARGET_KEYS:
            # For the value, using get_text with a separator ensures lines don't mash together
            data[key] = td.get_text(" ", strip=True)

    return data

import re
from bs4 import BeautifulSoup
import requests

STAR_MAP = {
    "zero-stars": 0,
    "one-star": 1,
    "two-stars": 2,
    "three-stars": 3,
    "four-stars": 4,
    "five-stars": 5,
}

import re
from bs4 import BeautifulSoup
import requests

def scrape_score_blocks(imslp_url):
    # Added a User-Agent to look like a real browser (IMSLP blocks default python requests sometimes)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(imslp_url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = 0

    blocks = soup.select("div.we_file_download.plainlinks")
    
    # DEBUG: Print how many blocks found to ensure basic selection works
    print(f"Found {len(blocks)} blocks.")

    for block in blocks:
        
        # ... inside the loop
        
        # Stop after one block to inspect

        

        # ⬇️ DOWNLOADS (Your existing code was mostly fine, just added safety)
        downloads_span = block.select_one("span[title^='Total number of downloads']")
        if downloads_span and ":" in downloads_span.get("title", ""):
            try:
                results = results + int(downloads_span["title"].split(":")[1].strip())
            except ValueError:
                pass

        
        
    return results
# ------------------ TEST ------------------

if __name__ == "__main__":
    url = "https://imslp.org/wiki/Romeo_and_Juliet_(overture-fantasia),_TH_42_(Tchaikovsky,_Pyotr)"
    scores = scrape_score_blocks(url)
    print(scores)
    


#test
if __name__ == "__main__":
    row = scrape_imslp_metadata('https://imslp.org/wiki/Amicizia_(Stankovych,_Tatiana)')
    print(row)