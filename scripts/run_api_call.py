#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from imslp.interfaces import internal

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
    parser.add_argument("--output", type=str, default=os.getenv("OUTPUT_PATH", "data/processed_156k.csv"), help="CSV output path")
    parser.add_argument("--batch", type=int, default=5000, help="Batch size per IMSLP request")
    args = parser.parse_args()

    # Avoid resetting/loading the internal cache when running in GitHub Actions by default.
    # This prevents failures when cache files are not present in the runner environment.
    print("Loading IMSLP cache via API crawl...")
    try:
        internal.reset_cache(from_file=False)
        internal.load_cache(from_file=False)
    except Exception as e:
        print(f"Cache load failed: {e}")
        sys.exit(1)
    print(f"Fetching up to {args.count} works starting at {args.start} (batch={args.batch})")
    works = fetch_works(start=args.start, count=args.count, batch=args.batch, cache=True)
    print(f"Fetched {len(works)} works")

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"Writing CSV to {args.output}")
    populate_csv(works, args.output)


if __name__ == "__main__":
    main()
