#!/usr/bin/env python3
"""Utility to repair CSV files that contain an unintended 'Year' column.

The IMSLP scraping pipeline used to accidentally emit a "Year" field which
ended up in the header and caused later values (including download counts) to
shift right.  After 2026‑03 we fixed the generator to drop this key and ignore
extras, but existing CSVs may still contain the stray column.

Usage:

    python scripts/fix_year_column.py input.csv output.csv

The script will remove the "Year" column and, when possible, relocate its
values into the appropriate field:

* if the value looks like a plausible composition year and the
  "Year/Date of Composition" column is empty, it will be moved there.
* otherwise, if the value appears numeric and the "num_downloads" column is
  empty, it will be used for downloads.
"""

import csv
import sys


def repair(in_path: str, out_path: str) -> None:
    with open(in_path, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if "Year" not in reader.fieldnames:
            print(f"no 'Year' column found in {in_path}; nothing to do")
            return

        # build new header without the stray column
        fieldnames = [f for f in reader.fieldnames if f != "Year"]
        with open(out_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                yearval = row.pop("Year", "")
                if yearval and not row.get("Year/Date of Composition"):
                    try:
                        y = int(yearval)
                        # heuristics for a genuine year versus a download count
                        if 1000 <= y <= 2100:
                            row["Year/Date of Composition"] = yearval
                        else:
                            if not row.get("num_downloads"):
                                row["num_downloads"] = yearval
                    except ValueError:
                        pass

                writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    repair(sys.argv[1], sys.argv[2])
