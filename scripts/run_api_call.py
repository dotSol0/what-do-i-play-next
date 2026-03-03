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
    parser.add_argument("--use-cache", action="store_true", help="Use internal cache when listing works")
    parser.add_argument("--force-cache-reset", action="store_true", help="Force reset/load of internal cache even in CI")
    args = parser.parse_args()

    # Avoid resetting/loading the internal cache when running in GitHub Actions by default.
    # This prevents failures when cache files are not present in the runner environment.
    ci_mode = os.getenv("GITHUB_ACTIONS") == "true"
    if ci_mode and not args.force_cache_reset:
        print("Detected GitHub Actions CI environment — skipping internal.reset_cache/load. Use --force-cache-reset to override.")
    else:
        print(f"Resetting/loading internal cache (from_file=True) to match notebook behaviour")
        try:
            internal.reset_cache(from_file=True)
            internal.load_cache(from_file=True)
        except Exception as e:
            print(f"Cache reset/load failed: {e}")

    print(f"Fetching up to {args.count} works starting at {args.start} (batch={args.batch})")
    works = fetch_works(start=args.start, count=args.count, batch=args.batch, cache=args.use_cache)
    print(f"Fetched {len(works)} works")

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"Writing CSV to {args.output}")
    populate_csv(works, args.output)


if __name__ == "__main__":
    main()
