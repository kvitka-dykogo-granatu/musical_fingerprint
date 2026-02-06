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
# Design System
# ----------------------------
SPOTIFY = {
    "bg_dark": "#121212",
    "bg_card": "#181818",
    "bg_elevated": "#282828",
    "bg_highlight": "#333333",
    "green": "#1DB954",
    "green_light": "#1ed760",
    "green_dim": "#0d4429",
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
    "Folk / Acoustic / Celtic": "#2D6A4F",
    "Hip-Hop / Rap": "#F97316",
    "Soundtrack / Score / Musicals": "#3B82F6",
    "Others": "#6B7280",
}

# Ordered for consistent stacking — maximise contrast between adjacent colors
GENRE_ORDER = [
    "EDM & Progressive", "Rock / Metal / Core", "Lo-Fi / Chillhop",
    "Soundtrack / Score / Musicals", "Pop & Regional Pop", "Folk / Acoustic / Celtic",
    "Hip-Hop / Rap", "Trance", "Electronica / Chill", "Others",
]

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp {{
        background: linear-gradient(180deg, {SPOTIFY["bg_dark"]} 0%, #0a0a0a 100%);
    }}
    
    .main .block-container {{
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1600px;
    }}
    
    #MainMenu, footer {{visibility: hidden;}}
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {SPOTIFY["white"]} !important;
        letter-spacing: -0.02em;
    }}
    
    /* ---- Header ---- */
    .dashboard-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }}
    .fingerprint-icon {{
        font-size: 48px;
        filter: drop-shadow(0 0 20px rgba(29, 185, 84, 0.4));
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
    
    /* ---- KPI Cards ---- */
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
        min-width: 120px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    .kpi-card:hover {{
        border-color: {SPOTIFY["green"]};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.15);
    }}
    .kpi-label {{
        font-size: 0.7rem;
        color: {SPOTIFY["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {SPOTIFY["white"]};
        line-height: 1;
    }}
    .kpi-trend {{
        font-size: 0.7rem;
        color: {SPOTIFY["text_muted"]};
        margin-top: 4px;
    }}
    .kpi-accent {{
        color: {SPOTIFY["green"]};
    }}
    
    /* ---- Section header ---- */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }}
    .section-title {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {SPOTIFY["white"]};
        margin: 0;
    }}
    
    /* ---- Top-item cards ---- */
    .top-item-card {{
        background: linear-gradient(135deg, {SPOTIFY["bg_elevated"]} 0%, {SPOTIFY["bg_card"]} 100%);
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s ease;
        margin-bottom: 8px;
    }}
    .top-item-card:hover {{ border-color: {SPOTIFY["green"]}; }}
    .rank-badge {{
        width: 36px; height: 36px;
        background: {SPOTIFY["green"]};
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: {SPOTIFY["bg_dark"]}; font-size: 14px; font-weight: 700;
        flex-shrink: 0;
    }}
    .top-item-name {{
        font-weight: 600; color: {SPOTIFY["white"]}; font-size: 0.9rem;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    .top-item-sub {{
        font-size: 0.75rem; color: {SPOTIFY["text_muted"]}; margin-top: 2px;
    }}
    
    /* ---- Billboard ---- */
    .billboard-item {{
        display: flex; align-items: center; padding: 8px 0;
        border-bottom: 1px solid rgba(64,64,64,0.2); gap: 10px;
    }}
    .billboard-item:last-child {{ border-bottom: none; }}
    .billboard-rank {{
        font-size: 1rem; font-weight: 700; color: {SPOTIFY["text_muted"]};
        width: 20px; text-align: center;
        font-family: 'JetBrains Mono', monospace !important;
    }}
    .billboard-name {{
        flex: 1; font-size: 0.8rem; color: {SPOTIFY["white"]};
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;
    }}
    .billboard-bar {{
        width: 60px; height: 6px; background: {SPOTIFY["bg_highlight"]};
        border-radius: 3px; overflow: hidden; flex-shrink: 0;
    }}
    .billboard-bar-fill {{
        height: 100%; border-radius: 3px;
        background: linear-gradient(90deg, {SPOTIFY["green"]} 0%, {SPOTIFY["green_light"]} 100%);
    }}
    .billboard-value {{
        font-size: 0.75rem; color: {SPOTIFY["text_secondary"]};
        width: 72px; text-align: right; flex-shrink: 0; white-space: nowrap;
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    /* ---- Discovery card ---- */
    .discovery-card {{
        background: linear-gradient(145deg, {SPOTIFY["bg_card"]} 0%, {SPOTIFY["bg_elevated"]} 100%);
        border: 1px solid {SPOTIFY["border"]}; border-radius: 12px; padding: 16px;
        text-align: center; transition: all 0.3s ease;
    }}
    .discovery-card:hover {{
        border-color: {SPOTIFY["green"]};
        box-shadow: 0 4px 15px rgba(29,185,84,0.1);
    }}
    .discovery-big {{
        font-size: 2rem; font-weight: 700; color: {SPOTIFY["green"]};
        font-family: 'JetBrains Mono', monospace !important;
    }}
    .discovery-label {{
        font-size: 0.7rem; color: {SPOTIFY["text_muted"]};
        text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px;
    }}
    .discovery-detail {{
        font-size: 0.75rem; color: {SPOTIFY["text_secondary"]}; margin-top: 2px;
    }}
    
    /* ---- Misc ---- */
    hr {{ border: none; height: 1px; background: {SPOTIFY["border"]}; margin: 16px 0; opacity: 0.5; }}
    
    .stRadio > div {{
        flex-direction: row !important; gap: 4px !important;
        background: {SPOTIFY["bg_elevated"]}; padding: 4px; border-radius: 8px;
        border: 1px solid {SPOTIFY["border"]};
    }}
    .stRadio > div > label {{
        background: transparent !important; border: none !important;
        padding: 6px 12px !important; margin: 0 !important; border-radius: 6px !important;
        color: {SPOTIFY["text_secondary"]} !important; font-size: 0.8rem !important;
        cursor: pointer; transition: all 0.2s ease;
    }}
    .stRadio > div > label:hover {{ background: {SPOTIFY["bg_highlight"]} !important; color: {SPOTIFY["white"]} !important; }}
    .stRadio > div > label[data-checked="true"] {{ background: {SPOTIFY["green"]} !important; color: {SPOTIFY["bg_dark"]} !important; }}
    
    .stSelectbox > div > div {{ background: {SPOTIFY["bg_elevated"]} !important; border-color: {SPOTIFY["border"]} !important; }}
    
    .stTabs [data-baseweb="tab-list"] {{ gap: 0; background: {SPOTIFY["bg_elevated"]}; padding: 3px; border-radius: 8px; }}
    .stTabs [data-baseweb="tab"] {{ background: transparent; border-radius: 6px; color: {SPOTIFY["text_secondary"]}; padding: 6px 14px; font-size: 0.8rem; }}
    .stTabs [aria-selected="true"] {{ background: {SPOTIFY["green"]} !important; color: {SPOTIFY["bg_dark"]} !important; }}
    
    div[data-testid="stCheckbox"] label span {{ color: {SPOTIFY["text_secondary"]} !important; }}
    
    /* ---- Narrative box ---- */
    .narrative-box {{
        background: linear-gradient(135deg, rgba(29,185,84,0.08) 0%, rgba(29,185,84,0.02) 100%);
        border-left: 3px solid {SPOTIFY["green"]};
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0 16px 0;
        color: {SPOTIFY["text_secondary"]};
        font-size: 0.85rem;
        line-height: 1.5;
    }}
    .narrative-box strong {{ color: {SPOTIFY["white"]}; }}
    .narrative-box .highlight {{ color: {SPOTIFY["green"]}; font-weight: 600; }}
    
    /* Hide Streamlit fullscreen button on chart containers */
    button[title="View fullscreen"] {{ display: none !important; }}
    /* Hide Streamlit sidebar navigation for multipage apps */
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# Helper Functions
# ----------------------------
def clean_string(s):
    if pd.isna(s): return None
    s = str(s).strip()
    return None if s.lower() in ["nan", "none", "undefined", "null", ""] else s

def _to_bool(x):
    if isinstance(x, bool): return x
    if pd.isna(x): return False
    return str(x).strip().lower() in ["true", "t", "1", "yes", "y"]

def section_header(icon, title, help_text=None):
    st.markdown(f'''<div class="section-header">
        <span style="font-size:1.1rem;">{icon}</span>
        <span class="section-title">{title}</span>
    </div>''', unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)

def style_fig(fig, height=300, show_legend=False):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=SPOTIFY["text_secondary"], family="DM Sans", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=show_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        hoverlabel=dict(bgcolor=SPOTIFY["bg_elevated"], font_size=11, bordercolor=SPOTIFY["border"])
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(64,64,64,0.2)", zeroline=False, tickfont=dict(size=9))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(64,64,64,0.2)", zeroline=False, tickfont=dict(size=9))
    return fig

# Hide the Plotly toolbar (zoom, download, etc.) on all charts — professor feedback
PLOTLY_CONFIG = {"displayModeBar": False}
# Heatmap needs a minimal toolbar so box-select works reliably
HEATMAP_CONFIG = {
    "displayModeBar": True,
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
        "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian",
        "toggleSpikelines", "toImage", "sendDataToCloud", "lasso2d",
    ],
    "displaylogo": False,
    "showEditInChartStudio": False,
}

@st.cache_data(show_spinner=False)
def load_csv(uploaded_file=None, path=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif path is not None:
        df = pd.read_csv(path)
    else:
        return pd.DataFrame()
    
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts"])
    df["ms_played"] = pd.to_numeric(df["ms_played"], errors="coerce").fillna(0).astype(int)
    df["skipped"] = df["skipped"].apply(_to_bool)
    df["artist_popularity"] = pd.to_numeric(df["artist_popularity"], errors="coerce")
    df["date"] = df["ts"].dt.date
    df["year"] = df["ts"].dt.year
    df["month"] = df["ts"].dt.to_period("M").astype(str)
    df["dow"] = df["ts"].dt.dayofweek
    df["hour"] = df["ts"].dt.hour
    df["start_ts"] = df["ts"] - pd.to_timedelta(df["ms_played"], unit="ms")
    
    for c in ["master_metadata_track_name", "master_metadata_album_artist_name",
              "master_metadata_album_album_name", "genre_bucket", "artist_genres"]:
        if c in df.columns:
            df[c] = df[c].apply(clean_string)
    
    df["track_id"] = df.apply(
        lambda r: f"{r['master_metadata_album_artist_name']}§{r['master_metadata_track_name']}"
        if r.get('master_metadata_track_name') and r.get('master_metadata_album_artist_name') else None, axis=1)
    return df

def measure_value(df, measure):
    return pd.Series(np.ones(len(df)), index=df.index) if measure == "Streams" else df["ms_played"] / 60000

def fmt_number(n):
    try:
        if abs(n) >= 1e6: return f"{n/1e6:.1f}M"
        if abs(n) >= 1e3: return f"{n/1e3:.1f}K"
        return f"{int(n):,}" if float(n).is_integer() else f"{n:.1f}"
    except: return str(n)

def fmt_hours(minutes):
    """Format minutes as Xh Ym for readability."""
    h = int(minutes // 60)
    m = int(minutes % 60)
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"

@st.cache_data
def compute_discovery(df_full, df_filtered):
    first_artist = df_full.dropna(subset=["master_metadata_album_artist_name"]).groupby("master_metadata_album_artist_name")["ts"].min()
    first_track = df_full.dropna(subset=["track_id"]).groupby("track_id")["ts"].min()
    period_start = df_filtered["ts"].min()
    period_end = df_filtered["ts"].max()
    new_artists = first_artist[(first_artist >= period_start) & (first_artist <= period_end)]
    new_tracks = first_track[(first_track >= period_start) & (first_track <= period_end)]
    period_artists = df_filtered["master_metadata_album_artist_name"].dropna().nunique()
    period_tracks = df_filtered["track_id"].dropna().nunique()
    pct_new_artists = (len(new_artists) / period_artists * 100) if period_artists > 0 else 0
    pct_new_tracks = (len(new_tracks) / period_tracks * 100) if period_tracks > 0 else 0
    return pct_new_artists, pct_new_tracks, len(new_artists), len(new_tracks)

@st.cache_data
def compute_old_vs_new_monthly(df_full, start_date, end_date):
    df_clean = df_full.dropna(subset=["track_id"]).copy()
    if len(df_clean) == 0: return pd.DataFrame()
    first_listen = df_clean.groupby("track_id")["ts"].min().reset_index()
    first_listen.columns = ["track_id", "first_listen_ts"]
    first_listen["first_listen_month"] = pd.to_datetime(first_listen["first_listen_ts"]).dt.to_period("M").astype(str)
    track_months = df_clean.groupby(["month", "track_id"]).size().reset_index(name="play_count")
    track_months = track_months.merge(first_listen[["track_id", "first_listen_month"]], on="track_id")
    track_months["is_new"] = track_months["month"] == track_months["first_listen_month"]
    monthly_counts = track_months.groupby(["month", "is_new"]).agg(unique_tracks=("track_id", "nunique")).reset_index()
    pivot = monthly_counts.pivot(index="month", columns="is_new", values="unique_tracks").fillna(0)
    if False in pivot.columns and True in pivot.columns:
        pivot.columns = ["Revisited tracks", "New discoveries"]
    elif True in pivot.columns:
        pivot.columns = ["New discoveries"]
        pivot["Revisited tracks"] = 0
    elif False in pivot.columns:
        pivot.columns = ["Revisited tracks"]
        pivot["New discoveries"] = 0
    pivot = pivot.reset_index()
    start_month = pd.Timestamp(start_date).to_period("M").strftime("%Y-%m")
    end_month = pd.Timestamp(end_date).to_period("M").strftime("%Y-%m")
    pivot = pivot[(pivot["month"] >= start_month) & (pivot["month"] <= end_month)]
    return pivot

@st.cache_data
def compute_genre_evolution(df_filtered, measure="Minutes"):
    """Compute genre proportions over time for the stream-graph."""
    gdf = df_filtered.dropna(subset=["genre_bucket"]).copy()
    if len(gdf) == 0: return pd.DataFrame()
    if measure == "Minutes":
        gdf["val"] = gdf["ms_played"] / 60000
    else:
        gdf["val"] = 1  # count streams
    monthly = gdf.groupby(["month", "genre_bucket"], as_index=False)["val"].sum()
    pivot = monthly.pivot(index="month", columns="genre_bucket", values="val").fillna(0)
    for g in GENRE_ORDER:
        if g not in pivot.columns:
            pivot[g] = 0
    pivot = pivot[GENRE_ORDER].reset_index()
    return pivot

@st.cache_data
def sessionize(df, gap_minutes=15):
    if len(df) == 0: return df
    d = df.sort_values("start_ts").copy()
    gap = pd.Timedelta(minutes=gap_minutes)
    prev_end = d["ts"].shift(1)
    new_session = (d["start_ts"] - prev_end) > gap
    d["session_id"] = new_session.cumsum().fillna(0).astype(int)
    session_len = d.groupby("session_id")["ms_played"].sum() / 60000
    d["session_minutes"] = d["session_id"].map(session_len)
    return d

@st.cache_data
def compute_streaks(df_filtered):
    """Compute the longest listening streak (consecutive days)."""
    dates_active = sorted(df_filtered["date"].unique())
    if len(dates_active) == 0: return 0, 0
    max_streak = 1; current_streak = 1
    for i in range(1, len(dates_active)):
        if (dates_active[i] - dates_active[i-1]).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    return max_streak, current_streak

@st.cache_data
def compute_bump_chart(df_filtered, measure="Streams", top_n=10):
    """Compute monthly rankings for top artists — for a bump (F1-style) chart."""
    adf = df_filtered.dropna(subset=["master_metadata_album_artist_name"]).copy()
    if len(adf) == 0:
        return pd.DataFrame()
    if measure == "Minutes":
        adf["val"] = adf["ms_played"] / 60000
    else:
        adf["val"] = 1
    monthly = adf.groupby(["month", "master_metadata_album_artist_name"], as_index=False)["val"].sum()
    # Determine top N artists overall
    top_artists = monthly.groupby("master_metadata_album_artist_name")["val"].sum().nlargest(top_n).index.tolist()
    monthly = monthly[monthly["master_metadata_album_artist_name"].isin(top_artists)]
    # Rank per month (1 = best)
    monthly["rank"] = monthly.groupby("month")["val"].rank(ascending=False, method="min").astype(int)
    return monthly

def bins_session_minutes(x):
    """Finer session bins based on peer feedback."""
    if x < 15: return "<15m"
    if x < 30: return "15–30m"
    if x < 60: return "30m–1h"
    if x < 120: return "1–2h"
    if x < 240: return "2–4h"
    return "4h+"

SESSION_BIN_ORDER = ["<15m", "15–30m", "30m–1h", "1–2h", "2–4h", "4h+"]

# ----------------------------
# Life Events System
# ----------------------------
EVENT_COLORS = {
    "semester": "rgba(59,130,246,0.12)",   # blue
    "exam": "rgba(239,68,68,0.15)",        # red
    "travel": "rgba(249,115,22,0.15)",     # orange
    "personal": "rgba(168,85,247,0.12)",   # purple
}
EVENT_BORDER_COLORS = {
    "semester": "rgba(59,130,246,0.4)",
    "exam": "rgba(239,68,68,0.5)",
    "travel": "rgba(249,115,22,0.5)",
    "personal": "rgba(168,85,247,0.4)",
}
EVENT_LABEL_COLORS = {
    "semester": "#60A5FA",
    "exam": "#F87171",
    "travel": "#FB923C",
    "personal": "#C084FC",
}

@st.cache_data(show_spinner=False)
def load_events(uploaded_file=None, path=None):
    """Load life events CSV. Expected columns: start_date, end_date, label, category"""
    try:
        if uploaded_file is not None:
            ev = pd.read_csv(uploaded_file)
        elif path is not None:
            ev = pd.read_csv(path)
        else:
            return pd.DataFrame()
        ev["start_date"] = pd.to_datetime(ev["start_date"]).dt.date
        ev["end_date"] = pd.to_datetime(ev["end_date"]).dt.date
        ev["category"] = ev["category"].str.strip().str.lower()
        # Convert dates to month strings for time-series matching
        ev["start_month"] = pd.to_datetime(ev["start_date"]).dt.to_period("M").astype(str)
        ev["end_month"] = pd.to_datetime(ev["end_date"]).dt.to_period("M").astype(str)
        return ev
    except Exception:
        return pd.DataFrame()

def add_event_overlays(fig, events_df, start_date, end_date, axis_type="month"):
    """
    Overlay life events as shaded regions on a time-series figure.
    axis_type: "month" for month-based x-axes (YYYY-MM), "date" for date-based.
    """
    if events_df is None or len(events_df) == 0:
        return fig
    
    for _, ev in events_df.iterrows():
        ev_start = ev["start_date"]
        ev_end = ev["end_date"]
        
        # Skip events outside the visible range
        if ev_end < start_date or ev_start > end_date:
            continue
        
        cat = ev["category"]
        fillcolor = EVENT_COLORS.get(cat, "rgba(107,114,128,0.1)")
        bordercolor = EVENT_BORDER_COLORS.get(cat, "rgba(107,114,128,0.3)")
        label_color = EVENT_LABEL_COLORS.get(cat, "#9CA3AF")
        
        if axis_type == "month":
            x0 = pd.Timestamp(ev_start).to_period("M").strftime("%Y-%m")
            x1 = pd.Timestamp(ev_end).to_period("M").strftime("%Y-%m")
        else:
            x0 = ev_start
            x1 = ev_end
        
        fig.add_vrect(
            x0=x0, x1=x1,
            fillcolor=fillcolor,
            line=dict(color=bordercolor, width=1, dash="dot"),
            layer="below",
        )
        
        # Add a small label at the top
        mid_date = ev_start + (ev_end - ev_start) / 2
        if axis_type == "month":
            x_label = pd.Timestamp(mid_date).to_period("M").strftime("%Y-%m")
        else:
            x_label = mid_date
        
        fig.add_annotation(
            x=x_label, y=1.0, yref="paper",
            text=ev["label"],
            showarrow=False,
            font=dict(size=8, color=label_color),
            bgcolor="rgba(18,18,18,0.8)",
            borderpad=2,
            yshift=10,
        )
    
    return fig


# ====================================================
# HEADER
# ====================================================
_hdr_l, _hdr_r = st.columns([5, 1])
with _hdr_l:
    st.markdown(f"""
    <div class="dashboard-header">
        <span class="fingerprint-icon">🎧</span>
        <div>
            <h1 class="dashboard-title">Musical Fingerprint</h1>
            <p class="dashboard-subtitle">Your unique listening DNA — patterns, genres, discoveries & obsessions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with _hdr_r:
    st.markdown(f"""
    <a href="/about" target="_self" style="
        display: inline-block; margin-top: 18px; padding: 8px 16px;
        background: {SPOTIFY['bg_elevated']}; border: 1px solid {SPOTIFY['border']};
        border-radius: 20px; color: {SPOTIFY['white']}; text-decoration: none;
        font-size: 0.82rem; font-weight: 500; font-family: 'DM Sans', sans-serif;
        transition: background 0.2s;
    " onmouseover="this.style.background='{SPOTIFY['bg_highlight']}'"
       onmouseout="this.style.background='{SPOTIFY['bg_elevated']}'">
        📖 About
    </a>
    """, unsafe_allow_html=True)

st.markdown("---")

# ====================================================
# FILTERS
# ====================================================
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.8, 0.8, 0.4, 1])

with filter_col1:
    time_options = ["30 days", "90 days", "180 days", "Year", "Lifetime"]
    selected_time = st.radio("Time", time_options, index=4, horizontal=True, label_visibility="collapsed")

with filter_col4:
    fc4a, fc4b = st.columns(2)
    with fc4a:
        use_demo = st.checkbox("Demo data", value=True)
    with fc4b:
        show_events = st.checkbox("Life events", value=False)
    if not use_demo:
        uploaded_file = st.file_uploader("Music CSV", type=["csv"], label_visibility="collapsed")
        events_file = st.file_uploader("Life events CSV", type=["csv"], label_visibility="collapsed",
                                       help="Columns: start_date, end_date, label, category (semester/exam/travel/personal)")
    else:
        uploaded_file = None
        events_file = None

try:
    if use_demo:
        df = load_csv(path="music_data.csv")
    elif uploaded_file:
        df = load_csv(uploaded_file=uploaded_file)
    else:
        st.info("📂 Upload your enriched Spotify CSV or enable demo data to explore.")
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

min_date, max_date = df["date"].min(), df["date"].max()

with filter_col2:
    today = max_date
    preset_ranges = {
        "30 days": (today - timedelta(days=30), today),
        "90 days": (today - timedelta(days=90), today),
        "180 days": (today - timedelta(days=180), today),
        "Year": (date(today.year, 1, 1), today),
        "Lifetime": (min_date, max_date),
    }
    default_start, default_end = preset_ranges.get(selected_time, (min_date, max_date))
    default_start = max(default_start, min_date)
    default_end = min(default_end, max_date)
    date_range = st.date_input("Dates", (default_start, default_end), min_value=min_date, max_value=max_date,
                               label_visibility="collapsed")
    start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (default_start, default_end)

with filter_col3:
    measure = st.selectbox("Measure", ["Streams", "Minutes"], label_visibility="collapsed")

mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_f = df[mask].copy()

if len(df_f) == 0:
    st.warning("No data in the selected range.")
    st.stop()

# ----------------------------
# Life Events loading
# ----------------------------
if show_events:
    if use_demo:
        events_df = load_events(path="life_events.csv")
    elif events_file:
        events_df = load_events(uploaded_file=events_file)
    else:
        events_df = pd.DataFrame()
else:
    events_df = pd.DataFrame()

# ====================================================
# KPI ROW
# ====================================================
total_streams = len(df_f)
total_minutes = df_f["ms_played"].sum() / 60000
total_hours = total_minutes / 60
n_tracks = df_f["track_id"].dropna().nunique()
n_artists = df_f["master_metadata_album_artist_name"].dropna().nunique()
n_albums = df_f["master_metadata_album_album_name"].dropna().nunique()
avg_skip_time = df_f[df_f["skipped"]]["ms_played"].mean() / 1000 if df_f["skipped"].any() else 0
max_streak, current_streak = compute_streaks(df_f)

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Streams</div>
        <div class="kpi-value">{fmt_number(total_streams)}</div>
        <div class="kpi-trend">total plays</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Listening Time</div>
        <div class="kpi-value">{total_hours:,.0f}<span style="font-size:0.9rem;color:{SPOTIFY['text_muted']};"> hrs</span></div>
        <div class="kpi-trend">{total_minutes:,.0f} minutes</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Unique Tracks</div>
        <div class="kpi-value">{fmt_number(n_tracks)}</div>
        <div class="kpi-trend">distinct songs</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Artists</div>
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
        <div class="kpi-value">{avg_skip_time:.1f}<span style="font-size:0.9rem;color:{SPOTIFY['text_muted']};"> sec</span></div>
        <div class="kpi-trend">avg before skip</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Best Streak</div>
        <div class="kpi-value">{max_streak}<span style="font-size:0.9rem;color:{SPOTIFY['text_muted']};"> days</span></div>
        <div class="kpi-trend">consecutive listening</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================================================
# ADAPTIVE LAYOUT — changes based on time range
# ====================================================
is_lifetime = selected_time == "Lifetime"

# ── Shared computations ──
# Listening Clock data
by_hour = df_f.copy()
by_hour["m"] = measure_value(by_hour, measure)
hour_agg = by_hour.groupby("hour", as_index=False)["m"].sum()
hour_mins = by_hour.groupby("hour", as_index=False)["ms_played"].agg(total_minutes=lambda s: s.sum() / 60000)
hour_agg = pd.DataFrame({"hour": range(24)}).merge(hour_agg, on="hour", how="left").fillna(0)
hour_agg = hour_agg.merge(hour_mins, on="hour", how="left").fillna(0)

# Heatmap data
daily = df_f.groupby("date", as_index=False).agg(
    streams=("ts", "count"), minutes=("ms_played", lambda s: s.sum()/60000))
daily["value"] = daily["streams"] if measure == "Streams" else daily["minutes"]
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Use ISO week numbering to avoid year-boundary gaps
_iso = all_dates.isocalendar()
full_grid = pd.DataFrame({
    'date': all_dates.date,
    'week': [f"{y}-W{w:02d}" for y, w in zip(_iso.year, _iso.week)],
    'dow': all_dates.dayofweek,
    'month_label': all_dates.strftime("%b %y"),
})
full_grid = full_grid.merge(daily[['date', 'value', 'minutes']], on='date', how='left').fillna(0)
day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
full_grid["day_name"] = full_grid["dow"].apply(lambda x: day_names[x])
full_grid["date_str"] = full_grid["date"].astype(str)
grid_dates = full_grid["date"].tolist()

# ── Reusable chart builders ──
def _build_clock_fig():
    fig = go.Figure(go.Barpolar(
        r=hour_agg["m"], theta=hour_agg["hour"] * 15, width=[14] * 24,
        marker_color=SPOTIFY["green"], marker_line_color=SPOTIFY["green_light"], marker_line_width=1, opacity=0.85,
        hovertemplate=(
            "<b>%{customdata[0]}:00</b><br>"
            "%{r:,.0f} " + measure.lower() + "<br>"
            "%{customdata[1]}<extra></extra>"
        ),
        customdata=list(zip(
            [f"{h:02d}" for h in hour_agg["hour"]],
            [fmt_hours(m) for m in hour_agg["total_minutes"]]
        ))
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(showticklabels=False, gridcolor="rgba(64,64,64,0.2)"),
            angularaxis=dict(direction="clockwise", rotation=90, tickmode="array",
                tickvals=[i*15 for i in range(0, 24, 3)],
                ticktext=[f"{i}h" for i in range(0, 24, 3)],
                tickfont=dict(size=9, color=SPOTIFY["text_muted"]),
                gridcolor="rgba(64,64,64,0.2)")),
        margin=dict(l=30, r=30, t=10, b=10)
    )
    return style_fig(fig, height=220)

def _build_sessions_fig():
    df_s = sessionize(df_f, gap_minutes=15)
    if len(df_s) == 0: return None
    sess = df_s.groupby("session_id", as_index=False).agg(session_minutes=("session_minutes", "first"))
    sess["bin"] = sess["session_minutes"].apply(bins_session_minutes)
    sess_bins = sess.groupby("bin", as_index=False).size().rename(columns={"size": "sessions"})
    sess_bins["bin"] = pd.Categorical(sess_bins["bin"], categories=SESSION_BIN_ORDER, ordered=True)
    sess_bins = sess_bins.sort_values("bin")
    fig = px.bar(sess_bins, x="bin", y="sessions", color_discrete_sequence=[SPOTIFY["green"]])
    fig.update_traces(
        marker_line_color=SPOTIFY["green_light"], marker_line_width=1,
        hovertemplate="<b>%{x}</b><br>%{y} sessions<extra></extra>"
    )
    fig.update_layout(xaxis_title="Duration", yaxis_title="Sessions")
    return fig

def _build_heatmap_fig(cal_height=220):
    fig_cal = go.Figure(go.Heatmap(
        x=full_grid["week"], y=full_grid["dow"], z=full_grid["value"],
        colorscale=[
            [0, SPOTIFY["bg_elevated"]], [0.15, "#0d3320"], [0.35, "#166534"],
            [0.6, "#22c55e"], [1, SPOTIFY["green_light"]]
        ],
        showscale=True,
        colorbar=dict(
            thickness=8, len=0.9, y=0.5, yanchor="middle",
            tickfont=dict(size=8, color=SPOTIFY["text_muted"]),
            title=dict(text=measure, font=dict(size=8, color=SPOTIFY["text_muted"])),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
        ),
        ygap=2, xgap=2,
        hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            + measure + ": %{z:,.0f}<br>"
            "Time: %{customdata[2]}<extra></extra>"
        ),
        customdata=[[d, dn, fmt_hours(m)] for d, dn, m in zip(
            full_grid["date_str"], full_grid["day_name"], full_grid["minutes"]
        )]
    ))
    fig_cal.update_yaxes(tickvals=list(range(7)), ticktext=day_names, autorange="reversed")
    month_ticks = full_grid.drop_duplicates(subset=["month_label"], keep="first")
    fig_cal.update_xaxes(
        tickvals=month_ticks["week"].tolist(),
        ticktext=month_ticks["month_label"].tolist(),
        showticklabels=True,
        tickfont=dict(size=8, color=SPOTIFY["text_muted"]),
        tickangle=-45,
    )
    fig_cal.update_layout(margin=dict(l=40, r=60, t=10, b=20), dragmode="select")
    return style_fig(fig_cal, height=cal_height)

def _render_no1():
    section_header("👑", "No. 1 Artist", "Most played by listening time")
    top_artist_df = (df_f.dropna(subset=["master_metadata_album_artist_name"])
                     .groupby("master_metadata_album_artist_name")["ms_played"].sum()
                     .sort_values(ascending=False))
    if len(top_artist_df) > 0:
        artist_name = top_artist_df.index[0]
        artist_streams = df_f[df_f['master_metadata_album_artist_name'] == artist_name].shape[0]
        artist_mins = top_artist_df.iloc[0] / 60000
        st.markdown(f"""<div class="top-item-card">
            <div class="rank-badge">🎧</div>
            <div style="flex:1;min-width:0;">
                <div class="top-item-name">{artist_name}</div>
                <div class="top-item-sub">{artist_streams:,} streams · {fmt_hours(artist_mins)}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    section_header("🎵", "No. 1 Track", "Most played song")
    top_track_df = (df_f.dropna(subset=["master_metadata_track_name", "master_metadata_album_artist_name"])
                    .groupby(["master_metadata_track_name", "master_metadata_album_artist_name"])["ms_played"]
                    .sum().sort_values(ascending=False))
    if len(top_track_df) > 0:
        (track_name, track_artist) = top_track_df.index[0]
        track_streams = df_f[(df_f['master_metadata_track_name'] == track_name) &
                             (df_f['master_metadata_album_artist_name'] == track_artist)].shape[0]
        st.markdown(f"""<div class="top-item-card">
            <div class="rank-badge">🎧</div>
            <div style="flex:1;min-width:0;">
                <div class="top-item-name">{track_name}</div>
                <div class="top-item-sub">{track_artist} · {track_streams} plays</div>
            </div>
        </div>""", unsafe_allow_html=True)

def _render_old_vs_new(chart_height=250):
    section_header("🆕", "Old vs New", "Unique songs each month: first listens vs revisits")
    old_new_data = compute_old_vs_new_monthly(df, start_date, end_date)
    if len(old_new_data) > 0 and "Revisited tracks" in old_new_data.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=old_new_data["month"], y=old_new_data["Revisited tracks"],
            name="Revisited", stackgroup="one",
            line=dict(width=0.5, color=SPOTIFY["text_muted"]),
            fillcolor="rgba(114,114,114,0.3)",
            hovertemplate="<b>%{x}</b><br>Revisited: %{y} tracks<extra></extra>",
        ))
        if "New discoveries" in old_new_data.columns:
            fig.add_trace(go.Scatter(
                x=old_new_data["month"], y=old_new_data["New discoveries"],
                name="New discoveries", stackgroup="one",
                line=dict(width=0.5, color=SPOTIFY["green"]),
                fillcolor="rgba(29,185,84,0.4)",
                hovertemplate="<b>%{x}</b><br>New: %{y} tracks<extra></extra>",
            ))
        fig.update_layout(xaxis_title="Month", yaxis_title="Unique tracks", hovermode="x unified")
        if show_events and len(events_df) > 0:
            fig = add_event_overlays(fig, events_df, start_date, end_date, axis_type="month")
        st.plotly_chart(style_fig(fig, height=chart_height, show_legend=True), use_container_width=True, key="oldnew", config=PLOTLY_CONFIG)
    else:
        st.info("Not enough data for this view.")


# ╔════════════════════════════════════════════════════╗
# ║  LIFETIME LAYOUT — heatmap gets full width         ║
# ╚════════════════════════════════════════════════════╝
if is_lifetime:
    # Row 1: Clock | Sessions | No.1 | Rank sparklines
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.5])
    
    with col1:
        section_header("🕐", "Listening Clock", "When you listen most")
        st.plotly_chart(_build_clock_fig(), use_container_width=True, key="clock", config=PLOTLY_CONFIG)
    
    with col2:
        section_header("⏱️", "Sessions", "Listening session durations")
        sfig = _build_sessions_fig()
        if sfig:
            st.plotly_chart(style_fig(sfig, height=220), use_container_width=True, key="sessions", config=PLOTLY_CONFIG)
    
    with col3:
        _render_no1()
    
    with col4:
        # Two compact rank-over-time sparklines for the No.1 artist and track
        # --- No.1 Artist rank over time ---
        top_artist_df_lt = (df_f.dropna(subset=["master_metadata_album_artist_name"])
                         .groupby("master_metadata_album_artist_name")["ms_played"].sum()
                         .sort_values(ascending=False))
        if len(top_artist_df_lt) > 0:
            no1_artist = top_artist_df_lt.index[0]
            adf = df_f.dropna(subset=["master_metadata_album_artist_name"]).copy()
            adf["val"] = adf["ms_played"] / 60000 if measure == "Minutes" else 1
            monthly_a = adf.groupby(["month", "master_metadata_album_artist_name"], as_index=False)["val"].sum()
            monthly_a["rank"] = monthly_a.groupby("month")["val"].rank(ascending=False, method="min").astype(int)
            artist_rank = monthly_a[monthly_a["master_metadata_album_artist_name"] == no1_artist].sort_values("month")
            
            if len(artist_rank) > 1:
                st.caption("👑 **Artist rank over time**")
                _max_r = max(artist_rank["rank"].max(), 4)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=artist_rank["month"], y=artist_rank["rank"],
                    mode="lines+markers", fill="tozeroy",
                    line=dict(width=2, color=SPOTIFY["green"]),
                    marker=dict(size=4, color=SPOTIFY["green_light"]),
                    fillcolor="rgba(29,185,84,0.15)",
                    hovertemplate="<b>%{x}</b><br>Rank #%{y}<extra></extra>",
                ))
                fig.update_yaxes(autorange="reversed", title="", range=[0.5, _max_r + 0.5],
                                 tickmode="linear", dtick=max(1, _max_r // 3),
                                 gridcolor="rgba(64,64,64,0.15)",
                                 tickfont=dict(size=8, color=SPOTIFY["text_muted"]))
                # Show ~5 x-axis ticks
                _n_ticks_a = min(5, len(artist_rank))
                _step_a = max(1, len(artist_rank) // _n_ticks_a)
                _tick_idx_a = artist_rank.iloc[::_step_a]
                fig.update_xaxes(title="", tickmode="array",
                                 tickvals=_tick_idx_a["month"].tolist(),
                                 ticktext=[m[-5:] for m in _tick_idx_a["month"].tolist()],
                                 tickangle=-45, tickfont=dict(size=7, color=SPOTIFY["text_muted"]))
                fig.update_layout(margin=dict(l=25, r=5, t=5, b=25),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(style_fig(fig, height=100), use_container_width=True,
                                key="rank_artist", config=PLOTLY_CONFIG)
        
        # --- No.1 Track rank over time ---
        top_track_df_lt = (df_f.dropna(subset=["master_metadata_track_name", "master_metadata_album_artist_name"])
                        .groupby(["master_metadata_track_name", "master_metadata_album_artist_name"])["ms_played"]
                        .sum().sort_values(ascending=False))
        if len(top_track_df_lt) > 0:
            (no1_track, no1_track_artist) = top_track_df_lt.index[0]
            tdf = df_f.dropna(subset=["master_metadata_track_name"]).copy()
            tdf["val"] = tdf["ms_played"] / 60000 if measure == "Minutes" else 1
            monthly_t = tdf.groupby(["month", "master_metadata_track_name"], as_index=False)["val"].sum()
            monthly_t["rank"] = monthly_t.groupby("month")["val"].rank(ascending=False, method="min").astype(int)
            track_rank = monthly_t[monthly_t["master_metadata_track_name"] == no1_track].sort_values("month")
            
            if len(track_rank) > 1:
                st.caption("🎵 **Track rank over time**")
                _max_r_t = max(track_rank["rank"].max(), 4)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=track_rank["month"], y=track_rank["rank"],
                    mode="lines+markers", fill="tozeroy",
                    line=dict(width=2, color=SPOTIFY["green"]),
                    marker=dict(size=4, color=SPOTIFY["green_light"]),
                    fillcolor="rgba(29,185,84,0.1)",
                    hovertemplate=f"<b>{no1_track}</b><br>" + "%{x}<br>Rank #%{y}<extra></extra>",
                ))
                fig.update_yaxes(autorange="reversed", title="", range=[0.5, _max_r_t + 0.5],
                                 tickmode="linear", dtick=max(1, _max_r_t // 3),
                                 gridcolor="rgba(64,64,64,0.15)",
                                 tickfont=dict(size=8, color=SPOTIFY["text_muted"]))
                _n_ticks_t = min(5, len(track_rank))
                _step_t = max(1, len(track_rank) // _n_ticks_t)
                _tick_idx_t = track_rank.iloc[::_step_t]
                fig.update_xaxes(title="", tickmode="array",
                                 tickvals=_tick_idx_t["month"].tolist(),
                                 ticktext=[m[-5:] for m in _tick_idx_t["month"].tolist()],
                                 tickangle=-45, tickfont=dict(size=7, color=SPOTIFY["text_muted"]))
                fig.update_layout(margin=dict(l=25, r=5, t=5, b=25),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(style_fig(fig, height=100), use_container_width=True,
                                key="rank_track", config=PLOTLY_CONFIG)
    
    # Row 2: Full-width heatmap (finally readable for lifetime!)
    section_header("📅", "Commit-ment to Music", "Daily listening — drag-select days to filter the whole dashboard")
    cal_event = st.plotly_chart(
        _build_heatmap_fig(cal_height=180),
        use_container_width=True, key="calendar",
        on_select="rerun", selection_mode=["box", "points"], config=HEATMAP_CONFIG,
    )
    
    # Row 3: Full-width Old vs New (with events)
    _render_old_vs_new(chart_height=280)

# ╔════════════════════════════════════════════════════╗
# ║  FILTERED LAYOUT — compact with discovery cards    ║
# ╚════════════════════════════════════════════════════╝
else:
    # Row 1: Clock | Sessions | Heatmap
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        section_header("🕐", "Listening Clock", "When you listen most")
        st.plotly_chart(_build_clock_fig(), use_container_width=True, key="clock", config=PLOTLY_CONFIG)
    
    with col2:
        section_header("⏱️", "Sessions", "Listening session durations")
        sfig = _build_sessions_fig()
        if sfig:
            st.plotly_chart(style_fig(sfig, height=220), use_container_width=True, key="sessions", config=PLOTLY_CONFIG)
    
    with col3:
        section_header("📅", "Commit-ment to Music", "Daily listening — drag-select days to filter")
        cal_event = st.plotly_chart(
            _build_heatmap_fig(cal_height=220),
            use_container_width=True, key="calendar",
            on_select="rerun", selection_mode=["box", "points"], config=HEATMAP_CONFIG,
        )

# ------------------------------------------------------------------
# PROCESS HEATMAP SELECTION → day-level filter for everything below
# ------------------------------------------------------------------
selected_dates = None
week_dow_to_date = dict(zip(
    zip(full_grid["week"], full_grid["dow"]),
    full_grid["date"]
))

if cal_event and cal_event.selection:
    sel = cal_event.selection
    resolved = []
    
    if sel.points:
        for p in sel.points:
            week_val = p.get("x")
            dow_val = p.get("y")
            if dow_val is not None:
                dow_val = int(round(dow_val)) if isinstance(dow_val, float) else dow_val
            if week_val is not None and dow_val is not None:
                d = week_dow_to_date.get((week_val, dow_val))
                if d is not None:
                    resolved.append(d)
    
    if not resolved and hasattr(sel, "box") and sel.box:
        for box in sel.box:
            x0 = box.get("x", [None, None])
            y0 = box.get("y", [None, None])
            if x0 and y0 and len(x0) == 2 and len(y0) == 2:
                y_min, y_max = sorted([int(round(y0[0])), int(round(y0[1]))])
                for _, row in full_grid.iterrows():
                    if y_min <= row["dow"] <= y_max:
                        w = row["week"]
                        if (x0[0] is None or w >= str(x0[0])) and (x0[1] is None or w <= str(x0[1])):
                            resolved.append(row["date"])
    
    if not resolved and hasattr(sel, "point_indices") and sel.point_indices:
        grid_dates_list = full_grid["date"].tolist()
        for idx in sel.point_indices:
            if 0 <= idx < len(grid_dates_list):
                resolved.append(grid_dates_list[idx])
    
    if resolved:
        selected_dates = sorted(set(resolved))

if selected_dates and len(selected_dates) > 0:
    df_f = df_f[df_f["date"].isin(selected_dates)].copy()
    date_min_s = min(selected_dates).strftime("%b %d")
    date_max_s = max(selected_dates).strftime("%b %d, %Y")
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(29,185,84,0.15) 0%, rgba(29,185,84,0.03) 100%);
        border: 1px solid rgba(29,185,84,0.3);
        border-radius: 8px; padding: 8px 16px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
    ">
        <span style="color:{SPOTIFY['green']}; font-size:0.85rem;">
            📌 Showing <strong>{len(selected_dates)} selected day{'s' if len(selected_dates)>1 else ''}</strong>
            ({date_min_s} → {date_max_s}) · All charts below are filtered
        </span>
        <span style="color:{SPOTIFY['text_muted']}; font-size:0.75rem;">
            Double-click the heatmap to clear
        </span>
    </div>
    """, unsafe_allow_html=True)
    if len(df_f) == 0:
        st.warning("No listening data on the selected days.")
        st.stop()

# ── Row after heatmap: Discovery + Old vs New (filtered layout only) ──
if not is_lifetime:
    pct_new_artists, pct_new_tracks, new_artists_count, new_tracks_count = compute_discovery(df, df_f)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        _render_no1()
    
    with col2:
        section_header("🔍", "Discovery Rate", "What share of your listening was brand-new music?")
        st.markdown(f"""
        <div style="display:flex; gap:12px; margin-bottom: 12px;">
            <div class="discovery-card" style="flex:1;">
                <div class="discovery-big">{pct_new_artists:.0f}%</div>
                <div class="discovery-label">New Artists</div>
                <div class="discovery-detail">
                    {new_artists_count} of {n_artists} artists<br>
                    heard <b>for the first time ever</b>
                </div>
            </div>
            <div class="discovery-card" style="flex:1;">
                <div class="discovery-big">{pct_new_tracks:.0f}%</div>
                <div class="discovery-label">New Tracks</div>
                <div class="discovery-detail">
                    {new_tracks_count} of {n_tracks} tracks<br>
                    played <b>for the first time ever</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        _render_old_vs_new(chart_height=250)

# ====================================================
# Sunburst | Genre Treemap
# ====================================================
col1, col2 = st.columns([1, 2])

with col1:
    section_header("🌞", "Top Artists → Tracks", "Your top 3 artists and their most-played tracks")
    sun_df = df_f.dropna(subset=["master_metadata_album_artist_name", "master_metadata_track_name"]).copy()
    sun_df["m"] = measure_value(sun_df, measure)
    artist_totals = sun_df.groupby("master_metadata_album_artist_name")["m"].sum()
    top3 = artist_totals.nlargest(3).index.tolist()
    sun_df = sun_df[sun_df["master_metadata_album_artist_name"].isin(top3)]
    sun_agg = sun_df.groupby(["master_metadata_album_artist_name", "master_metadata_track_name"])["m"].sum().reset_index()
    sun_agg = (sun_agg
               .sort_values("m", ascending=False)
               .groupby("master_metadata_album_artist_name", group_keys=False)
               .head(4)
               .reset_index(drop=True))
    
    if len(sun_agg) > 0:
        # Spotify-themed green palette
        palette = ["#1DB954", "#15803D", "#166534"]
        fig = px.sunburst(sun_agg, path=["master_metadata_album_artist_name", "master_metadata_track_name"],
                          values="m", color="master_metadata_album_artist_name",
                          color_discrete_sequence=palette)
        fig.update_traces(
            textinfo="label", insidetextorientation="radial",
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} " + measure.lower() + " (%{percentParent:.1%})<extra></extra>",
        )
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        st.plotly_chart(style_fig(fig, height=320), use_container_width=True, key="sunburst", config=PLOTLY_CONFIG)

with col2:
    section_header("🎨", "Genre Map", "Click a genre to drill into sub-genres; click center to go back")
    
    genre_df = df_f.dropna(subset=["genre_bucket"]).copy()
    genre_df["m"] = measure_value(genre_df, measure)
    
    genre_df["subgenres"] = genre_df["artist_genres"].apply(
        lambda x: [g.strip() for g in str(x).split(",") if g.strip() and clean_string(g.strip())] if x else ["(no subgenre)"]
    )
    
    rows = []
    for _, r in genre_df.iterrows():
        bucket = r["genre_bucket"]
        m_val = r["m"]
        subgenres = r["subgenres"] if r["subgenres"] else ["(no subgenre)"]
        for sg in subgenres:
            rows.append({"genre_bucket": bucket, "subgenre": sg, "m": m_val / len(subgenres)})
    
    if rows:
        treemap_df = pd.DataFrame(rows).groupby(["genre_bucket", "subgenre"], as_index=False)["m"].sum()
        
        # Add percentage to bucket names
        bucket_totals = treemap_df.groupby("genre_bucket")["m"].sum()
        grand_total = bucket_totals.sum()
        bucket_pct = {b: f"{b} ({v / grand_total * 100:.0f}%)" for b, v in bucket_totals.items()}
        treemap_df["genre_bucket_label"] = treemap_df["genre_bucket"].map(bucket_pct)
        
        # Top-N subgenres per bucket + Others (peer feedback)
        TOP_N_SUBGENRES = 8
        result_parts = []
        for bucket, bgroup in treemap_df.groupby("genre_bucket"):
            if len(bgroup) <= TOP_N_SUBGENRES:
                result_parts.append(bgroup)
            else:
                top = bgroup.nlargest(TOP_N_SUBGENRES, "m")
                others_m = bgroup[~bgroup.index.isin(top.index)]["m"].sum()
                others_row = pd.DataFrame([{"genre_bucket": bucket, "subgenre": "Other " + bucket,
                                            "m": others_m, "genre_bucket_label": bucket_pct.get(bucket, bucket)}])
                result_parts.append(pd.concat([top, others_row], ignore_index=True))
        treemap_df = pd.concat(result_parts, ignore_index=True)
        
        # Color map
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        def gradient_color(base_hex, intensity):
            base = hex_to_rgb(base_hex)
            dark = (25, 25, 25)
            return rgb_to_hex(tuple(dark[i] + (base[i] - dark[i]) * intensity for i in range(3)))
        
        color_map = {"(?)": "#1a1a1a", "All Genres": "#1a1a1a"}
        for bucket in GENRE_COLORS:
            # Map both original and labelled names
            color_map[bucket] = GENRE_COLORS[bucket]
            for lbl in bucket_pct.values():
                if lbl.startswith(bucket):
                    color_map[lbl] = GENRE_COLORS[bucket]
        
        for bucket in treemap_df["genre_bucket"].unique():
            bdata = treemap_df[treemap_df["genre_bucket"] == bucket]
            max_m, min_m = bdata["m"].max(), bdata["m"].min()
            base = GENRE_COLORS.get(bucket, SPOTIFY["green"])
            for _, row in bdata.iterrows():
                intensity = 0.35 + 0.65 * ((row["m"] - min_m) / (max_m - min_m)) if max_m > min_m else 1.0
                color_map[row["subgenre"]] = gradient_color(base, intensity)
        
        treemap_df["color_key"] = treemap_df["subgenre"]
        fig = px.treemap(treemap_df, path=[px.Constant("All Genres"), "genre_bucket_label", "subgenre"],
                         values="m", color="color_key", color_discrete_map=color_map)
        fig.update_traces(
            textinfo="label+percent parent", textfont=dict(size=12),
            marker=dict(cornerradius=5),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} " + measure.lower() + "<extra></extra>",
            root_color="#1a1a1a"
        )
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        st.plotly_chart(style_fig(fig, height=320), use_container_width=True, key="treemap", config=PLOTLY_CONFIG)


# ====================================================
# Genre Evolution (full width — under the treemap)
# ====================================================
_ge_unit = "min" if measure == "Minutes" else "streams"
section_header("🌊", "Genre Evolution", f"How your taste shifted over time — {measure.lower()} per month by genre")

genre_evo = compute_genre_evolution(df_f, measure=measure)
if len(genre_evo) > 1:
    fig = go.Figure()
    for genre in GENRE_ORDER:
        if genre in genre_evo.columns and genre_evo[genre].sum() > 0:
            fig.add_trace(go.Scatter(
                x=genre_evo["month"], y=genre_evo[genre],
                name=genre, stackgroup="one",
                line=dict(width=0.5, color=GENRE_COLORS.get(genre, "#6B7280")),
                fillcolor=GENRE_COLORS.get(genre, "#6B7280"),
                hovertemplate=f"<b>{genre}</b>: " + "%{y:,.0f} " + _ge_unit + "<extra></extra>",
            ))
    fig.update_layout(
        xaxis_title="Month", yaxis_title=measure,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(size=9), bgcolor="rgba(0,0,0,0)")
    )
    if show_events and len(events_df) > 0:
        fig = add_event_overlays(fig, events_df, start_date, end_date, axis_type="month")
    st.plotly_chart(style_fig(fig, height=300, show_legend=True), use_container_width=True, key="genre_evo", config=PLOTLY_CONFIG)
else:
    st.info("Need at least 2 months of data for genre evolution.")

# ====================================================
# Niche | Billboard
# ====================================================
col1, col2 = st.columns(2)

with col1:
    section_header("🎯", "Niche Score", "Your artists: Spotify popularity vs your play count")
    
    niche_df = df_f.dropna(subset=["master_metadata_album_artist_name", "artist_popularity"]).copy()
    niche_df["m"] = measure_value(niche_df, measure)
    artist_agg = niche_df.groupby(["master_metadata_album_artist_name", "artist_popularity"], as_index=False).agg(
        val=("m", "sum"), streams=("ts", "count"))
    
    if len(artist_agg) > 0:
        fig = px.scatter(artist_agg, x="artist_popularity", y="val", size="streams", size_max=20,
                         hover_name="master_metadata_album_artist_name",
                         hover_data={"artist_popularity": ":.0f", "val": False, "streams": True},
                         labels={"artist_popularity": "Spotify Popularity (0–100)", "streams": "Streams"},
                         color_discrete_sequence=[SPOTIFY["green"]])
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color=SPOTIFY["green_light"])))
        
        # Clearer quadrant lines (peer feedback)
        fig.add_vline(x=50, line_dash="dash", line_color=SPOTIFY["border"], opacity=0.5)
        max_y = artist_agg["val"].max()
        fig.add_vrect(x0=0, x1=50, fillcolor="rgba(29,185,84,0.04)", line_width=0)
        fig.add_annotation(x=25, y=max_y*0.92, text="🎯 Niche gems", showarrow=False,
                          font=dict(size=10, color=SPOTIFY["green"]))
        fig.add_annotation(x=75, y=max_y*0.92, text="🌟 Mainstream faves", showarrow=False,
                          font=dict(size=10, color=SPOTIFY["text_muted"]))
        fig.update_xaxes(title="Spotify Popularity", range=[-5, 105])
        fig.update_yaxes(title=measure)
        st.plotly_chart(style_fig(fig, height=350), use_container_width=True, key="niche", config=PLOTLY_CONFIG)
        
        # Quick stat
        niche_pct = (artist_agg["artist_popularity"] < 50).mean() * 100
        st.caption(f"**{niche_pct:.0f}%** of your artists have a Spotify popularity below 50 — {'a true underground explorer!' if niche_pct > 50 else 'you balance mainstream and niche well.'}")

with col2:
    section_header("📈", "Billboard", "Your top artists & tracks ranked")
    
    tab1, tab2 = st.tabs(["🎤 Artists", "🎵 Songs"])
    
    bill_df = df_f.dropna(subset=["master_metadata_album_artist_name"]).copy()
    bill_df["m"] = measure_value(bill_df, measure)
    unit_label = "min" if measure == "Minutes" else ""
    
    with tab1:
        bill_artists = bill_df.groupby("master_metadata_album_artist_name", as_index=False)["m"].sum().sort_values("m", ascending=False).head(8)
        if len(bill_artists) > 0:
            max_val = bill_artists["m"].max()
            html = ""
            for idx, (_, row) in enumerate(bill_artists.iterrows()):
                pct = (row["m"] / max_val) * 100
                val_str = f"{row['m']:,.0f} {unit_label}".strip() if measure == "Minutes" else fmt_number(row['m'])
                html += f"""<div class="billboard-item">
                    <span class="billboard-rank">{idx+1}</span>
                    <span class="billboard-name">{row['master_metadata_album_artist_name']}</span>
                    <div class="billboard-bar"><div class="billboard-bar-fill" style="width:{pct}%;"></div></div>
                    <span class="billboard-value">{val_str}</span>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)
    
    with tab2:
        bill_tracks = df_f.dropna(subset=["master_metadata_track_name", "master_metadata_album_artist_name"]).copy()
        bill_tracks["m"] = measure_value(bill_tracks, measure)
        bill_tracks = bill_tracks.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"],
                                          as_index=False)["m"].sum().sort_values("m", ascending=False).head(8)
        if len(bill_tracks) > 0:
            max_val = bill_tracks["m"].max()
            html = ""
            for idx, (_, row) in enumerate(bill_tracks.iterrows()):
                pct = (row["m"] / max_val) * 100
                name = row['master_metadata_track_name'][:25] + "…" if len(row['master_metadata_track_name']) > 25 else row['master_metadata_track_name']
                val_str = f"{row['m']:,.0f} {unit_label}".strip() if measure == "Minutes" else fmt_number(row['m'])
                html += f"""<div class="billboard-item">
                    <span class="billboard-rank">{idx+1}</span>
                    <span class="billboard-name" title="{row['master_metadata_track_name']} — {row['master_metadata_album_artist_name']}">{name}</span>
                    <div class="billboard-bar"><div class="billboard-bar-fill" style="width:{pct}%;"></div></div>
                    <span class="billboard-value">{val_str}</span>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)

# ====================================================
# KEY TAKEAWAYS — narrative style
# ====================================================
st.markdown("---")
section_header("💡", "Your Listening Profile", "A summary of your musical fingerprint")

# Ensure discovery metrics are always available
try:
    _ = pct_new_artists
except NameError:
    pct_new_artists, pct_new_tracks, new_artists_count, new_tracks_count = compute_discovery(df, df_f)

avg_pop = df_f["artist_popularity"].dropna().mean() if df_f["artist_popularity"].notna().any() else 50
skip_rate = df_f["skipped"].mean() * 100 if len(df_f) > 0 else 0
peak_hour = hour_agg.loc[hour_agg["m"].idxmax(), "hour"] if len(hour_agg) > 0 else 12

pop_label = "Mainstream 🌟" if avg_pop > 60 else ("Balanced 🎭" if avg_pop > 40 else "Indie 🎯")
skip_label = "Picky 🎯" if skip_rate > 20 else ("Selective 👀" if skip_rate > 10 else "Loyal 💚")
hour_label = "Night owl 🦉" if peak_hour >= 22 or peak_hour < 6 else ("Early bird 🌅" if peak_hour < 12 else "Afternoon listener ☀️")

# Top genre
top_genre_series = df_f.dropna(subset=["genre_bucket"]).groupby("genre_bucket")["ms_played"].sum().sort_values(ascending=False)
top_genre = top_genre_series.index[0] if len(top_genre_series) > 0 else "Unknown"

days_in_range = (end_date - start_date).days + 1
avg_daily_min = total_minutes / days_in_range if days_in_range > 0 else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Taste Profile</div>
        <div class="kpi-value" style="font-size:1.2rem;">{pop_label}</div>
        <div class="kpi-trend">avg popularity {avg_pop:.0f}/100</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Skip Behavior</div>
        <div class="kpi-value" style="font-size:1.2rem;">{skip_label}</div>
        <div class="kpi-trend">{skip_rate:.1f}% skip rate</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Peak Time</div>
        <div class="kpi-value" style="font-size:1.2rem;">{hour_label}</div>
        <div class="kpi-trend">most active at {int(peak_hour):02d}:00</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Top Genre</div>
        <div class="kpi-value" style="font-size:1.2rem;">{top_genre}</div>
        <div class="kpi-trend">dominant genre bucket</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Daily Average</div>
        <div class="kpi-value">{fmt_hours(avg_daily_min)}</div>
        <div class="kpi-trend">per day</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================================================
# FOOTER
# ====================================================
st.markdown(f"""
<div style="text-align:center; margin-top:40px; padding:20px; color:{SPOTIFY['text_muted']}; font-size:0.75rem;">
    🎧 Musical Fingerprint · {start_date} → {end_date} · {total_streams:,} plays · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
