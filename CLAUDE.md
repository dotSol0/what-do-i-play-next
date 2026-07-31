# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A classical sheet-music recommender built on scraped IMSLP metadata (title, composer,
instrumentation, key, era, duration, download count). Current app is a Streamlit
prototype (`frontend/app/streamlit.py`) driven by a baseline filter/sort recommender.
`docs/architecture.md` describes a target architecture (React/Vite + FastAPI + Supabase)
that has **not** been built yet — treat it as a roadmap, not current state. Don't assume
a `backend/` service exists; there isn't one yet.

There is also a standalone design-handoff prototype under
`Whatdoiplaynext UI redesign/design_handoff_play_next/` — a self-contained React + Vite
app with a hardcoded sample dataset (`src/data/catalog.js`) and a placeholder similarity
function (`src/lib/recommend.js`). It's a visual/interaction reference for a future
rebuild of the Streamlit app, not integrated with the real data pipeline. Its README
documents the intended screens (Home/Browse/Play Next) and design tokens in detail.

## Commands

Python env: this repo has both `venv/` and `.venv/` checked into the working tree
(not just gitignored) — check which one is active (`which python`) before installing.

```bash
pip install -r requirements.txt

# Run the app
streamlit run frontend/app/streamlit.py

# Run tests (from repo root, not inside tests/)
python -m pytest tests/

# Run a single test file / test
python -m pytest tests/test_predict_piece.py
python -m pytest tests/test_predict_piece.py::test_name -v
```

`tests/test_recommend.py` currently has a syntax error (unclosed brace) and fails to
collect — this breaks a bare `pytest` run for the whole suite. Run other test files
directly by path if you hit this, and mention it if asked to "make tests pass."

Design-handoff prototype (independent of everything else, has its own package.json):
```bash
cd "Whatdoiplaynext UI redesign/design_handoff_play_next"
npm install && npm run dev
```

## Data pipeline

- `data/imslp_fetch.py` — pages through the IMSLP API (`imslp` package's
  `internal.list_works`) in batches.
- `data/scraper.py` — scrapes an IMSLP wiki page's infobox table for metadata
  (Instrumentation, Key, Piece Style, First Performance, Year/Date of Composition,
  Composer Time Period, Average Duration).
- `data/adding_downloads.py` — separately scrapes each piece's page for its download
  count (`num_downloads`), threaded (`ThreadPoolExecutor`), with resumable
  append-to-CSV logic. Keep concurrency low (~5 workers) — IMSLP starts banning
  requests above that.
- `data/populate.py` — orchestrates fetch → scrape → download-count → CSV row, via
  `file_scrape()` / `populate_csv()`.
- `data/cleaner.py` — post-processing/normalization pass over a scraped CSV: parses
  years, alphabetizes/normalizes instrumentation tokens, normalizes duration strings to
  minutes, lowercases certain fields, and expands `"X or Y"` / `"(or Z)"` instrumentation
  strings into distinct catalog entries.
- `scripts/run_api_call.py` — CLI entrypoint gluing fetch + populate together; reads
  `START`/`COUNT`/`OUTPUT_PATH` from env or flags.
- `scripts/fix_year_column.py` — one-off repair script for CSVs from an older scraper
  version that emitted a stray `Year` column, shifting later fields.

### Automated collection (`.github/workflows/run_api_call.yml`)

Runs every 12 hours via `workflow_dispatch`/cron. Reads the current offset from
`state/offset.txt`, fetches the next 20k works, appends to
`data/processed/raw-full.csv`, advances `state/offset.txt`, and commits+pushes both
files as `chore: IMSLP batch <offset>` (see recent git log). If you touch this
pipeline, keep the offset file and the CSV append in sync — advancing one without the
other will cause the next run to duplicate or skip a block of works.

Processed/output CSVs of note: `data/processed/processed-700.csv` (small, early
dataset), `data/processed/processed-40k.csv` (current dataset the Streamlit app loads),
`data/processed/raw-full.csv` / `data/raw-full.csv` (raw scraper output, pre-cleaning).

## Recommendation logic

Two independent, non-ML rule-based scorers live under `ml/inference/`:

- `ml/inference/recommend.py` — `baseline_query(query, df)`: applies a sequence of
  independent filters (time period / instrument / key / mode / year range / duration)
  from a fixed-position `query` list, then sorts by `num_downloads`. This is the "browse
  with filters" path used by the top half of the Streamlit UI.
- `ml/inference/predict_piece.py` — `predict_recommendations(target, df, top_n)`: the
  "what did you play last" path. Filters candidates to shared instrumentation (falling
  back to the full set if that empties the result), scores each remaining row against
  `target` with additive integer biases (`_compute_score`: +3 same composer, +4 same
  key, +3 same style, +2 if year within ±100), then sorts by `(similarity_score,
  num_downloads)` descending.

`ml/training/` (`train_model.py`, `train_utils.py`) is currently just a stub/placeholder
for a future embedding-based model — there's no trained model or training loop yet.

Both scorers expect specific column names from the processed CSV (`Title`, `Composer`,
`Permlink`, `Instrumentation`, `Key`, `Piece Style`, `Year`, `Average Duration`,
`num_downloads`) — `Year` here is the cleaned/normalized column from `cleaner.py`, not
the raw `Year/Date of Composition` scrape field.
