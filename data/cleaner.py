import re
import csv
from typing import Optional, List, Dict, Any
import itertools


def normalize_year(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    match = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", str(value))
    return int(match.group()) if match else None


def normalize_instrumentation(value: Any) -> List[str]:
    if not value:
        return []

    if isinstance(value, list):
        items = value
    else:
        items = re.split(r",|;|\\|/", str(value))

    instruments = []
    for inst in items:
        inst = inst.lower().strip()
        inst = inst.replace("solo", "").strip()
        if inst:
            instruments.append(inst)

    return sorted(set(instruments))


def alphabetize_instrumentation(value: Any) -> List[str]:
    """Return an alphabetized list of instrumentation tokens.

    Accepts a list or a string. Normalizes whitespace and lowercases items
    before sorting. Returns a list of unique, sorted instruments.
    """
    if not value:
        return []

    if isinstance(value, str):
        tokens = [t.strip() for t in re.split(r",|;|\\|/", value) if t.strip()]
    else:
        tokens = list(value)

    cleaned = []
    for t in tokens:
        if not t:
            continue
        t2 = t.lower().strip()
        t2 = t2.replace("solo", "").strip()
        if t2:
            cleaned.append(t2)

    # deduplicate while preserving alphabetical order
    unique = sorted(set(cleaned), key=lambda s: s.lower())
    return unique


LOWERCASE_FIELDS = {
    "Instrumentation",
    "Piece Style",
    "Composer Time Period",
    "First Performance",
}


def normalize_case(row: Dict[str, Any]) -> Dict[str, Any]:
    for field in LOWERCASE_FIELDS:
        if row.get(field):
            try:
                row[field] = row[field].lower()
            except Exception:
                pass
    return row


def normalize_style(row: Dict[str, Any]) -> Dict[str, Any]:
    if not row.get("Piece Style") and row.get("Composer Time Period"):
        row["Piece Style"] = row["Composer Time Period"]
    return row


def normalize_duration(value: Optional[str]) -> Optional[int]:
    if not value:
        return None

    value = str(value).lower()

    minutes = 0

    hour_match = re.search(r"(\d+)\s*(hour|hours|h)", value)
    min_match = re.search(r"(\d+)\s*(minute|minutes|min)", value)

    if hour_match:
        minutes += int(hour_match.group(1)) * 60
    if min_match:
        minutes += int(min_match.group(1))

    return minutes if minutes > 0 else None


def normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    row = dict(row)

    row["Year"] = normalize_year(row.get("Year/Date of Composition"))
    row["Instrumentation"] = normalize_instrumentation(row.get("Instrumentation"))
    # ensure instrumentation tokens are alphabetized
    row["Instrumentation"] = alphabetize_instrumentation(row["Instrumentation"])
    row["Average Duration"] = normalize_duration(row.get("Average Duration"))

    row = normalize_case(row)
    row = normalize_style(row)

    return row


def _serialize_for_csv(row: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in row.items():
        if isinstance(v, list):
            out[k] = ", ".join(v)
        elif v is None:
            out[k] = ""
        else:
            out[k] = str(v)
    return out


def expand_instrumentation_options(raw_value: Any) -> List[str]:
    if not raw_value:
        return [""]

    s = str(raw_value)

    # Top-level: if semicolons exist, treat them as separate full options
    top_options = [opt.strip() for opt in re.split(r"\s*;\s*", s) if opt.strip()]

    results = []
    for opt in top_options:
        # Split tokens by comma (instruments in the ensemble)
        tokens = [t.strip() for t in re.split(r",\s*", opt) if t.strip()]

        alt_lists = []
        for tok in tokens:
            # Parenthetical alternative like 'viola(or violin)'
            m = re.match(r"^(.+?)\s*\(\s*or\s+(.+?)\s*\)$", tok, flags=re.I)
            if m:
                base = m.group(1).strip()
                alt = m.group(2).strip()
                alt_lists.append([base, alt])
                continue

            # Inline ' or ' alternatives like 'harpsichord or organ'
            if re.search(r"\bor\b", tok, flags=re.I):
                parts = [p.strip() for p in re.split(r"\s+or\s+", tok, flags=re.I) if p.strip()]
                if parts:
                    alt_lists.append(parts)
                    continue

            # otherwise single option
            alt_lists.append([tok])

        # Cartesian product of alternatives to produce combinations
        has_alternatives = any(len(lst) > 1 for lst in alt_lists)
        joiner = "/" if has_alternatives else ", "
        for combo in itertools.product(*alt_lists):
            inst_str = joiner.join([c for c in combo if c])
            results.append(inst_str)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for r in results:
        if r not in seen:
            seen.add(r)
            deduped.append(r)
    return deduped
def normalize_file(raw_file: str, processed_file: str, encoding: str = "utf-8") -> None:
    with open(raw_file, newline="", encoding=encoding) as infile, \
         open(processed_file, "w", newline="", encoding=encoding) as outfile:

        reader = csv.DictReader(infile)

        try:
            first_row = next(reader)
        except StopIteration:
            raise ValueError("Input CSV is empty")

        processed_first = normalize_row(first_row)

        fieldnames = list(processed_first.keys())

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # write the first processed row
        writer.writerow(_serialize_for_csv(processed_first))

        for row in reader:
            processed = normalize_row(row)
            writer.writerow(_serialize_for_csv(processed))


if __name__ == "__main__":
    # simple CLI convenience
    import sys
    if len(sys.argv) >= 3:
        normalize_file(sys.argv[1], sys.argv[2])

