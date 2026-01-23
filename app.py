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
# Custom CSS (from v2)
# ----------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
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
    
    /* Header */
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
        min-width: 130px;
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
    
    /* Section Card (from v3) */
    .section-card {{
        background: {SPOTIFY["bg_card"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }}
    
    .section-card-title {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {SPOTIFY["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    /* Section header (from v2) */
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
    
    /* Top item cards */
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
    
    .top-item-card:hover {{
        border-color: {SPOTIFY["green"]};
    }}
    
    .play-icon {{
        width: 36px;
        height: 36px;
        background: {SPOTIFY["green"]};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {SPOTIFY["bg_dark"]};
        font-size: 14px;
        flex-shrink: 0;
    }}
    
    .top-item-name {{
        font-weight: 600;
        color: {SPOTIFY["white"]};
        font-size: 0.9rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    .top-item-sub {{
        font-size: 0.75rem;
        color: {SPOTIFY["text_muted"]};
        margin-top: 2px;
    }}
    
    /* Billboard */
    .billboard-item {{
        display: flex;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(64, 64, 64, 0.2);
        gap: 10px;
    }}
    
    .billboard-item:last-child {{
        border-bottom: none;
    }}
    
    .billboard-rank {{
        font-size: 1rem;
        font-weight: 700;
        color: {SPOTIFY["text_muted"]};
        width: 20px;
        text-align: center;
    }}
    
    .billboard-name {{
        flex: 1;
        font-size: 0.8rem;
        color: {SPOTIFY["white"]};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        min-width: 0;
    }}
    
    .billboard-bar {{
        width: 80px;
        height: 6px;
        background: {SPOTIFY["bg_highlight"]};
        border-radius: 3px;
        overflow: hidden;
        flex-shrink: 0;
    }}
    
    .billboard-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, {SPOTIFY["green"]} 0%, {SPOTIFY["green_light"]} 100%);
        border-radius: 3px;
    }}
    
    .billboard-value {{
        font-size: 0.75rem;
        color: {SPOTIFY["text_secondary"]};
        width: 50px;
        text-align: right;
        flex-shrink: 0;
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: {SPOTIFY["border"]};
        margin: 16px 0;
        opacity: 0.5;
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        flex-direction: row !important;
        gap: 4px !important;
        background: {SPOTIFY["bg_elevated"]};
        padding: 4px;
        border-radius: 8px;
        border: 1px solid {SPOTIFY["border"]};
    }}
    
    .stRadio > div > label {{
        background: transparent !important;
        border: none !important;
        padding: 6px 12px !important;
        margin: 0 !important;
        border-radius: 6px !important;
        color: {SPOTIFY["text_secondary"]} !important;
        font-size: 0.8rem !important;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .stRadio > div > label:hover {{
        background: {SPOTIFY["bg_highlight"]} !important;
        color: {SPOTIFY["white"]} !important;
    }}
    
    .stRadio > div > label[data-checked="true"] {{
        background: {SPOTIFY["green"]} !important;
        color: {SPOTIFY["bg_dark"]} !important;
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        background: {SPOTIFY["bg_elevated"]} !important;
        border-color: {SPOTIFY["border"]} !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: {SPOTIFY["bg_elevated"]};
        padding: 3px;
        border-radius: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 6px;
        color: {SPOTIFY["text_secondary"]};
        padding: 6px 14px;
        font-size: 0.8rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {SPOTIFY["green"]} !important;
        color: {SPOTIFY["bg_dark"]} !important;
    }}
    
    /* Toggle */
    div[data-testid="stCheckbox"] label span {{
        color: {SPOTIFY["text_secondary"]} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper Functions
# ----------------------------
REQUIRED_COLS = ["ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name",
                 "master_metadata_album_album_name", "artist_popularity", "artist_genres", "genre_bucket", "skipped"]

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
        <span style="font-size: 1.1rem;">{icon}</span>
        <span class="section-title">{title}</span>
    </div>''', unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)

def style_fig(fig, height=300, show_legend=False):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=SPOTIFY["text_secondary"], family="DM Sans", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=show_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        hoverlabel=dict(bgcolor=SPOTIFY["bg_elevated"], font_size=11, bordercolor=SPOTIFY["border"])
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(64,64,64,0.2)", zeroline=False, tickfont=dict(size=9))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(64,64,64,0.2)", zeroline=False, tickfont=dict(size=9))
    return fig

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
        df[c] = df[c].apply(clean_string)
    
    df["track_id"] = df.apply(lambda r: f"{r['master_metadata_album_artist_name']}§{r['master_metadata_track_name']}" 
                              if r['master_metadata_track_name'] and r['master_metadata_album_artist_name'] else None, axis=1)
    return df

def measure_value(df, measure):
    return pd.Series(np.ones(len(df)), index=df.index) if measure == "Streams" else df["ms_played"] / 60000

def fmt_number(n):
    try:
        if abs(n) >= 1e6: return f"{n/1e6:.1f}M"
        if abs(n) >= 1e3: return f"{n/1e3:.1f}K"
        return f"{int(n):,}" if float(n).is_integer() else f"{n:.1f}"
    except: return str(n)

@st.cache_data
def compute_discovery(df_full, df_filtered):
    """Compute discovery metrics: % of new artists/tracks in filtered period"""
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
def compute_old_vs_new_monthly_fixed(df_full, start_date, end_date):
    """
    FIXED: Compute old vs new using FULL dataset for first listen detection,
    then filter to display only the selected period (zoom effect)
    """
    df_clean = df_full.dropna(subset=["track_id"]).copy()
    if len(df_clean) == 0: return pd.DataFrame()
    
    # Get first listen from FULL dataset (not filtered)
    first_listen = df_clean.groupby("track_id")["ts"].min().reset_index()
    first_listen.columns = ["track_id", "first_listen_ts"]
    first_listen["first_listen_month"] = pd.to_datetime(first_listen["first_listen_ts"]).dt.to_period("M").astype(str)
    
    # Group by month for full dataset
    track_months = df_clean.groupby(["month", "track_id"]).size().reset_index(name="play_count")
    track_months = track_months.merge(first_listen[["track_id", "first_listen_month"]], on="track_id")
    track_months["is_new"] = track_months["month"] == track_months["first_listen_month"]
    
    monthly_counts = track_months.groupby(["month", "is_new"]).agg(unique_tracks=("track_id", "nunique")).reset_index()
    pivot = monthly_counts.pivot(index="month", columns="is_new", values="unique_tracks").fillna(0)
    
    if False in pivot.columns and True in pivot.columns:
        pivot.columns = ["Old tracks", "New tracks"]
    pivot = pivot.reset_index()
    
    # Filter to selected date range (zoom effect)
    start_month = pd.Timestamp(start_date).to_period("M").strftime("%Y-%m")
    end_month = pd.Timestamp(end_date).to_period("M").strftime("%Y-%m")
    pivot = pivot[(pivot["month"] >= start_month) & (pivot["month"] <= end_month)]
    
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

def bins_session_minutes(x):
    if x < 120: return "<2h"
    if x < 240: return "2–4h"
    if x < 360: return "4–6h"
    return ">6h"

def create_gauge(value, max_val=100):
    """Create a half-circle gauge chart (from v3)"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 32, "color": SPOTIFY["white"]}},
        gauge={
            "axis": {"range": [0, max_val], "visible": False},
            "bar": {"color": SPOTIFY["green"], "thickness": 0.8},
            "bgcolor": SPOTIFY["bg_highlight"],
            "borderwidth": 0,
        }
    ))
    fig.update_layout(
        height=130,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig

st.markdown(f"""
<div class="dashboard-header">
    <span class="fingerprint-icon">🎧</span>
    <div>
        <h1 class="dashboard-title">Musical Fingerprint</h1>
        <p class="dashboard-subtitle">Your unique listening DNA — patterns, genres, discoveries & obsessions</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1, 0.6, 0.8])

with filter_col1:
    time_options = ["30 days", "90 days", "180 days", "Year", "Lifetime"]
    selected_time = st.radio("Time", time_options, index=4, horizontal=True, label_visibility="collapsed")

with filter_col4:
    use_demo = st.checkbox("Use demo data", value=True)
    if not use_demo:
        uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")
    else:
        uploaded_file = None

# Load data
try:
    if use_demo:
        df = load_csv(path="music_data.csv")
    elif uploaded_file:
        df = load_csv(uploaded_file=uploaded_file)
    else:
        st.info("Please upload a CSV file or enable demo data")
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
    
    date_range = st.date_input("Dates", (default_start, default_end), min_value=min_date, max_value=max_date, label_visibility="collapsed")
    start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (default_start, default_end)

with filter_col3:
    measure = st.selectbox("Measure", ["Streams", "Minutes"], label_visibility="collapsed")

# Filter data
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_f = df[mask].copy()

if len(df_f) == 0:
    st.warning("No data in selected range")
    st.stop()

# ----------------------------
# KPI ROW
# ----------------------------
total_streams = len(df_f)
total_minutes = df_f["ms_played"].sum() / 60000
total_hours = total_minutes / 60
n_tracks = df_f["track_id"].dropna().nunique()
n_artists = df_f["master_metadata_album_artist_name"].dropna().nunique()
n_albums = df_f["master_metadata_album_album_name"].dropna().nunique()
avg_skip_time = df_f[df_f["skipped"]]["ms_played"].mean() / 1000 if df_f["skipped"].any() else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Streams</div>
        <div class="kpi-value">{fmt_number(total_streams)}</div>
        <div class="kpi-trend">total plays</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Hours</div>
        <div class="kpi-value">{total_hours:,.1f}</div>
        <div class="kpi-trend">{total_minutes:,.0f} min</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Tracks</div>
        <div class="kpi-value">{fmt_number(n_tracks)}</div>
        <div class="kpi-trend">unique songs</div>
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
        <div class="kpi-value">{avg_skip_time:.1f}s</div>
        <div class="kpi-trend">avg before skip</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# ROW 1: Clock | Sessions | Calendar
# ----------------------------
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    section_header("🕐", "Listening Clock", "When you listen most (by hour)")
    
    by_hour = df_f.copy()
    by_hour["m"] = measure_value(by_hour, measure)
    hour_agg = by_hour.groupby("hour", as_index=False)["m"].sum()
    all_hours = pd.DataFrame({"hour": range(24)})
    hour_agg = all_hours.merge(hour_agg, on="hour", how="left").fillna(0)
    
    fig = go.Figure(go.Barpolar(
        r=hour_agg["m"], theta=hour_agg["hour"]*15, width=[14]*24,
        marker_color=SPOTIFY["green"], marker_line_color=SPOTIFY["green_light"], marker_line_width=1, opacity=0.85,
        hovertemplate="%{customdata}:00<br>%{r:,.0f} " + measure.lower() + "<extra></extra>",
        customdata=[f"{h:02d}" for h in hour_agg["hour"]]
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(showticklabels=False, gridcolor="rgba(64,64,64,0.2)"),
            angularaxis=dict(direction="clockwise", rotation=90, tickmode="array",
                tickvals=[i*15 for i in range(0, 24, 3)], ticktext=[f"{i}" for i in range(0, 24, 3)],
                tickfont=dict(size=9, color=SPOTIFY["text_muted"]), gridcolor="rgba(64,64,64,0.2)")),
        margin=dict(l=30, r=30, t=10, b=10)
    )
    st.plotly_chart(style_fig(fig, height=220), use_container_width=True, key="clock_chart")

with col2:
    section_header("⏱️", "Sessions", "Listening session lengths")
    
    df_s = sessionize(df_f, gap_minutes=15)
    if len(df_s) > 0:
        sess = df_s.groupby("session_id", as_index=False).agg(session_minutes=("session_minutes", "first"))
        sess["bin"] = sess["session_minutes"].apply(bins_session_minutes)
        sess_bins = sess.groupby("bin", as_index=False).size().rename(columns={"size": "sessions"})
        order = ["<2h", "2–4h", "4–6h", ">6h"]
        sess_bins["bin"] = pd.Categorical(sess_bins["bin"], categories=order, ordered=True)
        sess_bins = sess_bins.sort_values("bin")
        
        fig = px.bar(sess_bins, x="bin", y="sessions", color_discrete_sequence=[SPOTIFY["green"]])
        fig.update_traces(marker_line_color=SPOTIFY["green_light"], marker_line_width=1,
                         hovertemplate="%{x}<br>%{y} sessions<extra></extra>")
        fig.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(style_fig(fig, height=220), use_container_width=True, key="sessions_chart")

with col3:
    section_header("📅", "Commit-ment to Music", "Daily listening activity (GitHub-style)")
    
    daily = df_f.groupby("date", as_index=False).agg(streams=("ts", "count"), minutes=("ms_played", lambda s: s.sum()/60000))
    daily["value"] = daily["streams"] if measure == "Streams" else daily["minutes"]
    
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    full_grid = pd.DataFrame({'date': all_dates.date, 'week': all_dates.strftime("%Y-W%W"), 'dow': all_dates.dayofweek})
    full_grid = full_grid.merge(daily[['date', 'value']], on='date', how='left').fillna(0)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    full_grid["day_name"] = full_grid["dow"].apply(lambda x: day_names[x])
    
    fig = go.Figure(go.Heatmap(
        x=full_grid["week"], y=full_grid["dow"], z=full_grid["value"],
        colorscale=[[0, SPOTIFY["bg_elevated"]], [0.2, "#0d4429"], [0.4, "#166534"], [0.7, "#22c55e"], [1, SPOTIFY["green_light"]]],
        showscale=False, ygap=3, xgap=3,
        hovertemplate="%{customdata}<br>" + measure + ": %{z:,.0f}<extra></extra>",
        customdata=full_grid["day_name"]
    ))
    fig.update_yaxes(tickvals=list(range(7)), ticktext=day_names, autorange="reversed")
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(margin=dict(l=40, r=10, t=10, b=10))
    st.plotly_chart(style_fig(fig, height=200), use_container_width=True, key="calendar_chart")

# ----------------------------
# ROW 2: No.1 Artist + Artist Gauge | No.1 Track + Track Gauge | Old vs New
# ----------------------------
# Compute discovery metrics first
pct_new_artists, pct_new_tracks, new_artists_count, new_tracks_count = compute_discovery(df, df_f)

col1, col2, col3 = st.columns([1, 1, 1.5])

with col1:
    # No.1 Artist
    section_header("👑", "No.1 Artist", "Most played by time")
    top_artist_df = df_f.dropna(subset=["master_metadata_album_artist_name"]).groupby("master_metadata_album_artist_name")["ms_played"].sum().sort_values(ascending=False)
    if len(top_artist_df) > 0:
        artist_name = top_artist_df.index[0]
        artist_streams = df_f[df_f['master_metadata_album_artist_name'] == artist_name].shape[0]
        artist_mins = top_artist_df.iloc[0] / 60000
        st.markdown(f"""<div class="top-item-card">
            <div class="play-icon">▶</div>
            <div style="flex: 1; min-width: 0;">
                <div class="top-item-name">{artist_name}</div>
                <div class="top-item-sub">{artist_streams:,} streams • {artist_mins:,.0f} min</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    # New Artists Gauge
    section_header("🆕", "New Artists", "First-time artists")
    st.plotly_chart(create_gauge(pct_new_artists), use_container_width=True, key="gauge_artists")
    st.caption(f"{new_artists_count} first-time artists")

with col2:
    # No.1 Track
    section_header("🎵", "No.1 Track", "Most played song")
    top_track_df = df_f.dropna(subset=["master_metadata_track_name", "master_metadata_album_artist_name"]).groupby(["master_metadata_track_name", "master_metadata_album_artist_name"])["ms_played"].sum().sort_values(ascending=False)
    if len(top_track_df) > 0:
        (track_name, track_artist) = top_track_df.index[0]
        track_streams = df_f[(df_f['master_metadata_track_name'] == track_name) & (df_f['master_metadata_album_artist_name'] == track_artist)].shape[0]
        st.markdown(f"""<div class="top-item-card">
            <div class="play-icon">▶</div>
            <div style="flex: 1; min-width: 0;">
                <div class="top-item-name">{track_name}</div>
                <div class="top-item-sub">{track_artist} • {track_streams} plays</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    # New Tracks Gauge
    section_header("🔍", "New Tracks", "First-time tracks")
    st.plotly_chart(create_gauge(pct_new_tracks), use_container_width=True, key="gauge_tracks")
    st.caption(f"{new_tracks_count} first-time tracks")

with col3:
    section_header("🆕", "Old vs New", "Unique songs: first listens vs revisits per month")
    
    #full dataset for first listen detection
    old_new_data = compute_old_vs_new_monthly_fixed(df, start_date, end_date)
    
    if len(old_new_data) > 0 and "Old tracks" in old_new_data.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=old_new_data["month"], y=old_new_data["Old tracks"], name="Old (revisited)",
            line=dict(color=SPOTIFY["text_muted"], width=2), marker=dict(size=5),
            fill="tozeroy", fillcolor="rgba(114, 114, 114, 0.1)"))
        if "New tracks" in old_new_data.columns:
            fig.add_trace(go.Scatter(x=old_new_data["month"], y=old_new_data["New tracks"], name="New (discoveries)",
                line=dict(color=SPOTIFY["green"], width=2), marker=dict(size=5),
                fill="tozeroy", fillcolor="rgba(29, 185, 84, 0.15)"))
        fig.update_layout(xaxis_title="", yaxis_title="", hovermode="x unified")
        st.plotly_chart(style_fig(fig, height=280, show_legend=True), use_container_width=True, key="oldnew_chart")
    else:
        st.info("Not enough data")
    st.caption("Uses full history to determine first listens")

# ----------------------------
# ROW 3: Sunburst | Genre Treemap
# ----------------------------
col1, col2 = st.columns([1, 2])

with col1:
    # Sunburst Chart
    section_header("🌞", "Top Artists → Tracks", "Your top 3 artists and their most played tracks")
    sun_df = df_f.dropna(subset=["master_metadata_album_artist_name", "master_metadata_track_name"]).copy()
    sun_df["m"] = measure_value(sun_df, measure)
    
    artist_totals = sun_df.groupby("master_metadata_album_artist_name")["m"].sum()
    top3 = artist_totals.nlargest(3).index.tolist()
    sun_df = sun_df[sun_df["master_metadata_album_artist_name"].isin(top3)]
    
    sun_agg = sun_df.groupby(["master_metadata_album_artist_name", "master_metadata_track_name"])["m"].sum().reset_index()
    sun_agg = sun_agg.groupby("master_metadata_album_artist_name", group_keys=False).apply(lambda g: g.nlargest(4, "m"))
    
    if len(sun_agg) > 0:
        fig = px.sunburst(sun_agg, path=["master_metadata_album_artist_name", "master_metadata_track_name"], values="m",
                          color="master_metadata_album_artist_name", color_discrete_sequence=[SPOTIFY["green"], "#06B6D4", "#F97316"])
        fig.update_traces(textinfo="label+percent parent", insidetextorientation="radial",
                         hovertemplate="<b>%{label}</b><br>%{value:,.0f} " + measure.lower() + "<extra></extra>")
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        st.plotly_chart(style_fig(fig, height=320), use_container_width=True, key="sunburst_chart")

with col2:
    section_header("🎨", "Genres", "Click a genre to see subgenres, click center to go back")
    
    genre_df = df_f.dropna(subset=["genre_bucket"]).copy()
    genre_df["m"] = measure_value(genre_df, measure)
    
    # Explode subgenres for hierarchical treemap
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
        
        # Create gradient colors for subgenres within each bucket
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        def create_gradient_color(base_hex, intensity):
            """Create a color that's a gradient from dark to the base color"""
            base_rgb = hex_to_rgb(base_hex)
            dark_rgb = (25, 25, 25)
            new_rgb = tuple(dark_rgb[i] + (base_rgb[i] - dark_rgb[i]) * intensity for i in range(3))
            return rgb_to_hex(new_rgb)
        
        # Build complete color map
        color_map = {"(?)": "#1a1a1a", "All Genres": "#1a1a1a"}
        
        # Add bucket colors first
        for bucket in GENRE_COLORS:
            color_map[bucket] = GENRE_COLORS[bucket]
        
        # Calculate gradient colors for each subgenre
        for bucket in treemap_df["genre_bucket"].unique():
            bucket_data = treemap_df[treemap_df["genre_bucket"] == bucket].copy()
            max_m = bucket_data["m"].max()
            min_m = bucket_data["m"].min()
            base_color = GENRE_COLORS.get(bucket, SPOTIFY["green"])
            
            for _, row in bucket_data.iterrows():
                # Intensity range 0.35 to 1.0 to avoid too dark
                if max_m > min_m:
                    intensity = 0.35 + 0.65 * (row["m"] - min_m) / (max_m - min_m)
                else:
                    intensity = 1.0
                color_map[row["subgenre"]] = create_gradient_color(base_color, intensity)
        
        # Create a unique color key for proper coloring
        treemap_df["color_key"] = treemap_df["subgenre"]
        
        fig = px.treemap(
            treemap_df,
            path=[px.Constant("All Genres"), "genre_bucket", "subgenre"],
            values="m",
            color="color_key",
            color_discrete_map=color_map
        )
        
        # Override parent colors explicitly
        fig.update_traces(
            textinfo="label+percent parent",
            textfont=dict(size=12),
            marker=dict(cornerradius=5),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} " + measure.lower() + "<extra></extra>",
            root_color="#1a1a1a"
        )
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        st.plotly_chart(style_fig(fig, height=320), use_container_width=True, key="genre_treemap")

# ----------------------------
# ROW 4: Niche | Billboard
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    section_header("🎯", "Niche Score", "X = Spotify popularity, Y = your listening. Bottom-left = niche!")
    
    niche_df = df_f.dropna(subset=["master_metadata_album_artist_name", "artist_popularity"]).copy()
    niche_df["m"] = measure_value(niche_df, measure)
    artist_agg = niche_df.groupby(["master_metadata_album_artist_name", "artist_popularity"], as_index=False).agg(
        val=("m", "sum"), streams=("ts", "count"))
    
    if len(artist_agg) > 0:
        # no "total" in hover, just artist name, popularity, streams
        fig = px.scatter(artist_agg, x="artist_popularity", y="val", size="streams", size_max=20,
                        hover_name="master_metadata_album_artist_name",
                        hover_data={"artist_popularity": True, "val": False, "streams": True},
                        labels={"artist_popularity": "Popularity", "streams": "Streams"},
                        color_discrete_sequence=[SPOTIFY["green"]])
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color=SPOTIFY["green_light"])))
        fig.add_vline(x=50, line_dash="dash", line_color=SPOTIFY["border"], opacity=0.4)
        max_y = artist_agg["val"].max()
        fig.add_annotation(x=25, y=max_y*0.9, text="🎯 Niche", showarrow=False, font=dict(size=9, color=SPOTIFY["green"]))
        fig.add_annotation(x=75, y=max_y*0.9, text="🌟 Mainstream", showarrow=False, font=dict(size=9, color=SPOTIFY["text_muted"]))
        fig.update_xaxes(title="Popularity")
        fig.update_yaxes(title=measure)
        st.plotly_chart(style_fig(fig, height=280), use_container_width=True, key="niche_chart")

with col2:
    section_header("📈", "Billboard", "Your top artists & songs")
    
    tab1, tab2 = st.tabs(["🎤 Artists", "🎵 Songs"])
    
    # Use same measure calculation as sunburst for consistency
    bill_df = df_f.dropna(subset=["master_metadata_album_artist_name"]).copy()
    bill_df["m"] = measure_value(bill_df, measure)
    
    with tab1:
        # Billboard artists - same calculation as sunburst
        bill_artists = bill_df.groupby("master_metadata_album_artist_name", as_index=False)["m"].sum().sort_values("m", ascending=False).head(5)
        if len(bill_artists) > 0:
            max_val = bill_artists["m"].max()
            html = ""
            for idx, (_, row) in enumerate(bill_artists.iterrows()):
                pct = (row["m"] / max_val) * 100
                html += f"""<div class="billboard-item">
                    <span class="billboard-rank">{idx+1}</span>
                    <span class="billboard-name">{row['master_metadata_album_artist_name']}</span>
                    <div class="billboard-bar"><div class="billboard-bar-fill" style="width:{pct}%;"></div></div>
                    <span class="billboard-value">{fmt_number(row['m'])}</span>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)
    
    with tab2:
        bill_tracks = df_f.dropna(subset=["master_metadata_track_name", "master_metadata_album_artist_name"]).copy()
        bill_tracks["m"] = measure_value(bill_tracks, measure)
        bill_tracks = bill_tracks.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], as_index=False)["m"].sum().sort_values("m", ascending=False).head(5)
        if len(bill_tracks) > 0:
            max_val = bill_tracks["m"].max()
            html = ""
            for idx, (_, row) in enumerate(bill_tracks.iterrows()):
                pct = (row["m"] / max_val) * 100
                name = row['master_metadata_track_name'][:20] + "..." if len(row['master_metadata_track_name']) > 20 else row['master_metadata_track_name']
                html += f"""<div class="billboard-item">
                    <span class="billboard-rank">{idx+1}</span>
                    <span class="billboard-name" title="{row['master_metadata_track_name']}">{name}</span>
                    <div class="billboard-bar"><div class="billboard-bar-fill" style="width:{pct}%;"></div></div>
                    <span class="billboard-value">{fmt_number(row['m'])}</span>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)

# ----------------------------
# KEY TAKEAWAYS 
# ----------------------------
st.markdown("---")
section_header("💡", "Key Takeaways", "Summary of your listening profile")

avg_pop = df_f["artist_popularity"].dropna().mean() if df_f["artist_popularity"].notna().any() else 50
skip_rate = df_f["skipped"].mean() * 100 if len(df_f) > 0 else 0
peak_hour = hour_agg.loc[hour_agg["m"].idxmax(), "hour"] if len(hour_agg) > 0 else 12

# Determine labels with thresholds explained
pop_label = "Mainstream 🌟" if avg_pop > 60 else ("Balanced 🎭" if avg_pop > 40 else "Indie 🎯")
skip_label = "Picky 🎯" if skip_rate > 20 else ("Selective 👀" if skip_rate > 10 else "Loyal 💚")
hour_label = "Night owl 🦉" if peak_hour >= 22 or peak_hour < 6 else ("Early bird 🌅" if peak_hour < 12 else "Afternoon ☀️")

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Avg Popularity ⓘ</div>
        <div class="kpi-value">{avg_pop:.0f}/100</div>
        <div class="kpi-trend">↑ {pop_label}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Skip Rate ⓘ</div>
        <div class="kpi-value">{skip_rate:.1f}%</div>
        <div class="kpi-trend">↑ {skip_label}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Peak Hour ⓘ</div>
        <div class="kpi-value">{int(peak_hour):02d}:00</div>
        <div class="kpi-trend">↑ {hour_label}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("**Avg Popularity**: Spotify's popularity score (0-100) of artists you listen to. <40 = indie, 40-60 = balanced, >60 = mainstream")
st.caption("**Skip Rate**: How often you skip songs. >20% = picky, 10-20% = selective, <10% = loyal listener")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown(f"""
<div style="text-align:center; margin-top:40px; padding:20px; color:{SPOTIFY['text_muted']}; font-size:0.75rem;">
    🎧 Musical Fingerprint • {start_date} to {end_date} • {total_streams:,} plays
</div>
""", unsafe_allow_html=True)
