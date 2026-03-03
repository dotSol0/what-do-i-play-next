import csv
import os
import tempfile

from data import populate


def test_populate_ignores_extra_year_key(tmp_path):
    # create a fake work list with one dummy work; file_scrape will be monkeypatched
    works = [None]

    # monkeypatch the file_scrape to return dict with an extra "Year" key
    def fake_file_scrape(work):
        return {
            "Title": "Test",
            "Composer": "Composer",
            "Permlink": "http://example.com",
            "Instrumentation": "piano",
            "Key": "C major",
            "Piece Style": "test",
            "First Performance": "",
            "Year/Date of Composition": "2021",
            "Composer Time Period": "modern",
            "Average Duration": "1",
            "num_downloads": "42",
            "Year": "SHOULD_BE_IGNORED",
        }

    # patch the function
    original = populate.file_scrape
    populate.file_scrape = fake_file_scrape
    try:
        out_file = tmp_path / "out.csv"
        populate.populate_csv(works, str(out_file))

        # read back and verify
        with open(out_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            assert "Year" not in reader.fieldnames
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]["Year/Date of Composition"] == "2021"
            assert rows[0]["num_downloads"] == "42"
    finally:
        populate.file_scrape = original
