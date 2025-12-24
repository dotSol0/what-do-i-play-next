import inspect
import imslp # Replace 'my_package' with the name of the package you want to inspect
import sys
sys.path.append("..")  # or project root

from scraper import scrape_imslp_metadata


from imslp.interfaces import internal

works = internal.list_works(count=10)


import csv
def file_scrape(work):
    row = {}

    row["Title"] = work.get("intvals", {}).get("worktitle")
    row["Composer"] = work.get("intvals", {}).get("composer")
    row["Permlink"] = work.get("permlink")

    try:
        additional_info = scrape_imslp_metadata(row["Permlink"])

        row["Instrumentation"] = additional_info.get("Instrumentation")
        row["Key"] = additional_info.get("Key")
        row["Piece Style"] = additional_info.get("Piece Style")
        row["First Performance"] = additional_info.get("First Performance")
        row["Year/Date of Composition"] = additional_info.get("Year/Date of Composition")
        row["Composer Time Period"] = additional_info.get("Composer Time Period")
        row["Average Duration"] = additional_info.get("Average Duration")

    except Exception as e:
        print(f"Scrape failed for {row['Permlink']}: {e}")

        row["Instrumentation"] = None
        row["Key"] = None
        row["Piece Style"] = None
        row["First Performance"] = None
        row["Year/Date of Composition"] = None
        row["Composer Time Period"] = None
        row["Average Duration"] = None
    return row


i = 0
while (i < 9):
    work = works[i]
    row = file_scrape(work)
    print(row)
    i += 1
