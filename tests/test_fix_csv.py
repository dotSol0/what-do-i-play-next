import csv
import os
import tempfile

# import the script module dynamically since `scripts` isn't a package
import importlib.machinery
import importlib.util

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "fix_year_column.py"))
loader = importlib.machinery.SourceFileLoader("fix_year_column", script_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
fix_year_column = importlib.util.module_from_spec(spec)
loader.exec_module(fix_year_column)


def test_repair_moves_year_to_composition(tmp_path, capsys):
    # build a sample CSV with Year field
    header = [
        "Title",
        "Year/Date of Composition",
        "num_downloads",
        "Year",
    ]
    rows = [
        {"Title": "A", "Year/Date of Composition": "", "num_downloads": "", "Year": "1890"},
        {"Title": "B", "Year/Date of Composition": "2020", "num_downloads": "", "Year": "123"},
        {"Title": "C", "Year/Date of Composition": "", "num_downloads": "", "Year": "5000"},
    ]
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    with open(inp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    fix_year_column.repair(str(inp), str(out))

    with open(out, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        assert "Year" not in r.fieldnames
        results = list(r)
        # first row should move 1890 to Year/Date of Composition
        assert results[0]["Year/Date of Composition"] == "1890"
        assert results[0]["num_downloads"] == ""
        # second row should keep original composition year
        assert results[1]["Year/Date of Composition"] == "2020"
        assert results[1]["num_downloads"] == ""
        # third row looks like a download count
        assert results[2]["Year/Date of Composition"] == ""
        assert results[2]["num_downloads"] == "5000"
