

## `app.py` (full working MVP)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, datetime, date

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Musical Fingerprint",
    page_icon="🎧",
    layout="wide"
)

# ----------------------------
# Design system
# ----------------------------
UI = {
    "bg": "#0E1117",
    "panel": "#161B22",
    "border": "#2A2F3A",
    "text": "#E6EDF3",
    "muted": "#9BA3AF",
    "accent": "#1DB954",   # Spotify-ish green
}

GENRE_COLORS = {
    "EDM & Progressive": "#06B6D4",
    "Trance": "#8B5CF6",
    "Electronica / Chill": "#C7E3FF",
    "Lo-Fi / Chillhop": "#D6B370",
    "Pop & Regional Pop": "#EC4899",
    "Rock / Metal / Core": "#374151",
    "Folk / Acoustic / Celtic": "#16A34A",
    "Hip-Hop / Rap": "#F59E0B",
    "Soundtrack / Score / Musicals": "#2563EB",
    "Others": "#9CA3AF",
}

st.markdown(
    f"""
<style>
/* Page */
.block-container {{
    padding-top: 1.25rem;
    padding-bottom: 2rem;
}}
h1, h2, h3 {{
    letter-spacing: -0.02em;
}}
small, .stCaption {{
    color: {UI["muted"]} !important;
}}

/* Make expanders and charts feel like cards */
div[data-testid="stExpander"] > details {{
    background: {UI["panel"]};
    border: 1px solid {UI["border"]};
    border-radius: 14px;
    padding: 6px 10px;
}}
div[data-testid="stPlotlyChart"] {{
    background: {UI["panel"]};
    border: 1px solid {UI["border"]};
    border-radius: 14px;
    padding: 10px;
}}

/* KPI cards */
.kpi-card {{
    background: {UI["panel"]};
    border: 1px solid {UI["border"]};
    border-radius: 14px;
    padding: 14px 14px;
}}
.kpi-title {{
    font-size: 0.85rem;
    color: {UI["muted"]};
    margin-bottom: 4px;
}}
.kpi-value {{
    font-size: 1.65rem;
    font-weight: 700;
}}
.kpi-sub {{
    font-size: 0.85rem;
    color: {UI["muted"]};
}}

/* Section titles */
.section-title {{
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0.25rem 0 0.75rem 0;
}}
</style>
""",
    unsafe_allow_html=True
)


# ----------------------------
# Helpers: loading + cleaning
# ----------------------------
REQUIRED_COLS = [
    "ts", "ms_played",
    "master_metadata_track_name",
    "master_metadata_album_artist_name",
    "master_metadata_album_album_name",
    "artist_popularity",
    "artist_genres",
    "genre_bucket",
    "skipped"
]

def _to_bool(x):
    if isinstance(x, bool):
        return x
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    return s in ["true", "t", "1", "yes", "y"]

def style_fig(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor=UI["panel"],
        plot_bgcolor=UI["panel"],
        font=dict(color=UI["text"], family="Inter, system-ui, sans-serif"),
        margin=dict(l=12, r=12, t=45, b=12),
        title=dict(font=dict(size=16), x=0.02),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(0,0,0,0)"
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor=UI["border"], zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=UI["border"], zeroline=False)
    return fig

def show_fig(fig, height=300):
    st.plotly_chart(style_fig(fig, height=height), use_container_width=True)



@st.cache_data(show_spinner=False)
def load_csv(uploaded_file=None, path=None) -> pd.DataFrame:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif path is not None:
        df = pd.read_csv(path)
    else:
        return pd.DataFrame()

    # Normalize columns if needed
    # (keep as-is, just validate)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df.copy()
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts"])

    df["ms_played"] = pd.to_numeric(df["ms_played"], errors="coerce").fillna(0).astype(int)

    # booleans
    df["skipped"] = df["skipped"].apply(_to_bool)

    # popularity
    df["artist_popularity"] = pd.to_numeric(df["artist_popularity"], errors="coerce").fillna(np.nan)

    # time helpers
    df["date"] = df["ts"].dt.date
    df["year"] = df["ts"].dt.year
    df["month"] = df["ts"].dt.to_period("M").astype(str)
    df["dow"] = df["ts"].dt.dayofweek  # Mon=0
    df["hour"] = df["ts"].dt.hour

    # start time estimate (end ts - ms_played)
    df["start_ts"] = df["ts"] - pd.to_timedelta(df["ms_played"], unit="ms")

    # track id fallback
    if "track_id" not in df.columns:
        df["track_id"] = (df["master_metadata_album_artist_name"].astype(str) + "§" +
                          df["master_metadata_track_name"].astype(str))

    # Ensure strings
    for c in ["master_metadata_track_name", "master_metadata_album_artist_name",
              "master_metadata_album_album_name", "genre_bucket", "artist_genres"]:
        df[c] = df[c].astype(str).fillna("")

    return df

# @st.cache_data(show_spinner=False)
# def make_demo_data(n=25000, start="2021-01-01", end="2025-12-01") -> pd.DataFrame:
#     rng = np.random.default_rng(7)
#     start_dt = pd.to_datetime(start, utc=True)
#     end_dt = pd.to_datetime(end, utc=True)
#     ts = pd.to_datetime(rng.integers(start_dt.value//10**9, end_dt.value//10**9, size=n), unit="s", utc=True)

#     artists = ["Gåte", "Martin Garrix", "Twenty One Pilots", "Avicii", "Mac Miller",
#                "Taylor Swift", "Hans Zimmer", "AURORA", "Käärijä", "Rammstein"]
#     tracks = [f"Track {i}" for i in range(1, 301)]
#     albums = [f"Album {i}" for i in range(1, 101)]
#     buckets = ["EDM & Progressive", "Trance", "Electronica / Chill", "Lo-Fi / Chillhop",
#                "Pop & Regional Pop", "Rock / Metal / Core", "Folk / Acoustic / Celtic",
#                "Hip-Hop / Rap", "Soundtrack / Score / Musicals", "Others"]

#     df = pd.DataFrame({
#         "ts": ts,
#         "platform": rng.choice(["android", "ios", "desktop", "web"], size=n),
#         "ms_played": rng.integers(5_000, 240_000, size=n),
#         "conn_country": rng.choice(["ES", "UA", "FR", "DE", "NL"], size=n, p=[0.45, 0.25, 0.15, 0.10, 0.05]),
#         "master_metadata_track_name": rng.choice(tracks, size=n),
#         "master_metadata_album_artist_name": rng.choice(artists, size=n),
#         "master_metadata_album_album_name": rng.choice(albums, size=n),
#         "spotify_track_uri": "spotify:track:demo",
#         "reason_start": rng.choice(["trackdone", "clickrow", "appload"], size=n),
#         "reason_end": rng.choice(["trackdone", "endplay", "fwdbtn", "backbtn"], size=n),
#         "skipped": rng.choice([True, False], size=n, p=[0.12, 0.88]),
#         "offline": rng.choice([True, False], size=n, p=[0.05, 0.95]),
#         "track_id": rng.choice([f"demo_{i}" for i in range(1, 301)], size=n),
#         "artist_id": rng.choice([f"artist_{i}" for i in range(1, 51)], size=n),
#         "artist_genres": rng.choice(["trance", "folk metal", "pop", "lo-fi", "edm", "score", "rap"], size=n),
#         "artist_popularity": rng.integers(5, 95, size=n),
#         "artist_followers": rng.integers(500, 5_000_000, size=n),
#         "genre_bucket": rng.choice(buckets, size=n),
#         "play_id": None
#     })

#     # finalize types like real loader does
#     df["ts"] = pd.to_datetime(df["ts"], utc=True)
#     df["date"] = df["ts"].dt.date
#     df["year"] = df["ts"].dt.year
#     df["month"] = df["ts"].dt.to_period("M").astype(str)
#     df["dow"] = df["ts"].dt.dayofweek
#     df["hour"] = df["ts"].dt.hour
#     df["start_ts"] = df["ts"] - pd.to_timedelta(df["ms_played"], unit="ms")
#     return df

DEMO_PATH = "music_data.csv"

@st.cache_data(show_spinner=False)
def load_demo_file() -> pd.DataFrame:
    return load_csv(path=DEMO_PATH)


# ----------------------------
# Computations
# ----------------------------
def measure_value(df: pd.DataFrame, measure: str) -> pd.Series:
    if measure == "Streams":
        return pd.Series(np.ones(len(df), dtype=float), index=df.index)
    # Minutes
    return df["ms_played"] / (1000 * 60)

def fmt_big(n):
    try:
        if abs(n) >= 1_000_000:
            return f"{n/1_000_000:.2f}M"
        if abs(n) >= 1_000:
            return f"{n/1_000:.1f}K"
        if float(n).is_integer():
            return f"{int(n)}"
        return f"{n:.2f}"
    except Exception:
        return str(n)

@st.cache_data(show_spinner=False)
def compute_first_listen_flags(df: pd.DataFrame) -> pd.DataFrame:
    # "New song" = first time you ever played that track_id
    first_ts = df.groupby("track_id")["ts"].min()
    df = df.copy()
    df["first_listen_ts"] = df["track_id"].map(first_ts)
    df["is_new_to_you"] = df["ts"] == df["first_listen_ts"]
    return df

@st.cache_data(show_spinner=False)
def sessionize(df: pd.DataFrame, gap_minutes=15) -> pd.DataFrame:
    # Simple sessionization by time gap between consecutive plays
    d = df.sort_values("start_ts").copy()
    gap = pd.Timedelta(minutes=gap_minutes)
    prev_end = d["ts"].shift(1)
    new_session = (d["start_ts"] - prev_end) > gap
    d["session_id"] = new_session.cumsum().fillna(0).astype(int)
    # session length in minutes
    session_len = d.groupby("session_id")["ms_played"].sum() / (1000 * 60)
    d["session_minutes"] = d["session_id"].map(session_len)
    return d

def bins_session_minutes(x):
    if x < 120: return "<2h"
    if x < 240: return "2–4h"
    if x < 360: return "4–6h"
    return ">6h"

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.title("🎛 Controls")

use_demo = st.sidebar.toggle("Use included dataset", value=True)

uploaded = None
if not use_demo:
    uploaded = st.sidebar.file_uploader("Upload your own Spotify data CSV", type=["csv"])


measure = st.sidebar.radio("Measure", ["Streams", "Minutes"], horizontal=True)

# ----------------------------
# Load data
# ----------------------------
try:
    if use_demo:
        df = load_demo_file()
        st.sidebar.success("Loaded included dataset (music_data.csv).")
    else:
        if uploaded is None:
            st.info("Upload your CSV in the sidebar or turn on 'Use included dataset'.")
            st.stop()
        df = load_csv(uploaded_file=uploaded)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Date filter
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# filter base
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_f = df.loc[mask].copy()

# compute "new to you" flags only once on full df, then filter
df_new = compute_first_listen_flags(df)
df_new_f = df_new.loc[mask].copy()

# ----------------------------
# Header
# ----------------------------
title_col, legend_col = st.columns([2.2, 1.0], vertical_alignment="center")

with title_col:
    st.markdown("## 🎧 Musical Fingerprint")
    st.caption("An interactive dashboard showing long-term listening habits: time patterns, genre identity, novelty, and niche taste.")

with legend_col:
    with st.expander("What do charts mean? (quick)"):
        st.markdown(
            """
- **Old vs New**: *New* means **first time you ever listened** to that track (new-to-you).  
- **Niche scatter**: X = Spotify popularity (0–100), Y = your listening (streams/minutes).  
- All views respect the **date range** + **measure**.
            """
        )

st.divider()

# ----------------------------
# KPI row (general stats)
# ----------------------------
val = measure_value(df_f, measure)
total_streams = len(df_f)
total_minutes = df_f["ms_played"].sum() / (1000 * 60)
total_hours = total_minutes / 60

n_tracks = df_f["master_metadata_track_name"].nunique()
n_artists = df_f["master_metadata_album_artist_name"].nunique()
n_albums = df_f["master_metadata_album_album_name"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, title, value, sub=""):
    col.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


kpi(k1, "Streams", f"{total_streams:,}")
kpi(k2, "Hours listened", f"{total_hours:,.1f}")
kpi(k3, "Unique tracks", f"{n_tracks:,}")
kpi(k4, "Unique artists", f"{n_artists:,}")
kpi(k5, "Unique albums", f"{n_albums:,}")

# small trend sparklines (by month)
with st.expander("Trends over time (mini)"):
    by_month = df_f.groupby("month", as_index=False).agg(
        streams=("ts", "count"),
        minutes=("ms_played", lambda s: s.sum()/(1000*60)),
        artists=("master_metadata_album_artist_name", "nunique"),
        tracks=("master_metadata_track_name", "nunique")
    )
    y = "streams" if measure == "Streams" else "minutes"
    fig_tr = px.line(by_month, x="month", y=y, markers=True)
    fig_tr.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_tr, use_container_width=True)
    show_fig(fig_tr, height=220)


st.divider()

# ----------------------------
# Main layout: left + right
# ----------------------------
left, right = st.columns([1.25, 1.0], gap="large")


# ===== LEFT COLUMN (your bottom-left big panel) =====
with left:
    st.subheader("Core patterns")

    # Top #1 artist + track cards
    top_artist = (
        df_f.groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )
    top_track = (
        df_f.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"])["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    cA, cB = st.columns(2)

    with cA:
        if len(top_artist) > 0:
            artist_name = top_artist.index[0]
            st.markdown("### 🥇 No.1 Artist")
            st.write(artist_name)
            st.caption(f"{fmt_big(top_artist.iloc[0]/(1000*60) if measure=='Minutes' else df_f[df_f['master_metadata_album_artist_name']==artist_name].shape[0])} {measure.lower()}")
        else:
            st.write("No data in selection.")

    with cB:
        if len(top_track) > 0:
            (track_name, track_artist) = top_track.index[0]
            st.markdown("### 🥇 No.1 Track")
            st.write(f"{track_name} — {track_artist}")
            st.caption(f"{fmt_big(top_track.iloc[0]/(1000*60) if measure=='Minutes' else df_f[(df_f['master_metadata_track_name']==track_name) & (df_f['master_metadata_album_artist_name']==track_artist)].shape[0])} {measure.lower()}")
        else:
            st.write("No data in selection.")

    # Listening clock (polar)
    st.markdown("### 🕒 Listening Clock")
    by_hour = df_f.copy()
    by_hour["m"] = measure_value(by_hour, measure)
    hour_agg = by_hour.groupby("hour", as_index=False)["m"].sum()

    fig_clock = go.Figure()
    fig_clock.add_trace(go.Barpolar(
        r=hour_agg["m"],
        theta=hour_agg["hour"] * 15,  # 24*15=360
        width=[15]*len(hour_agg),
        hovertemplate="Hour %{customdata}: %{r:.2f}<extra></extra>",
        customdata=hour_agg["hour"]
    ))
    fig_clock.update_layout(
        height=320,
        margin=dict(l=10,r=10,t=10,b=10),
        polar=dict(
            angularaxis=dict(direction="clockwise", rotation=90, tickmode="array",
                             tickvals=[i*15 for i in range(0,24,3)],
                             ticktext=[f"{i:02d}:00" for i in range(0,24,3)]),
        )
    )
    #st.plotly_chart(fig_clock, use_container_width=True)
    show_fig(fig_clock, height=220)


    # Old vs New (clarified!)
    st.markdown("### 🆕 Old vs New (new-to-you)")
    tmp = df_new_f.copy()
    tmp["m"] = measure_value(tmp, measure)
    # group by month: new vs old share
    g = tmp.groupby(["month", "is_new_to_you"], as_index=False)["m"].sum()
    pivot = g.pivot(index="month", columns="is_new_to_you", values="m").fillna(0)
    pivot.columns = ["Old (repeat)", "New-to-you"] if list(pivot.columns) == [False, True] else [str(c) for c in pivot.columns]
    pivot = pivot.reset_index()

    fig_oldnew = go.Figure()
    if "Old (repeat)" in pivot.columns:
        fig_oldnew.add_trace(go.Scatter(x=pivot["month"], y=pivot["Old (repeat)"], mode="lines+markers", name="Old (repeat)"))
    if "New-to-you" in pivot.columns:
        fig_oldnew.add_trace(go.Scatter(x=pivot["month"], y=pivot["New-to-you"], mode="lines+markers", name="New-to-you"))
    fig_oldnew.update_layout(height=280, margin=dict(l=10,r=10,t=10,b=10), legend=dict(orientation="h"))
    #st.plotly_chart(fig_oldnew, use_container_width=True)
    show_fig(fig_oldnew, height=280)


    # Sunburst: top 3 artists + top 3 tracks each
    st.markdown("### 🌞 Top artists → top tracks (Sunburst)")
    tmp2 = df_f.copy()
    tmp2["m"] = measure_value(tmp2, measure)
    top3_art = tmp2.groupby("master_metadata_album_artist_name")["m"].sum().sort_values(ascending=False).head(3).index
    tmp2 = tmp2[tmp2["master_metadata_album_artist_name"].isin(top3_art)].copy()

    # keep only top 3 tracks per artist
    track_rank = (tmp2.groupby(["master_metadata_album_artist_name","master_metadata_track_name"])["m"].sum()
                  .reset_index().sort_values(["master_metadata_album_artist_name","m"], ascending=[True, False]))
    track_rank["rk"] = track_rank.groupby("master_metadata_album_artist_name").cumcount()+1
    keep_tracks = track_rank[track_rank["rk"] <= 3][["master_metadata_album_artist_name","master_metadata_track_name"]]
    tmp2 = tmp2.merge(keep_tracks, on=["master_metadata_album_artist_name","master_metadata_track_name"], how="inner")

    sun = tmp2.groupby(["master_metadata_album_artist_name","master_metadata_track_name"], as_index=False)["m"].sum()
    fig_sun = px.sunburst(
        sun,
        path=["master_metadata_album_artist_name","master_metadata_track_name"],
        values="m"
    )
    fig_sun.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_sun, use_container_width=True)
    show_fig(fig_sun, height=360)


    # Niche scatter
    st.markdown("### 🎯 How niche is your taste?")
    tmp3 = df_f.copy()
    tmp3["m"] = measure_value(tmp3, measure)
    artist_agg = (tmp3.groupby(["master_metadata_album_artist_name","artist_popularity"], as_index=False)
                  .agg(total=("m","sum"),
                       streams=("ts","count"),
                       minutes=("ms_played", lambda s: s.sum()/(1000*60))))
    fig_sc = px.scatter(
        artist_agg,
        x="artist_popularity",
        y="total",
        size="streams",
        hover_name="master_metadata_album_artist_name",
        labels={"artist_popularity":"Artist popularity (Spotify 0–100)", "total":f"Your {measure.lower()}"},
    )
    fig_sc.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_sc, use_container_width=True)
    show_fig(fig_sc, height=280)


# ===== RIGHT COLUMN (calendar + genre + sessions + billboard) =====
with right:
    st.subheader("Taste + engagement")

    # Commit-ment calendar (GitHub-ish)
    st.markdown('### ✅ Your "commit-ment to music"')
    daily = df_f.groupby("date", as_index=False).agg(
        streams=("ts","count"),
        minutes=("ms_played", lambda s: s.sum()/(1000*60))
    )
    daily["value"] = daily["streams"] if measure == "Streams" else daily["minutes"]

    # Build week/day grid
    dts = pd.to_datetime(daily["date"])
    daily["year"] = dts.dt.year
    daily["week"] = dts.dt.isocalendar().week.astype(int)
    daily["dow"] = dts.dt.dayofweek.astype(int)  # Mon=0

    # heatmap needs a full grid for consistent look
    # we show only within selected range
    weeks = sorted(daily["week"].unique().tolist())
    dows = list(range(7))
    grid = pd.MultiIndex.from_product([weeks, dows], names=["week","dow"]).to_frame(index=False)
    daily_h = grid.merge(daily[["week","dow","date","value"]], on=["week","dow"], how="left")

    fig_cal = px.density_heatmap(
        daily_h,
        x="week",
        y="dow",
        z="value",
        nbinsx=len(weeks),
        nbinsy=7,
        color_continuous_scale="Greens",
        hover_data={"date": True, "value": ":.2f", "week": True, "dow": True},
        labels={"week":"Week", "dow":"Day", "value": measure}
    )
    fig_cal.update_yaxes(
        tickvals=list(range(7)),
        ticktext=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        autorange="reversed"
    )
    fig_cal.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_cal, use_container_width=True)
    show_fig(fig_cal, height=280)


    # Genre treemap: bucket -> subgenres (drilldown via selectbox for MVP clarity)
    st.markdown("### 🎨 Genres")

    view_mode = st.radio(
        "View",
        ["Buckets (overview)", "Subgenres (drilldown)"],
        horizontal=True
    )

    df_g = df_f.copy()
    df_g["m"] = measure_value(df_g, measure)

    if view_mode == "Buckets (overview)":
        bucket_agg = (df_g.groupby("genre_bucket", as_index=False)["m"]
                    .sum()
                    .sort_values("m", ascending=False))

        fig_bucket = px.treemap(
            bucket_agg,
            path=["genre_bucket"],
            values="m",
            color="genre_bucket",
            color_discrete_map=GENRE_COLORS
        )
        fig_bucket.update_traces(
            hovertemplate="<b>%{label}</b><br>" + measure + ": %{value:.2f}<extra></extra>"
        )

        show_fig(fig_bucket, height=320)

    else:
        bucket = st.selectbox(
            "Choose bucket",
            sorted(df_g["genre_bucket"].unique().tolist())
        )

        df_sub = df_g[df_g["genre_bucket"] == bucket].copy()

        # Explode comma-separated subgenres
        sub = (df_sub.assign(subgenre=df_sub["artist_genres"].str.split(","))
                    .explode("subgenre"))
        sub["subgenre"] = sub["subgenre"].astype(str).str.strip()
        sub = sub[sub["subgenre"].str.len() > 0]

        sub_agg = (sub.groupby("subgenre", as_index=False)["m"]
                .sum()
                .sort_values("m", ascending=False)
                .head(40))

        fig_sub = px.treemap(
            sub_agg,
            path=["subgenre"],
            values="m",
            color="m",
            color_continuous_scale="Blues"
        )

        # optional: put bucket name in title
        fig_sub.update_layout(title=f"Subgenres inside: {bucket}")

        show_fig(fig_sub, height=320)



    # Session time bins
    st.markdown("### ⏱ Session time")
    gap = st.slider("Session gap threshold (minutes)", 5, 60, 15, 5)
    df_s = sessionize(df_f, gap_minutes=gap)

    sess = df_s.groupby("session_id", as_index=False).agg(
        session_minutes=("session_minutes","first")
    )
    sess["bin"] = sess["session_minutes"].apply(bins_session_minutes)
    sess_bins = sess.groupby("bin", as_index=False).size().rename(columns={"size":"sessions"})
    order = ["<2h","2–4h","4–6h",">6h"]
    sess_bins["bin"] = pd.Categorical(sess_bins["bin"], categories=order, ordered=True)
    sess_bins = sess_bins.sort_values("bin")

    fig_sess = px.bar(sess_bins, x="bin", y="sessions", labels={"bin":"Duration", "sessions":"# Sessions"})
    fig_sess.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_sess, use_container_width=True)
    show_fig(fig_sess, height=260)


    # Billboard
    st.markdown('### 📈 Your personal "Billboard"')
    mode = st.radio("Ranking target", ["Artists", "Songs"], horizontal=True)
    ranking_type = st.radio("Ranking style", ["Accumulated (within range)", "At that time (rolling window)"], horizontal=True)

    if ranking_type == "At that time (rolling window)":
        # slider date within selection
        sel_dates = pd.to_datetime(df_f["date"].unique())
        sel_dates = np.sort(sel_dates)
        if len(sel_dates) == 0:
            st.info("No data in selected range.")
        else:
            d0 = pd.Timestamp(sel_dates[0]).date()
            d1 = pd.Timestamp(sel_dates[-1]).date()

            pivot_date = st.slider("Pick a date", min_value=d0, max_value=d1, value=d1)
            window_days = st.slider("Window size (days)", 7, 180, 30, 7)
            window_start = pivot_date - timedelta(days=window_days)
            subf = df_f[(df_f["date"] >= window_start) & (df_f["date"] <= pivot_date)].copy()
    else:
        subf = df_f.copy()

    subf["m"] = measure_value(subf, measure)

    if mode == "Artists":
        bill = (subf.groupby("master_metadata_album_artist_name", as_index=False)["m"].sum()
                .sort_values("m", ascending=False).head(5))
        fig_bill = px.bar(bill, x="m", y="master_metadata_album_artist_name", orientation="h",
                          labels={"m":measure, "master_metadata_album_artist_name":"Artist"})
    else:
        bill = (subf.groupby(["master_metadata_track_name","master_metadata_album_artist_name"], as_index=False)["m"].sum()
                .sort_values("m", ascending=False).head(5))
        bill["label"] = bill["master_metadata_track_name"] + " — " + bill["master_metadata_album_artist_name"]
        fig_bill = px.bar(bill, x="m", y="label", orientation="h", labels={"m":measure, "label":"Track"})

    fig_bill.update_layout(height=280, margin=dict(l=10,r=10,t=10,b=10))
    #st.plotly_chart(fig_bill, use_container_width=True)
    show_fig(fig_bill, height=280)

st.divider()

# ----------------------------
# Footer: quick interpretation for MVP "message"
# ----------------------------
st.markdown("### Takeaway")
avg_pop = df_f["artist_popularity"].dropna().mean() if df_f["artist_popularity"].notna().any() else np.nan
new_share = df_new_f["is_new_to_you"].mean() if len(df_new_f) else 0

c1, c2, c3 = st.columns(3)
c1.metric("Avg artist popularity", "—" if np.isnan(avg_pop) else f"{avg_pop:.1f}/100")
c2.metric("New-to-you share", f"{new_share*100:.1f}%")
c3.metric("Skip rate", f"{(df_f['skipped'].mean()*100):.1f}%")
