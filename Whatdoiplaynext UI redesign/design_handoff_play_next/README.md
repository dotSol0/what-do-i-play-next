# Handoff: What Do I Play Next

## Overview
A repertoire-discovery web app for music students browsing a curated database of
**public-domain** pieces (indexed from IMSLP). Three screens:

1. **Home** — landing/discovery surface: search, "pick up where you left off", a
   personalized *you may like* shelf, and *editor's-pick* starters.
2. **Browse** — the searchable library: filter rail + scannable results table.
3. **Play Next** — the recommender: give it the piece you played last, get ranked
   similar pieces with a plain-English reason for each match.

Every piece links **out to IMSLP** via a `View on IMSLP ↗` button — the app never
hosts scores or cover art itself (all licensing/copyright stays with IMSLP).

## About the Design Files
This bundle ships **two things**:

- `reference/Play Next — Prototype.dc.html` — the original design prototype (a single
  self-contained HTML file). This is the **source of truth for look & behavior**.
- A runnable **React + Vite** port under `src/` that recreates the prototype 1:1.

Treat both as **design references**. The React code is a faithful, runnable starting
point — but the real task is to **recreate these designs inside your target codebase**
using its own environment, routing, data layer, and component conventions. If you have
no app yet, the included Vite app is a fine place to start (`npm install && npm run dev`).

## Fidelity
**High-fidelity.** Final colors, typography, spacing, and interactions are settled. Match
the layout and tokens below precisely. The only intentionally *stubbed* parts (clearly
commented in code) are: the filter rail, the search input, and the "Prioritize" toggles —
these are visual placeholders to be wired to real state and services.

## Running the React port
```bash
cd design_handoff_play_next
npm install
npm run dev
```

## File map
```
src/
  main.jsx                 # React entry
  App.jsx                  # screen router (useState: screen + seedId)
  styles.css               # all design tokens + component classes
  data/catalog.js          # sample dataset (replace with real IMSLP index)
  lib/recommend.js         # enrich() + computeMatches() — the similarity stub
  components/
    TopBar.jsx             # persistent burgundy nav bar
    MatchCard.jsx          # recommendation card (score + reasons) — compact & full
    StarterCard.jsx        # editor's-pick card (downloads, no score)
    ResultRow.jsx          # Browse table row (+ ResultHeader)
  screens/
    StartScreen.jsx        # Home
    BrowseScreen.jsx       # Browse
    PlayNextScreen.jsx     # Play Next
```

## Screens / Views

### Home (`StartScreen`)
- **Purpose**: entry point; search, resume, or get recommendations.
- **Layout**: centered column. Masthead (eyebrow + serif H1 + subhead) capped at 720px;
  a 56px-tall search field; era chips. Below, a 1000px-wide block containing three
  sections, each left-aligned:
  1. *Pick up where you left off* — compact 3-column grid of slim cards (title + composer
     + "Similar →"). Clicking routes to Play Next seeded with that piece.
  2. *Because you've been exploring solo cello — you may like* — 4-column grid of compact
     `MatchCard`s, with a `For you / Popular / New additions` segmented toggle (visual).
  3. *New to the library? Start here — editor's picks* — 4-column grid of `StarterCard`s,
     with a `Browse all 12,480 →` link to Browse.
- **Search field**: clicking it routes to Browse (in production, focus + open search).

### Browse (`BrowseScreen`)
- **Purpose**: search and filter the full library.
- **Layout**: full-width search bar row, then a `236px | 1fr` grid — left **filter rail**
  (Era checkboxes w/ counts, Instrument, Duration dual-slider, Key), right **results**
  (sort header + column header + rows).
- **Result row** (`ResultRow`): grid columns `1fr 132px 88px 68px 220px` =
  Piece · Instrumentation · Key · Length · actions. Piece cell shows serif title + era
  tag + composer + download count. Actions: `≈ Similar` (routes to Play Next) and a filled
  `View on IMSLP ↗` button. Row hover tint = `--wine-soft`.

### Play Next (`PlayNextScreen`)
- **Purpose**: recommendations from a seed piece.
- **Layout**: hero band (gradient `--paper2 → --paper`) with eyebrow, serif H1
  "What did you play last?", a bordered input showing the seed as a filled chip + a
  "Show me similar →" button, and three "Prioritize" chips. Below: heading
  "Because you played *{title}*" + a 3-column grid of full `MatchCard`s.
- **MatchCard** (full): era tag + big brass match `%`; serif title + composer·instrument;
  up to 2 reason lines (brass ✦ bullet); full-width `View on IMSLP ↗` + a `≈` similar button.

## Interactions & Behavior
- **Navigation** is local screen state (`App.jsx`): `start | browse | recommend`, plus a
  `seedId`. `goRecommend(id)` sets the seed and switches to Play Next; every `≈` / "Similar"
  affordance and every "pick up where you left off" card calls it. `window.scrollTo(0,0)`
  on each transition.
- **View on IMSLP**: `<a target="_blank" rel="noopener noreferrer" href={permalink}>`.
- **Hover states**: `.btn` darkens to `--wine-d`; `.simbtn` bg → `rgba(122,39,51,.15)`;
  `.a-row` bg → `--wine-soft`; `.likecard` border → `rgba(122,39,51,.35)`.
- **Stubbed (wire these up)**: filter rail, search text/query, sort control, the segmented
  `For you/Popular/New` toggle, and the `Prioritize` chips (should re-weight matches — see
  `computeMatches(seed, { weights })`).

## Recommendation logic
`src/lib/recommend.js → computeMatches(seed, { weights })` is a **placeholder** content
ranker: base score 46, `+26` same composer, `+24` same instrument (first word match),
`+14` same era, `+12` same form; capped at 99; top 6 returned with up to 2 human-readable
reasons. **Replace this** with your cosine-similarity service — keep the return shape
`{ ...piece, score: '87%', reasons: string[] }` and the UI works unchanged. The
`Prioritize` chips map to the `weights` argument.

## State Management
- `screen: 'start' | 'browse' | 'recommend'`
- `seedId: number` — id of the piece Play Next is built from
- (To add) filter state, search query, sort key, active toggle segment, priority weights.

## Design Tokens (from `styles.css`)
Colors:
- bg `#e7e0d1` · paper `#f8f4ea` · paper2 `#efe8d8`
- ink `#1c1710` · ink2 `#453d2f` · muted `#786f5b` · faint `#a99f86`
- line `rgba(28,23,16,.12)` · line2 `rgba(28,23,16,.06)`
- **wine (dominant)** `#7a2733` · wine-d `#611c27` · wine-soft `rgba(122,39,51,.09)`
- **brass (accent)** `#a97b33` · brass-d `#835e22`
- Era tags: baroque → brass `rgba(169,123,51,.18)`/`#835e22`; classical → slate
  `rgba(60,90,105,.16)`/`#2f4a58`; romantic → wine `rgba(122,39,51,.14)`/`#7a2733`.

Type:
- Serif (titles/headings): **Spectral** — H1 30–42px/1.12–1.2, card titles 14.5–15.5px.
- Sans (UI/body): **IBM Plex Sans** — body 12–14px.
- Mono (metadata, eyebrows, keys, counts): **IBM Plex Mono** — 10–12px, letter-spacing
  .06–.16em, often uppercase.

Radius: chips 20px · buttons 8–9px · cards 10–13px · fields 9–13px.
Shadow (elevated fields): `0 6px 22px -12px rgba(122,39,51,.55)`.
Layout widths: content 720px, library block 1000px, Browse rail 236px.

## Data fields (per piece)
`Title, Composer, Instrumentation, Key, Piece Style (era), Average Duration,
num_downloads, Permlink (url)` — plus a derived `form` used only by the similarity stub.
See `src/data/catalog.js`.

## Assets
None to hand off. No images, cover art, or scores — deliberately. Fonts load from Google
Fonts (Spectral, IBM Plex Sans, IBM Plex Mono). Iconography is Unicode glyphs
(♪ ⌕ ↻ ✦ ≈ ↗); substitute your icon set if preferred.
