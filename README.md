# Musical Fingerprint 🎧

https://musical-fingerprint-baliasina.streamlit.app/

A Spotify-inspired **interactive web dashboard** to explore your unique listening story: habits over time, discovery patterns, genre structure, and top artists/tracks.

Built with **Streamlit** + **Plotly**.  

## Highlights
- Time filtering: presets (30/90/180 days, Year, Lifetime) + custom range
- Toggle between **Streams** and **Minutes**
- Multiple interactive views: calendar heatmap, listening clock, discovery gauges, hierarchical charts (sunburst & treemap), “old vs new” trends, and more
- Supports **demo data** (`music_data.csv`) or your own uploaded CSV

---

## Features (What you can explore)
- **KPI row:** total streams, hours, unique tracks/artists/albums, average time before skip
- **Listening Clock:** hour-of-day polar chart
- **Sessions:** session length distribution (based on inactivity gaps)
- **Commit-ment to Music:** GitHub-style daily activity heatmap
- **Discovery:** % and counts of first-time artists/tracks in the selected range
- **Old vs New:** monthly unique tracks — first listens vs revisits (uses full history to detect “first listen”)
- **Hierarchical views**
  - **Sunburst:** Top artists → their most played tracks
  - **Treemap:** Genre bucket → subgenres (click to drill down)
- **Niche Score:** popularity vs your listening intensity (scatter plot)
- **Billboard:** Top artists and top songs

---

## Getting Started

### 1) Install dependencies
Create a virtual environment (recommended), then:

```bash
pip install streamlit pandas numpy plotly
```

If your repo has a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2) Run the app
```bash
streamlit run app.py
```

Streamlit will print a local URL in your terminal.

---

## Using your own data (CSV format)

### Required columns
Your CSV must include these columns:

- `ts` — timestamp of the play event (the app parses it as UTC)
- `ms_played` — play duration in milliseconds
- `master_metadata_track_name` — track name
- `master_metadata_album_artist_name` — artist name
- `master_metadata_album_album_name` — album name
- `artist_popularity` — numeric popularity score (e.g., 0–100)
- `artist_genres` — comma-separated list of genres/subgenres
- `genre_bucket` — higher-level genre category (used for treemap)
- `skipped` — whether the track was skipped (accepted values: true/false, 1/0, yes/no, etc.)

### Columns computed by the app
You do **not** need to provide these; they are derived automatically:
- `date`, `year`, `month`, `dow`, `hour`
- `start_ts` (computed from `ts - ms_played`)
- `track_id` (built as `artist§track`)

### Demo mode
If “Use demo data” is enabled, the app loads a local file named:
- `music_data.csv`

---

## Session definition
Listening sessions are created by grouping consecutive plays where the time gap between events is **≤ 15 minutes**.  
You can change this in `sessionize(..., gap_minutes=15)` inside `app.py`.

---

## Suggested repository structure
```text
.
├── app.py
├── music_data.csv          # optional demo dataset used by “Use demo data”
├── requirements.txt        # recommended
└── assets/                 # optional: screenshots for README
```

---

## Notes & limitations
- This app expects an **already enriched dataset** (it requires `artist_popularity`, `artist_genres`, and `genre_bucket`).
