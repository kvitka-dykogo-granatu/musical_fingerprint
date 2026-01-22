"""
Musical Fingerprint - Spotify Listening Dashboard
A beautifully styled dashboard showing your unique listening patterns
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, datetime, date

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Musical Fingerprint",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Spotify-Inspired Design System
# ----------------------------
SPOTIFY = {
    "bg_dark": "#121212",
    "bg_card": "#181818",
    "bg_elevated": "#282828",
    "bg_highlight": "#333333",
    "green": "#1DB954",
    "green_light": "#1ed760",
    "white": "#FFFFFF",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B3B3B3",
    "text_muted": "#727272",
    "border": "#404040",
}

GENRE_COLORS = {
    "EDM & Progressive": "#1DB954",
    "Trance": "#8B5CF6",
    "Electronica / Chill": "#06B6D4",
    "Lo-Fi / Chillhop": "#F59E0B",
    "Pop & Regional Pop": "#EC4899",
    "Rock / Metal / Core": "#EF4444",
    "Folk / Acoustic / Celtic": "#22C55E",
    "Hip-Hop / Rap": "#F97316",
    "Soundtrack / Score / Musicals": "#3B82F6",
    "Others": "#6B7280",
}

# ----------------------------
# Custom CSS - Spotify Dark Theme
# ----------------------------
st.markdown(f"""
<style>
    /* Import Spotify-like fonts */
    @import url('https://fonts.googleapis.com/css2?family=Circular+Std:wght@400;500;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* Global styles */
    .stApp {{
        background: linear-gradient(180deg, {SPOTIFY["bg_dark"]} 0%, #0a0a0a 100%);
    }}
    
    .main .block-container {{
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1600px;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu, footer {{visibility: hidden;}}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'DM Sans', 'Circular Std', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: {SPOTIFY["white"]} !important;
        letter-spacing: -0.02em;
    }}
    
    p, span, div {{
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Header styling */
    .dashboard-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }}
    
    .fingerprint-icon {{
        font-size: 48px;
        filter: drop-shadow(0 0 20px {SPOTIFY["green"]}40);
    }}
    
    .dashboard-title {{
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, {SPOTIFY["white"]} 0%, {SPOTIFY["green"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.1;
    }}
    
    .dashboard-subtitle {{
        color: {SPOTIFY["text_secondary"]};
        font-size: 0.95rem;
        margin-top: 4px;
    }}
    
    /* KPI Cards */
    .kpi-container {{
        display: flex;
        gap: 12px;
        margin: 16px 0;
        flex-wrap: wrap;
    }}
    
    .kpi-card {{
        background: linear-gradient(145deg, {SPOTIFY["bg_card"]} 0%, {SPOTIFY["bg_elevated"]} 100%);
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 16px 20px;
        flex: 1;
        min-width: 140px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    .kpi-card:hover {{
        border-color: {SPOTIFY["green"]};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.15);
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {SPOTIFY["green"]} 0%, {SPOTIFY["green_light"]} 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .kpi-card:hover::before {{
        opacity: 1;
    }}
    
    .kpi-label {{
        font-size: 0.75rem;
        color: {SPOTIFY["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }}
    
    .kpi-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {SPOTIFY["white"]};
        line-height: 1;
    }}
    
    .kpi-trend {{
        font-size: 0.75rem;
        color: {SPOTIFY["green"]};
        margin-top: 6px;
    }}
    
    /* Section Cards */
    .section-card {{
        background: {SPOTIFY["bg_card"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }}
    
    .section-card:hover {{
        border-color: {SPOTIFY["bg_highlight"]};
    }}
    
    .section-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {SPOTIFY["white"]};
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .section-title-icon {{
        font-size: 1.2rem;
    }}
    
    /* Top Item Cards */
    .top-item-card {{
        background: linear-gradient(135deg, {SPOTIFY["bg_elevated"]} 0%, {SPOTIFY["bg_card"]} 100%);
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.2s ease;
    }}
    
    .top-item-card:hover {{
        border-color: {SPOTIFY["green"]};
        background: linear-gradient(135deg, {SPOTIFY["bg_highlight"]} 0%, {SPOTIFY["bg_elevated"]} 100%);
    }}
    
    .top-item-rank {{
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, {SPOTIFY["green"]} 0%, {SPOTIFY["green_light"]} 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        color: {SPOTIFY["bg_dark"]};
        flex-shrink: 0;
    }}
    
    .top-item-info {{
        flex: 1;
        min-width: 0;
    }}
    
    .top-item-name {{
        font-weight: 600;
        color: {SPOTIFY["white"]};
        font-size: 0.95rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    .top-item-sub {{
        font-size: 0.8rem;
        color: {SPOTIFY["text_muted"]};
        margin-top: 2px;
    }}
    
    .top-item-stat {{
        font-weight: 700;
        color: {SPOTIFY["green"]};
        font-size: 0.9rem;
        flex-shrink: 0;
    }}
    
    /* Play button style */
    .play-icon {{
        width: 32px;
        height: 32px;
        background: {SPOTIFY["green"]};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    
    /* Filter pills */
    .filter-container {{
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }}
    
    .filter-pill {{
        background: {SPOTIFY["bg_elevated"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.8rem;
        color: {SPOTIFY["text_secondary"]};
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .filter-pill:hover, .filter-pill.active {{
        background: {SPOTIFY["green"]};
        color: {SPOTIFY["bg_dark"]};
        border-color: {SPOTIFY["green"]};
    }}
    
    /* Commitment calendar legend */
    .calendar-legend {{
        display: flex;
        align-items: center;
        gap: 4px;
        justify-content: flex-end;
        margin-top: 8px;
        font-size: 0.7rem;
        color: {SPOTIFY["text_muted"]};
    }}
    
    .legend-box {{
        width: 12px;
        height: 12px;
        border-radius: 2px;
    }}
    
    /* Billboard table */
    .billboard-item {{
        display: flex;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid {SPOTIFY["border"]}20;
        gap: 12px;
    }}
    
    .billboard-item:last-child {{
        border-bottom: none;
    }}
    
    .billboard-rank {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {SPOTIFY["text_muted"]};
        width: 24px;
        text-align: center;
    }}
    
    .billboard-bar {{
        flex: 1;
        height: 8px;
        background: {SPOTIFY["bg_highlight"]};
        border-radius: 4px;
        overflow: hidden;
    }}
    
    .billboard-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, {SPOTIFY["green"]} 0%, {SPOTIFY["green_light"]} 100%);
        border-radius: 4px;
    }}
    
    .billboard-name {{
        flex: 2;
        font-size: 0.85rem;
        color: {SPOTIFY["white"]};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    .billboard-value {{
        font-size: 0.8rem;
        color: {SPOTIFY["text_secondary"]};
        width: 60px;
        text-align: right;
    }}
    
    /* Plotly chart containers */
    .chart-container {{
        background: {SPOTIFY["bg_card"]};
        border-radius: 12px;
        padding: 16px;
        border: 1px solid {SPOTIFY["border"]};
    }}
    
    /* Streamlit component overrides */
    .stSelectbox > div > div {{
        background: {SPOTIFY["bg_elevated"]};
        border-color: {SPOTIFY["border"]};
        color: {SPOTIFY["white"]};
    }}
    
    .stRadio > div {{
        gap: 8px;
    }}
    
    .stRadio > div > label {{
        background: {SPOTIFY["bg_elevated"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 20px;
        padding: 6px 14px;
        color: {SPOTIFY["text_secondary"]};
        transition: all 0.2s ease;
    }}
    
    .stRadio > div > label:hover {{
        border-color: {SPOTIFY["green"]};
    }}
    
    .stRadio > div > label[data-checked="true"] {{
        background: {SPOTIFY["green"]};
        color: {SPOTIFY["bg_dark"]};
        border-color: {SPOTIFY["green"]};
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {SPOTIFY["border"]}, transparent);
        margin: 20px 0;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: {SPOTIFY["bg_card"]};
        border-right: 1px solid {SPOTIFY["border"]};
    }}
    
    section[data-testid="stSidebar"] .stRadio > label {{
        color: {SPOTIFY["white"]};
    }}
    
    /* Metric delta colors */
    [data-testid="stMetricDelta"] svg {{
        stroke: {SPOTIFY["green"]};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: {SPOTIFY["bg_elevated"]} !important;
        border-radius: 8px !important;
        color: {SPOTIFY["white"]} !important;
    }}
    
    /* Tooltip styling for charts */
    .js-plotly-plot .plotly .hoverlayer {{
        font-family: 'DM Sans', sans-serif !important;
    }}
    
    /* Slider */
    .stSlider > div > div > div {{
        background: {SPOTIFY["green"]} !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {SPOTIFY["bg_elevated"]};
        border-radius: 8px;
        color: {SPOTIFY["text_secondary"]};
        padding: 8px 16px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {SPOTIFY["green"]} !important;
        color: {SPOTIFY["bg_dark"]} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper Functions
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


def style_fig(fig, height=300, show_legend=True):
    """Apply Spotify-inspired styling to Plotly figures"""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=SPOTIFY["text_secondary"],
            family="DM Sans, -apple-system, BlinkMacSystemFont, sans-serif",
            size=12
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(
            font=dict(size=14, color=SPOTIFY["white"]),
            x=0,
            xanchor="left"
        ),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=SPOTIFY["text_secondary"])
        ),
        hoverlabel=dict(
            bgcolor=SPOTIFY["bg_elevated"],
            font_size=12,
            font_family="DM Sans",
            bordercolor=SPOTIFY["border"]
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(64, 64, 64, 0.25)",
        zeroline=False,
        showline=False,
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(64, 64, 64, 0.25)",
        zeroline=False,
        showline=False,
        tickfont=dict(size=10)
    )
    return fig


@st.cache_data(show_spinner=False)
def load_csv(uploaded_file=None, path=None) -> pd.DataFrame:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif path is not None:
        df = pd.read_csv(path)
    else:
        return pd.DataFrame()

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df.copy()
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts"])
    df["ms_played"] = pd.to_numeric(df["ms_played"], errors="coerce").fillna(0).astype(int)
    df["skipped"] = df["skipped"].apply(_to_bool)
    df["artist_popularity"] = pd.to_numeric(df["artist_popularity"], errors="coerce").fillna(np.nan)
    
    # Time helpers
    df["date"] = df["ts"].dt.date
    df["year"] = df["ts"].dt.year
    df["month"] = df["ts"].dt.to_period("M").astype(str)
    df["dow"] = df["ts"].dt.dayofweek
    df["hour"] = df["ts"].dt.hour
    df["start_ts"] = df["ts"] - pd.to_timedelta(df["ms_played"], unit="ms")
    
    if "track_id" not in df.columns:
        df["track_id"] = (df["master_metadata_album_artist_name"].astype(str) + "§" +
                          df["master_metadata_track_name"].astype(str))
    
    for c in ["master_metadata_track_name", "master_metadata_album_artist_name",
              "master_metadata_album_album_name", "genre_bucket", "artist_genres"]:
        df[c] = df[c].astype(str).fillna("")
    
    return df


DEMO_PATH = "music_data.csv"

@st.cache_data(show_spinner=False)
def load_demo_file() -> pd.DataFrame:
    return load_csv(path=DEMO_PATH)


def measure_value(df: pd.DataFrame, measure: str) -> pd.Series:
    if measure == "Streams":
        return pd.Series(np.ones(len(df), dtype=float), index=df.index)
    return df["ms_played"] / (1000 * 60)


def fmt_number(n):
    """Format large numbers nicely"""
    try:
        if abs(n) >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if abs(n) >= 1_000:
            return f"{n/1_000:.1f}K"
        if isinstance(n, float) and not n.is_integer():
            return f"{n:.1f}"
        return f"{int(n):,}"
    except:
        return str(n)


@st.cache_data(show_spinner=False)
def compute_first_listen_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Mark first-time listens for each track"""
    first_ts = df.groupby("track_id")["ts"].min()
    df = df.copy()
    df["first_listen_ts"] = df["track_id"].map(first_ts)
    df["is_new_to_you"] = df["ts"] == df["first_listen_ts"]
    return df


@st.cache_data(show_spinner=False)
def compute_old_vs_new_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    FIXED: Count unique songs per month that are new vs old.
    A song is "new" in a month if its first-ever listen was in that month.
    A song is "old" if it was first listened to in a previous month.
    Each song counts ONCE per month regardless of replays.
    """
    df = df.copy()
    
    # Get first listen timestamp for each track
    first_listen = df.groupby("track_id")["ts"].min().reset_index()
    first_listen.columns = ["track_id", "first_listen_ts"]
    first_listen["first_listen_month"] = pd.to_datetime(first_listen["first_listen_ts"]).dt.to_period("M").astype(str)
    
    # Get unique track-month combinations
    track_months = df.groupby(["month", "track_id"]).size().reset_index(name="play_count")
    track_months = track_months.merge(first_listen[["track_id", "first_listen_month"]], on="track_id")
    
    # A track is "new" in a month if that month equals the first listen month
    track_months["is_new"] = track_months["month"] == track_months["first_listen_month"]
    
    # Count unique tracks per month by new/old status
    monthly_counts = track_months.groupby(["month", "is_new"]).agg(
        unique_tracks=("track_id", "nunique")
    ).reset_index()
    
    pivot = monthly_counts.pivot(index="month", columns="is_new", values="unique_tracks").fillna(0)
    pivot.columns = ["Old tracks", "New tracks"] if list(pivot.columns) == [False, True] else [str(c) for c in pivot.columns]
    pivot = pivot.reset_index()
    
    return pivot


@st.cache_data(show_spinner=False)
def sessionize(df: pd.DataFrame, gap_minutes=15) -> pd.DataFrame:
    """Group plays into sessions based on time gaps"""
    d = df.sort_values("start_ts").copy()
    gap = pd.Timedelta(minutes=gap_minutes)
    prev_end = d["ts"].shift(1)
    new_session = (d["start_ts"] - prev_end) > gap
    d["session_id"] = new_session.cumsum().fillna(0).astype(int)
    session_len = d.groupby("session_id")["ms_played"].sum() / (1000 * 60)
    d["session_minutes"] = d["session_id"].map(session_len)
    return d


def bins_session_minutes(x):
    if x < 120: return "<2h"
    if x < 240: return "2–4h"
    if x < 360: return "4–6h"
    return ">6h"


# ----------------------------
# Sidebar Controls
# ----------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <span style="font-size: 40px;">🎧</span>
        <h2 style="margin: 10px 0 5px 0; color: {SPOTIFY['white']};">Controls</h2>
    </div>
    """, unsafe_allow_html=True)
    
    use_demo = st.toggle("Use included dataset", value=True)
    
    uploaded = None
    if not use_demo:
        uploaded = st.file_uploader("Upload your Spotify CSV", type=["csv"])
    
    st.divider()
    
    measure = st.radio("📊 Measure", ["Streams", "Minutes"], horizontal=True)
    
    st.divider()
    
    st.markdown(f"<p style='color: {SPOTIFY['text_muted']}; font-size: 0.8rem;'>Tip: Toggle the sidebar with the arrow on desktop, or swipe on mobile.</p>", unsafe_allow_html=True)

# ----------------------------
# Load Data
# ----------------------------
try:
    if use_demo:
        df = load_demo_file()
    else:
        if uploaded is None:
            st.info("👈 Upload your CSV in the sidebar or enable 'Use included dataset'")
            st.stop()
        df = load_csv(uploaded_file=uploaded)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# ----------------------------
# Header
# ----------------------------
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown(f"""
    <div class="dashboard-header">
        <span class="fingerprint-icon">🎧</span>
        <div>
            <h1 class="dashboard-title">Musical Fingerprint</h1>
            <p class="dashboard-subtitle">Your unique listening DNA — patterns, genres, discoveries & obsessions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    # Date filter in header for prominence
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

# Filter data
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_f = df.loc[mask].copy()
df_new = compute_first_listen_flags(df)
df_new_f = df_new.loc[mask].copy()

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------
# KPI Row
# ----------------------------
total_streams = len(df_f)
total_minutes = df_f["ms_played"].sum() / (1000 * 60)
total_hours = total_minutes / 60
n_tracks = df_f["master_metadata_track_name"].nunique()
n_artists = df_f["master_metadata_album_artist_name"].nunique()
n_albums = df_f["master_metadata_album_album_name"].nunique()

# Calculate discovery stats
new_tracks_count = df_new_f["is_new_to_you"].sum()
discovery_pct = (new_tracks_count / len(df_new_f) * 100) if len(df_new_f) > 0 else 0

# Avg skip time for skipped tracks
avg_skip_time = df_f[df_f["skipped"]]["ms_played"].mean() / 1000 if df_f["skipped"].any() else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Total Streams</div>
        <div class="kpi-value">{fmt_number(total_streams)}</div>
        <div class="kpi-trend">plays in range</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Hours Listened</div>
        <div class="kpi-value">{total_hours:,.1f}</div>
        <div class="kpi-trend">{total_minutes:,.0f} minutes total</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Unique Tracks</div>
        <div class="kpi-value">{fmt_number(n_tracks)}</div>
        <div class="kpi-trend">different songs</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Unique Artists</div>
        <div class="kpi-value">{fmt_number(n_artists)}</div>
        <div class="kpi-trend">discovered</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Albums</div>
        <div class="kpi-value">{fmt_number(n_albums)}</div>
        <div class="kpi-trend">explored</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Skip Time</div>
        <div class="kpi-value">{avg_skip_time:.1f}s</div>
        <div class="kpi-trend">avg before skip</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Main Dashboard Grid
# ----------------------------

# Row 1: Top Artist + Top Track + Commitment Calendar
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">👑</span> No.1 Artist</div>', unsafe_allow_html=True)
    
    top_artist = (
        df_f.groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )
    
    if len(top_artist) > 0:
        artist_name = top_artist.index[0]
        artist_streams = df_f[df_f['master_metadata_album_artist_name'] == artist_name].shape[0]
        artist_mins = top_artist.iloc[0] / (1000 * 60)
        
        st.markdown(f"""
        <div class="top-item-card">
            <div class="play-icon">▶</div>
            <div class="top-item-info">
                <div class="top-item-name">{artist_name}</div>
                <div class="top-item-sub">{artist_streams:,} streams • {artist_mins:,.0f} min</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No data")

with col2:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">🎵</span> No.1 Track</div>', unsafe_allow_html=True)
    
    top_track = (
        df_f.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"])["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )
    
    if len(top_track) > 0:
        (track_name, track_artist) = top_track.index[0]
        track_streams = df_f[(df_f['master_metadata_track_name'] == track_name) & 
                            (df_f['master_metadata_album_artist_name'] == track_artist)].shape[0]
        track_mins = top_track.iloc[0] / (1000 * 60)
        
        st.markdown(f"""
        <div class="top-item-card">
            <div class="play-icon">▶</div>
            <div class="top-item-info">
                <div class="top-item-name">{track_name}</div>
                <div class="top-item-sub">{track_artist} • {track_streams} plays</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No data")

with col3:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">📅</span> Your "Commit"-ment to Music</div>', unsafe_allow_html=True)
    
    daily = df_f.groupby("date", as_index=False).agg(
        streams=("ts", "count"),
        minutes=("ms_played", lambda s: s.sum()/(1000*60))
    )
    daily["value"] = daily["streams"] if measure == "Streams" else daily["minutes"]
    
    dts = pd.to_datetime(daily["date"])
    daily["week"] = dts.dt.isocalendar().week.astype(int)
    daily["dow"] = dts.dt.dayofweek.astype(int)
    daily["year_week"] = dts.dt.strftime("%Y-W%W")
    
    fig_cal = px.density_heatmap(
        daily,
        x="year_week",
        y="dow",
        z="value",
        color_continuous_scale=[
            [0, SPOTIFY["bg_elevated"]],
            [0.25, "#0d4429"],
            [0.5, "#166534"],
            [0.75, "#22c55e"],
            [1, SPOTIFY["green_light"]]
        ],
        labels={"year_week": "", "dow": "", "value": measure}
    )
    fig_cal.update_yaxes(
        tickvals=list(range(7)),
        ticktext=["M", "T", "W", "T", "F", "S", "S"],
        autorange="reversed"
    )
    fig_cal.update_xaxes(tickangle=45, nticks=15)
    fig_cal.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_cal, height=180, show_legend=False), use_container_width=True)

# Row 2: Listening Clock + Old vs New + Genre Treemap
col1, col2, col3 = st.columns([1, 1.2, 1.3])

with col1:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">🕐</span> Listening Clock</div>', unsafe_allow_html=True)
    
    by_hour = df_f.copy()
    by_hour["m"] = measure_value(by_hour, measure)
    hour_agg = by_hour.groupby("hour", as_index=False)["m"].sum()
    
    # Fill missing hours
    all_hours = pd.DataFrame({"hour": range(24)})
    hour_agg = all_hours.merge(hour_agg, on="hour", how="left").fillna(0)
    
    fig_clock = go.Figure()
    fig_clock.add_trace(go.Barpolar(
        r=hour_agg["m"],
        theta=hour_agg["hour"] * 15,
        width=[14]*24,
        marker_color=SPOTIFY["green"],
        marker_line_color=SPOTIFY["green_light"],
        marker_line_width=1,
        opacity=0.85,
        hovertemplate="Hour %{customdata}:00<br>%{r:.0f} " + measure.lower() + "<extra></extra>",
        customdata=hour_agg["hour"]
    ))
    fig_clock.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                showticklabels=False,
                showline=False,
                gridcolor="rgba(64, 64, 64, 0.25)"
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickmode="array",
                tickvals=[i*15 for i in range(0, 24, 3)],
                ticktext=[f"{i}" for i in range(0, 24, 3)],
                tickfont=dict(size=10, color=SPOTIFY["text_muted"]),
                gridcolor="rgba(64, 64, 64, 0.25)"
            )
        ),
        showlegend=False
    )
    st.plotly_chart(style_fig(fig_clock, height=260, show_legend=False), use_container_width=True)

with col2:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">🆕</span> Discovery: Old vs New Tracks</div>', unsafe_allow_html=True)
    st.caption("Unique songs per month (first listen = new, revisits = old)")
    
    old_new_data = compute_old_vs_new_monthly(df_new_f)
    
    if len(old_new_data) > 0:
        fig_oldnew = go.Figure()
        
        if "Old tracks" in old_new_data.columns:
            fig_oldnew.add_trace(go.Scatter(
                x=old_new_data["month"],
                y=old_new_data["Old tracks"],
                mode="lines+markers",
                name="Old (revisited)",
                line=dict(color=SPOTIFY["text_muted"], width=2),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(114, 114, 114, 0.12)"
            ))
        
        if "New tracks" in old_new_data.columns:
            fig_oldnew.add_trace(go.Scatter(
                x=old_new_data["month"],
                y=old_new_data["New tracks"],
                mode="lines+markers",
                name="New (discoveries)",
                line=dict(color=SPOTIFY["green"], width=2),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(29, 185, 84, 0.18)"
            ))
        
        fig_oldnew.update_layout(
            xaxis_title="",
            yaxis_title="Unique tracks",
            hovermode="x unified"
        )
        st.plotly_chart(style_fig(fig_oldnew, height=240), use_container_width=True)
    else:
        st.info("Not enough data for this chart")

with col3:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">🎨</span> Top Genres</div>', unsafe_allow_html=True)
    
    df_g = df_f.copy()
    df_g["m"] = measure_value(df_g, measure)
    bucket_agg = (df_g.groupby("genre_bucket", as_index=False)["m"]
                .sum()
                .sort_values("m", ascending=False))
    
    fig_genre = px.treemap(
        bucket_agg,
        path=["genre_bucket"],
        values="m",
        color="genre_bucket",
        color_discrete_map=GENRE_COLORS
    )
    fig_genre.update_traces(
        hovertemplate="<b>%{label}</b><br>" + measure + ": %{value:,.0f}<extra></extra>",
        textinfo="label+percent root",
        textfont=dict(size=12)
    )
    fig_genre.update_layout(margin=dict(l=5, r=5, t=5, b=5))
    st.plotly_chart(style_fig(fig_genre, height=280, show_legend=False), use_container_width=True)

# Row 3: Niche Scatter + Session Time + Billboard
col1, col2, col3 = st.columns([1.3, 0.8, 1.4])

with col1:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">🎯</span> How Niche is Your Taste?</div>', unsafe_allow_html=True)
    st.caption("X = Artist popularity (Spotify 0-100), Y = Your listening volume")
    
    tmp3 = df_f.copy()
    tmp3["m"] = measure_value(tmp3, measure)
    artist_agg = (tmp3.groupby(["master_metadata_album_artist_name", "artist_popularity"], as_index=False)
                  .agg(total=("m", "sum"), streams=("ts", "count")))
    artist_agg = artist_agg.dropna(subset=["artist_popularity"])
    
    fig_niche = px.scatter(
        artist_agg,
        x="artist_popularity",
        y="total",
        size="streams",
        size_max=25,
        hover_name="master_metadata_album_artist_name",
        labels={"artist_popularity": "Artist Popularity", "total": f"Your {measure}"},
        color_discrete_sequence=[SPOTIFY["green"]]
    )
    fig_niche.update_traces(
        marker=dict(
            line=dict(width=1, color=SPOTIFY["green_light"]),
            opacity=0.7
        )
    )
    
    # Add quadrant lines
    fig_niche.add_hline(y=artist_agg["total"].median(), line_dash="dash", line_color=SPOTIFY["border"], opacity=0.5)
    fig_niche.add_vline(x=50, line_dash="dash", line_color=SPOTIFY["border"], opacity=0.5)
    
    # Add annotations
    fig_niche.add_annotation(x=25, y=artist_agg["total"].max() * 0.9, text="Niche favorites", 
                            showarrow=False, font=dict(size=9, color=SPOTIFY["text_muted"]))
    fig_niche.add_annotation(x=75, y=artist_agg["total"].max() * 0.9, text="Mainstream favorites",
                            showarrow=False, font=dict(size=9, color=SPOTIFY["text_muted"]))
    
    st.plotly_chart(style_fig(fig_niche, height=280, show_legend=False), use_container_width=True)

with col2:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">⏱️</span> Session Duration</div>', unsafe_allow_html=True)
    
    df_s = sessionize(df_f, gap_minutes=15)
    sess = df_s.groupby("session_id", as_index=False).agg(session_minutes=("session_minutes", "first"))
    sess["bin"] = sess["session_minutes"].apply(bins_session_minutes)
    sess_bins = sess.groupby("bin", as_index=False).size().rename(columns={"size": "sessions"})
    
    order = ["<2h", "2–4h", "4–6h", ">6h"]
    sess_bins["bin"] = pd.Categorical(sess_bins["bin"], categories=order, ordered=True)
    sess_bins = sess_bins.sort_values("bin")
    
    fig_sess = px.bar(
        sess_bins,
        x="bin",
        y="sessions",
        labels={"bin": "", "sessions": "Sessions"},
        color_discrete_sequence=[SPOTIFY["green"]]
    )
    fig_sess.update_traces(
        marker_line_color=SPOTIFY["green_light"],
        marker_line_width=1
    )
    st.plotly_chart(style_fig(fig_sess, height=280, show_legend=False), use_container_width=True)

with col3:
    st.markdown(f'<div class="section-title"><span class="section-title-icon">📈</span> Your Personal Billboard</div>', unsafe_allow_html=True)
    
    bill_tabs = st.tabs(["🎤 Top Artists", "🎵 Top Songs"])
    
    with bill_tabs[0]:
        subf = df_f.copy()
        subf["m"] = measure_value(subf, measure)
        bill_artists = (subf.groupby("master_metadata_album_artist_name", as_index=False)["m"]
                       .sum()
                       .sort_values("m", ascending=False)
                       .head(5))
        
        max_val = bill_artists["m"].max() if len(bill_artists) > 0 else 1
        
        billboard_html = ""
        for i, row in bill_artists.iterrows():
            pct = (row["m"] / max_val) * 100
            rank = bill_artists.index.get_loc(i) + 1
            billboard_html += f"""
            <div class="billboard-item">
                <span class="billboard-rank">{rank}</span>
                <span class="billboard-name">{row['master_metadata_album_artist_name']}</span>
                <div class="billboard-bar">
                    <div class="billboard-bar-fill" style="width: {pct}%;"></div>
                </div>
                <span class="billboard-value">{fmt_number(row['m'])}</span>
            </div>
            """
        
        st.markdown(billboard_html, unsafe_allow_html=True)
    
    with bill_tabs[1]:
        bill_songs = (subf.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], as_index=False)["m"]
                     .sum()
                     .sort_values("m", ascending=False)
                     .head(5))
        
        max_val = bill_songs["m"].max() if len(bill_songs) > 0 else 1
        
        billboard_html = ""
        for i, row in bill_songs.iterrows():
            pct = (row["m"] / max_val) * 100
            rank = bill_songs.index.get_loc(i) + 1
            display_name = f"{row['master_metadata_track_name'][:25]}..." if len(row['master_metadata_track_name']) > 25 else row['master_metadata_track_name']
            billboard_html += f"""
            <div class="billboard-item">
                <span class="billboard-rank">{rank}</span>
                <span class="billboard-name" title="{row['master_metadata_track_name']} - {row['master_metadata_album_artist_name']}">{display_name}</span>
                <div class="billboard-bar">
                    <div class="billboard-bar-fill" style="width: {pct}%;"></div>
                </div>
                <span class="billboard-value">{fmt_number(row['m'])}</span>
            </div>
            """
        
        st.markdown(billboard_html, unsafe_allow_html=True)

# ----------------------------
# Row 4: Additional Insights (collapsible)
# ----------------------------
st.markdown("<hr>", unsafe_allow_html=True)

with st.expander("🌞 Deep Dive: Artist → Track Sunburst & More", expanded=False):
    sun_col, drilldown_col = st.columns(2)
    
    with sun_col:
        st.markdown("#### Top 3 Artists → Their Top Tracks")
        
        tmp2 = df_f.copy()
        tmp2["m"] = measure_value(tmp2, measure)
        top3_art = tmp2.groupby("master_metadata_album_artist_name")["m"].sum().sort_values(ascending=False).head(3).index
        tmp2 = tmp2[tmp2["master_metadata_album_artist_name"].isin(top3_art)].copy()
        
        track_rank = (tmp2.groupby(["master_metadata_album_artist_name", "master_metadata_track_name"])["m"]
                      .sum()
                      .reset_index()
                      .sort_values(["master_metadata_album_artist_name", "m"], ascending=[True, False]))
        track_rank["rk"] = track_rank.groupby("master_metadata_album_artist_name").cumcount() + 1
        keep_tracks = track_rank[track_rank["rk"] <= 4][["master_metadata_album_artist_name", "master_metadata_track_name"]]
        tmp2 = tmp2.merge(keep_tracks, on=["master_metadata_album_artist_name", "master_metadata_track_name"], how="inner")
        
        sun = tmp2.groupby(["master_metadata_album_artist_name", "master_metadata_track_name"], as_index=False)["m"].sum()
        
        fig_sun = px.sunburst(
            sun,
            path=["master_metadata_album_artist_name", "master_metadata_track_name"],
            values="m",
            color="master_metadata_album_artist_name",
            color_discrete_sequence=[SPOTIFY["green"], "#22d3ee", "#f97316"]
        )
        fig_sun.update_traces(
            textinfo="label",
            insidetextorientation="radial"
        )
        st.plotly_chart(style_fig(fig_sun, height=350, show_legend=False), use_container_width=True)
    
    with drilldown_col:
        st.markdown("#### Genre Drilldown: Subgenres")
        
        bucket = st.selectbox(
            "Select a genre bucket to explore",
            sorted(df_f["genre_bucket"].unique().tolist())
        )
        
        df_sub = df_f[df_f["genre_bucket"] == bucket].copy()
        df_sub["m"] = measure_value(df_sub, measure)
        
        sub = (df_sub.assign(subgenre=df_sub["artist_genres"].str.split(","))
               .explode("subgenre"))
        sub["subgenre"] = sub["subgenre"].astype(str).str.strip()
        sub = sub[sub["subgenre"].str.len() > 0]
        
        sub_agg = (sub.groupby("subgenre", as_index=False)["m"]
                   .sum()
                   .sort_values("m", ascending=False)
                   .head(12))
        
        fig_sub = px.bar(
            sub_agg,
            x="m",
            y="subgenre",
            orientation="h",
            labels={"m": measure, "subgenre": ""},
            color_discrete_sequence=[GENRE_COLORS.get(bucket, SPOTIFY["green"])]
        )
        fig_sub.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(style_fig(fig_sub, height=350, show_legend=False), use_container_width=True)

# ----------------------------
# Footer: Takeaway Stats
# ----------------------------
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(f'<div class="section-title"><span class="section-title-icon">💡</span> Key Takeaways</div>', unsafe_allow_html=True)

take_col1, take_col2, take_col3, take_col4 = st.columns(4)

avg_pop = df_f["artist_popularity"].dropna().mean() if df_f["artist_popularity"].notna().any() else np.nan
new_share = df_new_f["is_new_to_you"].mean() * 100 if len(df_new_f) else 0
skip_rate = df_f["skipped"].mean() * 100 if len(df_f) > 0 else 0

# Peak listening hour
peak_hour = hour_agg.loc[hour_agg["m"].idxmax(), "hour"] if len(hour_agg) > 0 else 0

with take_col1:
    taste_desc = "Mainstream" if avg_pop > 60 else ("Balanced" if avg_pop > 40 else "Indie/Niche")
    st.metric("🎯 Avg Artist Popularity", f"{avg_pop:.0f}/100" if not np.isnan(avg_pop) else "—", taste_desc)

with take_col2:
    discovery_desc = "Explorer!" if new_share > 30 else ("Balanced" if new_share > 15 else "Comfort zone")
    st.metric("🆕 Discovery Rate", f"{new_share:.1f}%", discovery_desc)

with take_col3:
    skip_desc = "Picky listener" if skip_rate > 20 else ("Average" if skip_rate > 10 else "Committed")
    st.metric("⏭️ Skip Rate", f"{skip_rate:.1f}%", skip_desc)

with take_col4:
    hour_desc = "Night owl 🦉" if peak_hour >= 22 or peak_hour < 6 else ("Morning person 🌅" if peak_hour < 12 else "Afternoon vibes ☀️")
    st.metric("🕐 Peak Hour", f"{int(peak_hour):02d}:00", hour_desc)

# Footer
st.markdown(f"""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: {SPOTIFY['text_muted']}; font-size: 0.8rem;">
    <p>Made with 💚 using Streamlit • Data from your Spotify listening history</p>
    <p style="margin-top: 8px;">🎧 Musical Fingerprint — Your unique listening DNA</p>
</div>
""", unsafe_allow_html=True)
