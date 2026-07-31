#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so `from data...` works when running
# this script as `python scripts/run_api_call.py` (sys.path[0] is `scripts/`).
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.imslp_fetch import fetch_works
from data.populate import populate_csv


def main():
    parser = argparse.ArgumentParser(description="Fetch IMSLP works and populate CSV")
    parser.add_argument("--start", type=int, default=int(os.getenv("START", "0")), help="Start offset for fetching works")
    parser.add_argument("--count", type=int, default=int(os.getenv("COUNT", "156000")), help="Number of works to fetch")
    parser.add_argument("--output", type=str, default=os.getenv("OUTPUT_PATH", "data/processed/raw-full.csv"), help="CSV output path")
    parser.add_argument("--batch", type=int, default=5000, help="Batch size per IMSLP request")
    parser.add_argument("--append", action="store_true", help="Append to output CSV instead of overwriting it")
    args = parser.parse_args()

    # cache=False makes fetch_works hit internal.list_works(..., cache=False), which
    # paginates directly over just [start, start+count) via the IMSLP API. This avoids
    # internal.load_cache(from_file=False), which forces a full, unbounded live re-fetch
    # of the entire catalog (including the unused "people" list) from scratch on every
    # run, with no caching between runs and silent truncation on any request hiccup.
    print(f"Fetching up to {args.count} works starting at {args.start} (batch={args.batch})")
    works = fetch_works(start=args.start, count=args.count, batch=args.batch, cache=False)
    print(f"Fetched {len(works)} works")

    if not works:
        print("No works fetched — exiting with error so the caller does not advance past this range.")
        sys.exit(1)

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"Writing CSV to {args.output} (append={args.append})")
    written = populate_csv(works, args.output, append=args.append)
    print(f"Wrote {written} rows")

    if written == 0:
        print("No rows written — exiting with error so the caller does not advance past this range.")
        sys.exit(1)


if __name__ == "__main__":
    main()
