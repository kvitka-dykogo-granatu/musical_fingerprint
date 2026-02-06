import streamlit as st

st.set_page_config(
    page_title="About - Musical Fingerprint",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    .stApp {{ background: linear-gradient(180deg, {SPOTIFY["bg_dark"]} 0%, #0a0a0a 100%); }}
    .main .block-container {{ padding: 1.5rem 2rem 2rem 2rem; max-width: 1000px; }}
    #MainMenu, footer {{ visibility: hidden; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    h1, h2, h3 {{ color: {SPOTIFY["white"]} !important; letter-spacing: -0.02em; }}
    p, li {{ color: {SPOTIFY["text_secondary"]} !important; line-height: 1.7; }}
    strong {{ color: {SPOTIFY["white"]} !important; }}
    
    .about-title {{
        font-size: 2rem; font-weight: 900;
        background: linear-gradient(135deg, {SPOTIFY["white"]} 0%, {SPOTIFY["green"]} 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        margin-bottom: 4px;
    }}
    .about-subtitle {{ color: {SPOTIFY["text_secondary"]}; font-size: 0.95rem; margin-bottom: 24px; }}
    
    .section {{
        background: {SPOTIFY["bg_card"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }}
    .section h3 {{
        font-size: 1.1rem !important;
        margin-bottom: 8px !important;
        display: flex; align-items: center; gap: 10px;
    }}
    .section p {{
        font-size: 0.88rem !important;
        margin-bottom: 6px !important;
    }}
    .badge {{
        display: inline-block;
        background: {SPOTIFY["bg_elevated"]};
        border: 1px solid {SPOTIFY["border"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.75rem;
        color: {SPOTIFY["green"]};
        margin-right: 4px;
        margin-bottom: 4px;
    }}
    .swatch {{
        display: inline-block;
        width: 14px; height: 14px;
        border-radius: 3px;
        vertical-align: middle;
        margin-right: 4px;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 class="about-title">📖 About This Dashboard</h1>
<p class="about-subtitle">Design rationale explained through the Dashboard Design Cheatsheet categories</p>
""", unsafe_allow_html=True)

st.markdown(f"""
<a href="/" target="_self" style="
    display: inline-block; padding: 8px 16px; margin-bottom: 16px;
    background: {SPOTIFY['bg_elevated']}; border: 1px solid {SPOTIFY['border']};
    border-radius: 20px; color: {SPOTIFY['white']}; text-decoration: none;
    font-size: 0.82rem; font-weight: 500; font-family: 'DM Sans', sans-serif;
" onmouseover="this.style.background='{SPOTIFY['bg_highlight']}'"
   onmouseout="this.style.background='{SPOTIFY['bg_elevated']}'">
    🎧 ← Back to Dashboard
</a>
""", unsafe_allow_html=True)

# ── 1. DATA ──
st.markdown(f"""
<div class="section">
    <h3>📊 Data</h3>
    <p>
        <span class="badge">Personal data</span>
        <span class="badge">Aggregated</span>
        <span class="badge">Derived values</span>
        <span class="badge">Enriched</span>
    </p>
    <p>
        <strong>Primary source</strong>: Personal Spotify Extended Streaming History obtained via a GDPR data request. Each row represents one stream event with fields including timestamp (<code>ts</code>), track/artist/album names, milliseconds played (<code>ms_played</code>), and a skip flag. The data spans multiple years of real listening behavior.
    </p>
    <p>
        <strong>Enrichment</strong>: The raw history was enriched through the Spotify Web API with two additional fields per track - <strong>artist popularity</strong> (0–100 score) and <strong>artist genres</strong> (freeform tags like "progressive electro house"). These freeform genre tags were then manually bucketed into 10 high-level genre categories (e.g., "progressive electro house" → "EDM & Progressive") to enable meaningful genre-level analysis.
    </p>
    <p>
        <strong>Secondary source</strong>: An optional Life Events CSV providing personal context (semester dates, exam periods, travels) with columns <code>start_date, end_date, label, category</code>. A demo events file is included by default.
    </p>
    <p>
        <strong>Derived metrics</strong>: Several metrics are computed at runtime and do not exist in the raw data: listening sessions (inferred via a 15-minute inactivity gap), discovery rate (comparing each stream's first-ever occurrence against full history), listening streaks (consecutive days with any activity), and monthly artist/track rankings.
    </p>
    <p>
        <strong>Demo mode</strong>: A demo dataset is included for public exploration. Users can upload their own enriched CSV to see their personal fingerprint.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 2. STRUCTURE ──
st.markdown(f"""
<div class="section">
    <h3>🏗️ Structure</h3>
    <p>
        <span class="badge">Single-page dashboard</span>
        <span class="badge">Top-down narrative</span>
        <span class="badge">Adaptive layout</span>
    </p>
    <p>
        The dashboard follows a <strong>single-page, vertically scrollable</strong> structure because it tells one continuous story: "What does my listening look like?" The viewer scrolls top-to-bottom through a logical progression - from high-level summary numbers, to temporal patterns, to content deep-dives (genres, artists), to a final listening profile. This avoids the context-switching of multi-page designs and keeps the entire "fingerprint" in one flow.
    </p>
    <p>
        The dashboard uses an <strong>adaptive layout</strong> that changes based on the selected time range. In Lifetime mode, the calendar heatmap gets full width (it spans years of data), and the No.1 artist/track cards are paired with compact rank-over-time sparklines. In filtered modes (30d–Year), the layout is more compact with discovery rate cards visible, since discovery percentages are more meaningful over shorter windows.
    </p>
    <p>
        The only separate page is this About page, which is informational and accessible via a link in the dashboard header.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 3. VISUAL REPRESENTATION ──
st.markdown(f"""
<div class="section">
    <h3>📈 Visual Representations I Chose</h3>
    <p>
        <span class="badge">Detailed visualization</span>
        <span class="badge">Miniature charts</span>
        <span class="badge">Numbers</span>
        <span class="badge">Progress bars</span>
        <span class="badge">Hierarchical</span>
    </p>
    <p>
        Each visualization was chosen to match its data type and the specific question it answers:
    </p>
    <p>
        <strong>KPI cards</strong> (streams, listening time, unique tracks, artists, albums, skip time, best streak) - single-number displays providing immediate orientation before any charts. These answer "how much did I listen overall?"
    </p>
    <p>
        <strong>Polar bar chart (Listening Clock)</strong> - uses circular form to naturally encode the 24-hour cycle. Radial length maps to listening volume by hour, making peak times immediately visible. More intuitive than a linear bar chart for cyclical time data.
    </p>
    <p>
        <strong>Histogram (Sessions)</strong> - shows the distribution of listening session durations in bucketed bars (&lt;15m, 15–30m, 30m–1h, 1–2h, 2–4h, 4h+). Sessions are inferred from the data using a 15-minute inactivity gap.
    </p>
    <p>
        <strong>GitHub-style heatmap (Commit-ment to Music)</strong> - maps each day to a cell in a week × month grid, with green color intensity encoding listening volume. This leverages spatial memory (weekday patterns) and enables rapid recognition of habits, inactive periods, and streaks. Uses ISO week numbering to handle year boundaries correctly. Doubles as a filter control via box-select.
    </p>
    <p>
        <strong>Rank sparklines (Lifetime mode)</strong> - two compact line charts showing how the No.1 artist and No.1 track ranked each month over the full history. These pair with the No.1 cards to the left, answering "how consistently dominant were they?"
    </p>
    <p>
        <strong>Stacked area chart (Old vs New)</strong> - shows the proportion of first-ever-heard tracks vs. revisited tracks each month. The stacked form communicates both the total and the composition. "New" is defined against the <em>full</em> listening history, not just the filtered window.
    </p>
    <p>
        <strong>Discovery Rate cards</strong> (filtered modes) - two percentage cards showing what share of artists and tracks in the selected period were heard for the very first time. Answer "how exploratory was I?"
    </p>
    <p>
        <strong>Sunburst (Top Artists → Tracks)</strong> - two-level radial hierarchy (artist → tracks) where angular size encodes listening volume. Shows both cross-artist comparison and within-artist track breakdown. Click an artist ring to zoom in for details.
    </p>
    <p>
        <strong>Treemap (Genre Map)</strong> - part-to-whole hierarchical display of genre buckets → sub-genres. Area encodes volume, genre bucket labels include their percentage of total listening. Sub-genres within each bucket use intensity gradients (darker = less, brighter = more). Top-8 sub-genres per bucket are shown, remaining grouped as "Other."
    </p>
    <p>
        <strong>Stacked area / stream chart (Genre Evolution)</strong> - the centerpiece visualization showing how genre proportions shift month over month. Reveals temporal trends in taste that no snapshot can capture. Genre stacking order is optimized so similar colors are never adjacent.
    </p>
    <p>
        <strong>Scatter plot (Niche Score)</strong> - maps Spotify popularity (x) vs. personal listening volume (y) with bubble size encoding stream count. A vertical reference line at popularity = 50 and subtle annotations make the niche-vs-mainstream distribution immediately readable.
    </p>
    <p>
        <strong>Billboard lists</strong> - custom HTML ranked lists with inline gradient bar fills showing relative volume. A familiar "Top 8" format that is instantly understandable, following the global Streams/Minutes measure toggle.
    </p>
    <p>
        <strong>Listening Profile cards</strong> - summary cards at the bottom (Taste Profile, Skip Behavior, Peak Time, Top Genre, Daily Average) that synthesize the entire fingerprint into five quick takeaways with emoji labels.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 4. PAGE LAYOUT ──
st.markdown(f"""
<div class="section">
    <h3>📐 Page Layout</h3>
    <p>
        <span class="badge">Grouped</span>
        <span class="badge">Stratified</span>
        <span class="badge">Adaptive</span>
    </p>
    <p>
        The layout follows a <strong>top-to-bottom narrative</strong> grouped into logical rows:
    </p>
    <p>
        <strong>Filters</strong> - global controls pinned at the top: time preset radio (30d / 90d / 180d / Year / Lifetime), date range picker, Streams/Minutes toggle, Demo data and Life events checkboxes. These affect the entire dashboard.<br>
        <strong>KPIs</strong> - seven headline numbers providing immediate context.<br>
        <strong>Temporal row</strong> - Listening Clock, Sessions, Calendar Heatmap (+ rank sparklines in Lifetime mode) answer "when and how long?"<br>
        <strong>Content row</strong> - No.1 artist/track, Discovery Rate, Old vs New answer "what do I listen to and how much is new?"<br>
        <strong>Genre hierarchy</strong> - Sunburst and Treemap side-by-side for hierarchical exploration.<br>
        <strong>Genre Evolution</strong> - full-width stream chart, placed under the treemap for natural genre → genre-over-time reading order.<br>
        <strong>Deep dives</strong> - Niche Score scatter plot and Billboard ranked lists.<br>
        <strong>Profile</strong> - summary cards synthesizing five key insights.
    </p>
    <p>
        Columns within each row are sized proportionally to information density. The heatmap and Genre Evolution get extra width because they encode many data points across time. Compact visualizations (Clock, Sessions) stay small to avoid wasting space.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 5. SCREENSPACE ──
st.markdown(f"""
<div class="section">
    <h3>🖥️ Screenspace Use</h3>
    <p>
        <span class="badge">Wide layout</span>
        <span class="badge">Vertical scroll</span>
        <span class="badge">Proportional columns</span>
    </p>
    <p>
        The dashboard uses Streamlit's <code>layout="wide"</code> mode (max-width 1600px) to maximize horizontal space. Vertical scrolling is the primary navigation - each row of charts fits roughly within one viewport height so the viewer sees a complete "section" at a time.
    </p>
    <p>
        <strong>Wide visuals</strong> are reserved for temporal patterns that benefit from horizontal extent: the calendar heatmap (full-width in Lifetime mode), Genre Evolution stream chart, and Old vs New area chart. <strong>Compact visuals</strong> like the Listening Clock, Session histogram, and KPI cards are kept small since they show simple distributions or single values.
    </p>
    <p>
        The <strong>adaptive layout</strong> reconfigures the first analytical row based on time range: Lifetime mode gives the heatmap full width (spanning years of data needs the space), while filtered modes use a compact 3-column arrangement where the heatmap shares a row with Clock and Sessions.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 6. INTERACTION ──
st.markdown(f"""
<div class="section">
    <h3>🖱️ Interaction</h3>
    <p>
        <span class="badge">Filter &amp; Focus</span>
        <span class="badge">Direct manipulation</span>
        <span class="badge">Detail on demand</span>
        <span class="badge">Drill-down</span>
        <span class="badge">Personalization</span>
    </p>
    <p>
        <strong>Global filtering</strong> - time presets (30d / 90d / 180d / Year / Lifetime), a date range picker, and a Streams/Minutes measure toggle re-slice the entire dashboard. All charts, KPIs, and derived metrics update simultaneously. This enables temporal comparison (e.g., "Did I discover more music this summer than last year?").
    </p>
    <p>
        <strong>Heatmap direct manipulation</strong> - the GitHub-style heatmap supports box-select: dragging over a range of days filters all charts below to show only that selection. This makes the heatmap both a visualization <em>and</em> a filter control - a direct manipulation pattern where the same element serves double duty.
    </p>
    <p>
        <strong>Detail-on-demand (tooltips)</strong> - every chart has rich hover tooltips showing exact values, formatted durations (e.g., "3h 42m"), date labels, and contextual information. The Genre Evolution uses "x unified" hover mode showing all genres for a given month in a single tooltip. Plotly mode bars are hidden to keep the interface clean.
    </p>
    <p>
        <strong>Drill-down (treemap &amp; sunburst)</strong> - clicking a genre bucket in the treemap reveals its sub-genres; clicking the center returns to the overview. The sunburst similarly supports clicking an artist ring to focus on their tracks. This provides progressive disclosure without cluttering the initial view.
    </p>
    <p>
        <strong>Life events overlay</strong> - toggling "Life events" overlays labeled shaded regions (semesters, exam periods, travels) on the Genre Evolution and Old vs New charts. This connects listening patterns to real-world context (e.g., "I explored more new music during summer break"). Users can upload their own events CSV when demo mode is off.
    </p>
    <p>
        <strong>Billboard tabs</strong> - the Billboard section uses tabs (Artists / Songs) to show two rankings in the same space, keeping the layout clean.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 7. META DATA ──
st.markdown(f"""
<div class="section">
    <h3>🏷️ Metadata</h3>
    <p>
        <span class="badge">Titles &amp; subtitles</span>
        <span class="badge">Annotations</span>
        <span class="badge">Legends</span>
        <span class="badge">Data source info</span>
    </p>
    <p>
        <strong>Titles and subtitles</strong>: Every chart section has a title and a descriptive subtitle explaining what it shows and how to read it (e.g., "Daily listening - drag-select days to filter the whole dashboard"). These serve as built-in documentation so the viewer never needs external help.
    </p>
    <p>
        <strong>Inline annotations</strong>: The Niche Score chart includes a vertical divider at popularity = 50 with "Niche gems" and "Mainstream faves" labels, plus a percentage caption below. The Listening Profile cards include threshold explanations in their trend lines (e.g., "avg popularity 60/100"). Genre bucket names in the treemap include their percentage of total listening.
    </p>
    <p>
        <strong>Legends</strong>: The Genre Evolution stream chart has a horizontal legend above the chart. The heatmap has a vertical color bar with labeled scale. Genre colors are consistent across treemap, stream chart, and legend so the viewer builds a stable mental mapping.
    </p>
    <p>
        <strong>Data source</strong>: Users can toggle between demo data and their own upload. The footer shows the active date range, total play count, and tools used. This About page provides complete design documentation.
    </p>
    <p>
        <strong>Life events labels</strong>: When enabled, life events appear as labeled shaded regions on time-series charts, providing named external context for listening patterns.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 8. COLOR ──
st.markdown(f"""
<div class="section">
    <h3>🎨 Color Use</h3>
    <p>
        <span class="badge">Brand semantic</span>
        <span class="badge">Categorical distinct</span>
        <span class="badge">Sequential encoding</span>
        <span class="badge">Intensity gradients</span>
    </p>
    <p>
        <strong>Brand palette</strong>: The entire dashboard uses Spotify's visual language - dark background (#121212), signature green (#1DB954), and neutral grays - creating an immediately recognizable context. Green consistently means "primary" or "active" (play counts, highlights, fills), while gray means "secondary" or "baseline."
    </p>
    <p>
        <strong>Categorical genre palette</strong> - 10 distinct hues for genre buckets, chosen to maximize perceptual contrast between adjacent genres in the stacked area chart:
    </p>
    <p>
        <span class="swatch" style="background:#1DB954;"></span> EDM & Progressive &nbsp;
        <span class="swatch" style="background:#EF4444;"></span> Rock / Metal / Core &nbsp;
        <span class="swatch" style="background:#F59E0B;"></span> Lo-Fi / Chillhop &nbsp;
        <span class="swatch" style="background:#3B82F6;"></span> Soundtrack / Score &nbsp;
        <span class="swatch" style="background:#EC4899;"></span> Pop & Regional Pop<br>
        <span class="swatch" style="background:#2D6A4F;"></span> Folk / Acoustic / Celtic &nbsp;
        <span class="swatch" style="background:#F97316;"></span> Hip-Hop / Rap &nbsp;
        <span class="swatch" style="background:#8B5CF6;"></span> Trance &nbsp;
        <span class="swatch" style="background:#06B6D4;"></span> Electronica / Chill &nbsp;
        <span class="swatch" style="background:#6B7280;"></span> Others
    </p>
    <p>
        These colors are consistent across the Genre Evolution stream chart, treemap, and genre legend. The stacking order in the stream chart is deliberately arranged so that similar colors (e.g., green and dark forest green, pink and red, blue and cyan) are never adjacent.
    </p>
    <p>
        <strong>Intensity gradients in treemap</strong>: Within each genre bucket, sub-genre tiles use brightness gradients of the parent color (darker → brighter = less → more listening). This preserves categorical association while encoding quantitative data within the hierarchy.
    </p>
    <p>
        <strong>Sequential scale (heatmap)</strong>: The calendar heatmap uses a dark-to-bright green gradient mirroring GitHub's contribution graph, which most technical viewers already understand. Zero-activity days match the background, while peak days are bright green.
    </p>
    <p>
        <strong>Sunburst</strong>: Uses a three-shade green palette (#1DB954, #15803D, #166534) for the top 3 artists, keeping it cohesive with the dashboard's Spotify theme.
    </p>
    <p>
        <strong>Life events</strong>: Overlays use semi-transparent category colors (blue for semesters, red for exams, orange for travel, purple for personal) that are distinct from the genre palette to avoid confusion.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Limitations ──
st.markdown(f"""
<div class="section">
    <h3>⚠️ Limitations & Trade-offs</h3>
    <p>
        <strong>Data gaps</strong>: Spotify's extended history lacks audio features (valence, energy, danceability), which would enable mood-based analyses. Genre labels are artist-level and may not reflect individual song styles accurately.
    </p>
    <p>
        <strong>Session heuristic</strong>: Listening sessions are inferred using a 15-minute gap - if more than 15 minutes pass between streams, a new session begins. This is an approximation and may split or merge sessions inaccurately.
    </p>
    <p>
        <strong>Genre bucketing</strong>: Genre buckets are manually mapped from Spotify's freeform tags. This involves subjective choices and some artists span multiple buckets. The "Others" bucket is a catch-all for genres that don't fit neatly.
    </p>
    <p>
        <strong>Streamlit constraints</strong>: As a Streamlit app, layout switching between Lifetime and filtered modes causes a full page re-render (no smooth CSS transitions). The heatmap box-select uses Plotly's event system which can vary across browsers.
    </p>
    <p>
        <strong>Privacy</strong>: The demo dataset ships with the dashboard. Users uploading their own data keep it local to their session - nothing is stored server-side.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; margin-top:30px; padding:16px; color:{SPOTIFY['text_muted']}; font-size:0.75rem;">
    📖 Musical Fingerprint - Design Explanation · Built with Streamlit & Plotly · Dashboard Design Cheatsheet framework
</div>
""", unsafe_allow_html=True)
