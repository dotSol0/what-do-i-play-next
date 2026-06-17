# Architecture

## Overview
Web app for recommending classical sheet music based on user-defined filters and past pieces played.

## Stack
- **Frontend:** React + Vite, deployed on Vercel
- **Backend:** FastAPI, deployed on Render
- **Database:** Supabase (Postgres + pgvector)

## Data Pipeline
- Source: IMSLP public API
- Collection: GitHub Actions workflow runs every 12 hours, appends 20k records to `data/raw-full.csv`, advances `state/offset.txt`
- Import: CSV imported into Supabase `pieces` table after collection is complete

## Services
- `frontend/` — React app, calls backend API
- `backend/` — FastAPI, houses recommendation logic, queries Supabase
- `.github/workflows/` — automated data collection

## API Endpoints
- `POST /recommend` — takes filter inputs, returns ranked piece results

## Recommendation Logic
Hybrid filter + scoring system based on IMSLP categories and piece ratings. Embeddings/semantic search to be added after initial deployment.

## What's Not Here Yet
- Embedding generation and vector search
- User accounts / saved history