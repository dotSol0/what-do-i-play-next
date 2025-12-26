import re
import csvstream

def normalize_year(value):
    if not value:
        return None
    match = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", value)
    return int(match.group()) if match else None


def normalize_instrumentation(value):
    if not value:
        return []

    instruments = []
    for inst in value.split(","):
        inst = inst.lower().strip()
        inst = inst.replace("solo", "").strip()
        if inst:
            instruments.append(inst)

    return sorted(set(instruments))

LOWERCASE_FIELDS = {
    "Instrumentation",
    "Piece Style",
    "Composer Time Period",
    "First Performance"
}

def normalize_case(row):
    for field in LOWERCASE_FIELDS:
        if row.get(field):
            row[field] = row[field].lower()
    return row


def normalize_style(row):
    if not row.get("Piece Style") and row.get("Composer Time Period"):
        row["Piece Style"] = row["Composer Time Period"]
    return row

import re

def normalize_duration(value):
    if not value:
        return None

    value = value.lower()

    minutes = 0

    hour_match = re.search(r"(\d+)\s*(hour|hours|h)", value)
    min_match = re.search(r"(\d+)\s*(minute|minutes|min)", value)

    if hour_match:
        minutes += int(hour_match.group(1)) * 60
    if min_match:
        minutes += int(min_match.group(1))

    return minutes if minutes > 0 else None


def normalize_row(row):
    row = row.copy()

    row["Year"] = normalize_year(row.get("Year/Date of Composition"))
    row["Instrumentation"] = normalize_instrumentation(row.get("Instrumentation"))
    row["Average Duration"] = normalize_duration(row.get("Average Duration"))

    row = normalize_case(row)
    row = normalize_style(row)

    return row

def normalize_file(raw_file, processed_file):
    with open(raw_file, newline"", encoding=encoding) as infile, \
         open(output_path, "w", newline="", encoding=encoding) as outfile:

         reader = csv.DictReader(infile)

         try:
            first_row = next(reader)

         except StopIteration:
            raise ValueError("Input CSV is empty")
        
         processed_first = normalize_row(first_row)

         writer = csv.DictWriter(
            outfile, 
            fieldnames = processed_first.keys()
         )
         writer.writeheader()
         writer.writerow(processed_first)

         for row in reader:
            processed = process_row(row)
            writter.writerow(processed)

