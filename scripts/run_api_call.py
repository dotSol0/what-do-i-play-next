#!/usr/bin/env python3
import argparse
import os
import sys
from imslp.interfaces import internal

from data.imslp_fetch import fetch_works
from data.populate import populate_csv


def main():
    parser = argparse.ArgumentParser(description="Fetch IMSLP works and populate CSV")
    parser.add_argument("--count", type=int, default=int(os.getenv("COUNT", "156000")), help="Number of works to fetch")
    parser.add_argument("--output", type=str, default=os.getenv("OUTPUT_PATH", "data/processed_156k.csv"), help="CSV output path")
    parser.add_argument("--batch", type=int, default=5000, help="Batch size per IMSLP request")
    parser.add_argument("--use-cache", action="store_true", help="Use internal cache when listing works")
    args = parser.parse_args()

    print(f"Resetting/loading internal cache (from_file=True) to match notebook behaviour")
    try:
        internal.reset_cache(from_file=True)
        internal.load_cache(from_file=True)
    except Exception as e:
        print(f"Cache reset/load failed: {e}")

    print(f"Fetching up to {args.count} works (batch={args.batch})")
    works = fetch_works(start=0, count=args.count, batch=args.batch, cache=args.use_cache)
    print(f"Fetched {len(works)} works")

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"Writing CSV to {args.output}")
    populate_csv(works, args.output)


if __name__ == "__main__":
    main()
