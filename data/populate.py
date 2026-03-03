import csv
import time
from typing import Iterable
from urllib.parse import urljoin

from data.scraper import scrape_imslp_metadata
from data.adding_downloads import process_downloads

FIELDNAMES = [
    "Title",
    "Composer",
    "Permlink",
    "Instrumentation",
    "Key",
    "Piece Style",
    "First Performance",
    "Year/Date of Composition",
    "Composer Time Period",
    "Average Duration",
    "num_downloads",
]


def _normalize_url(permlink: str) -> str:
    if not permlink:
        return ""
    permlink = permlink.strip()
    if permlink.startswith("http"):
        return permlink
    # common permlink shapes: '/wiki/Title' or 'wiki/Title' or 'Title'
    if permlink.startswith("/"):
        return urljoin("https://imslp.org", permlink)
    if permlink.startswith("wiki/"):
        return urljoin("https://imslp.org/", permlink)
    # fallback: assume wiki path
    return urljoin("https://imslp.org/wiki/", permlink)


def file_scrape(work: dict) -> dict:
    row = {}

    row["Title"] = work.get("intvals", {}).get("worktitle")
    row["Composer"] = work.get("intvals", {}).get("composer")
    row["Permlink"] = work.get("permlink")

    # Normalize to a full URL for downstream scrapers
    url = _normalize_url(row["Permlink"]) if row["Permlink"] else ""

    try:
        additional_info = scrape_imslp_metadata(url) if url else {}

        row["Instrumentation"] = additional_info.get("Instrumentation")
        row["Key"] = additional_info.get("Key")
        row["Piece Style"] = additional_info.get("Piece Style")
        row["First Performance"] = additional_info.get("First Performance")
        row["Year/Date of Composition"] = additional_info.get("Year/Date of Composition")
        row["Composer Time Period"] = additional_info.get("Composer Time Period")
        row["Average Duration"] = additional_info.get("Average Duration")

    except Exception as e:
        row["Instrumentation"] = None
        row["Key"] = None
        row["Piece Style"] = None
        row["First Performance"] = None
        row["Year/Date of Composition"] = None
        row["Composer Time Period"] = None
        row["Average Duration"] = None

    # set Permlink to the normalized URL so process_downloads can fetch it
    row["Permlink"] = url

    try:
        row = process_downloads(row)
    except Exception:
        row["num_downloads"] = 0

    return row


def populate_csv(works: Iterable[dict], output_path: str):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        # ignore any unexpected keys such as stray "Year" column
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()

        for idx, work in enumerate(works, 1):
            try:
                row = file_scrape(work)
                # drop any accidental "Year" key that slipped in during scraping
                if "Year" in row:
                    row.pop("Year")
                writer.writerow(row)
                print(f"[{idx}] Wrote: {row.get('Title')}")
            except Exception as e:
                print(f"[{idx}] Failed row: {e}")

            # rate limiting safety
            time.sleep(0.01)


if __name__ == "__main__":
    print("This module provides populate_csv(works, output_path)")
