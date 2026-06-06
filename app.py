import streamlit as st
import pandas as pd
from datetime import date, timedelta
from supabase import create_client
import time

# =========================
# SUPABASE CONFIG
# =========================
SUPABASE_URL = "https://grgefavcsqpmdicuvfvy.supabase.co"
SUPABASE_KEY = "sb_publishable_XWDVocxI3J1wrdAHKLKsEA_6bYZv-gV"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chiya AI · Smart Food Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS — PREMIUM DARK THEME
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --bg-base:       #0b0f0e;
    --bg-card:       #111815;
    --bg-card2:      #161d1a;
    --accent:        #3dffa0;
    --accent-dim:    rgba(61,255,160,0.12);
    --accent-glow:   rgba(61,255,160,0.35);
    --warn:          #ffb347;
    --warn-dim:      rgba(255,179,71,0.12);
    --danger:        #ff5e7a;
    --danger-dim:    rgba(255,94,122,0.12);
    --text-primary:  #eaf5ee;
    --text-muted:    #6b8c79;
    --border:        rgba(61,255,160,0.10);
    --radius:        16px;
    --radius-sm:     10px;
}

/* ── GLOBAL RESET ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-base) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--bg-card) !important; }

/* Remove streamlit default padding */
.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1280px !important;
}

/* ── HERO HEADER ── */
.chiya-hero {
    background: linear-gradient(135deg, #0d1f17 0%, #091510 50%, #0b1a14 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.chiya-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
}
.chiya-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(61,255,160,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.chiya-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.chiya-tagline {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 300;
    letter-spacing: 0.5px;
}
.chiya-badge {
    display: inline-block;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* ── SECTION HEADINGS ── */
.section-head {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-head span {
    display: inline-block;
    width: 4px; height: 20px;
    background: var(--accent);
    border-radius: 2px;
}

/* ── CARDS ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}
.stat-card .stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.stat-card .stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 500;
}
.stat-green  .stat-value { color: var(--accent); }
.stat-red    .stat-value { color: var(--danger); }
.stat-orange .stat-value { color: var(--warn); }

/* ── ALERT CARDS ── */
.alert-card {
    border-radius: var(--radius-sm);
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 0.92rem;
    font-weight: 500;
}
.alert-warn   { background: var(--warn-dim);   border-left: 3px solid var(--warn);   color: var(--warn); }
.alert-danger { background: var(--danger-dim); border-left: 3px solid var(--danger); color: var(--danger); }
.alert-ok     { background: var(--accent-dim); border-left: 3px solid var(--accent); color: var(--accent); }

/* ── ADD FOOD FORM ── */
.form-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
}

/* ── INPUT OVERRIDES ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: var(--bg-card2) !important;
    border: 1px solid rgba(61,255,160,0.2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}

/* ── LABELS ── */
label, .stTextInput label, .stNumberInput label, .stDateInput label {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #050f09 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.6rem 2rem !important;
    transition: box-shadow 0.2s, transform 0.15s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 20px var(--accent-glow) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── SECONDARY BUTTON ── */
[data-testid="stButton"].secondary > button {
    background: transparent !important;
    color: var(--danger) !important;
    border: 1px solid var(--danger) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    background: var(--bg-card) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg-card2) !important;
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
}

/* ── STATUS BADGES (injected via html col) ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-fresh   { background: var(--accent-dim);  color: var(--accent);  border: 1px solid var(--accent); }
.badge-risk    { background: var(--warn-dim);    color: var(--warn);    border: 1px solid var(--warn); }
.badge-expired { background: var(--danger-dim);  color: var(--danger);  border: 1px solid var(--danger); }

/* ── TOAST NOTIFICATIONS ── */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-sm) !important;
    border: none !important;
}
[data-testid="stAlert"][data-baseweb="notification"] {
    background: var(--accent-dim) !important;
    border-left: 3px solid var(--accent) !important;
}

/* ── FOOTER ── */
.chiya-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    letter-spacing: 0.3px;
}
.chiya-footer b { color: var(--accent); }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: rgba(61,255,160,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── METRIC OVERRIDES ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--accent) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 4px !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--accent) !important;
    color: #050f09 !important;
}
[data-baseweb="tab-border"] { display: none !important; }
[data-baseweb="tab-highlight"] { display: none !important; }

/* Success / warning / error messages */
.stSuccess { background: var(--accent-dim) !important; color: var(--accent) !important; border: none !important; }
.stWarning { background: var(--warn-dim) !important;   color: var(--warn)   !important; border: none !important; }
.stError   { background: var(--danger-dim) !important; color: var(--danger)  !important; border: none !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# HERO HEADER
# =========================
st.markdown("""
<div class="chiya-hero">
    <div class="chiya-badge">✦ SaaS Platform · v2.0</div>
    <div class="chiya-logo">🌱 Chiya AI</div>
    <div class="chiya-tagline">Smart Food Intelligence System · Reduce waste. Eat smarter. Save more.</div>
</div>
""", unsafe_allow_html=True)


# =========================
# LOAD DATA (cached with TTL)
# =========================
@st.cache_data(ttl=30)
def load_foods():
    try:
        response = (
            supabase
            .table("food_items")
            .select("*")
            .order("expiry_date", desc=False)
            .execute()
        )
        return response.data or []
    except Exception as e:
        st.error(f"Database Error: {e}")
        return []


# =========================
# TABS LAYOUT
# =========================
tab1, tab2, tab3 = st.tabs(["📊  Dashboard", "➕  Add Food", "📦  Inventory"])


# ──────────────────────────────────────────
# TAB 1 — DASHBOARD
# ──────────────────────────────────────────
with tab1:
    foods = load_foods()
    today = date.today()

    # Calculate stats
    total_items = len(foods)
    expired = 0
    high_risk = 0
    fresh = 0
    total_qty = 0
    alerts_list = []
    expired_list = []

    for item in foods:
        exp_date = pd.to_datetime(item["expiry_date"]).date()
        days_left = (exp_date - today).days
        total_qty += item.get("quantity", 1)

        if days_left < 0:
            expired += 1
            expired_list.append(item)
        elif days_left <= 3:
            high_risk += 1
            alerts_list.append((item, days_left))
        else:
            fresh += 1

    # ── KPI ROW ──
    st.markdown('<div class="section-head"><span></span>Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card stat-green">
            <div class="stat-value">{total_items}</div>
            <div class="stat-label">Total Items</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card stat-green">
            <div class="stat-value">{total_qty}</div>
            <div class="stat-label">Total Units</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card stat-orange">
            <div class="stat-value">{high_risk}</div>
            <div class="stat-label">Use Soon ⚡</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card stat-red">
            <div class="stat-value">{expired}</div>
            <div class="stat-label">Expired 🗑️</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI ALERTS ──
    st.markdown('<div class="section-head"><span></span>🤖 AI Alerts</div>', unsafe_allow_html=True)

    if not foods:
        st.markdown('<div class="alert-card alert-ok">🌿 Your pantry is empty — start by adding some food items!</div>', unsafe_allow_html=True)
    elif not alerts_list and not expired_list:
        st.markdown('<div class="alert-card alert-ok">✅ Everything looks fresh! No items expiring soon.</div>', unsafe_allow_html=True)
    else:
        if expired_list:
            for item in expired_list:
                st.markdown(
                    f'<div class="alert-card alert-danger">🚨 <strong>{item["food_name"]}</strong> has expired — discard immediately!</div>',
                    unsafe_allow_html=True
                )
        for item, days in alerts_list:
            if days == 0:
                msg = f'<div class="alert-card alert-danger">🔴 <strong>{item["food_name"]}</strong> expires <strong>TODAY</strong> — use now!</div>'
            elif days == 1:
                msg = f'<div class="alert-card alert-warn">🟠 <strong>{item["food_name"]}</strong> expires <strong>tomorrow</strong> — plan a meal!</div>'
            else:
                msg = f'<div class="alert-card alert-warn">⚠️ <strong>{item["food_name"]}</strong> expires in <strong>{days} days</strong> — use soon.</div>'
            st.markdown(msg, unsafe_allow_html=True)

    # ── QUICK INSIGHTS ──
    if total_items > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span>📈 Quick Insights</div>', unsafe_allow_html=True)
        waste_pct = round((expired / total_items) * 100, 1) if total_items else 0
        safe_pct  = round((fresh / total_items) * 100, 1) if total_items else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("Fresh Items", f"{fresh}", f"{safe_pct}% of stock")
        c2.metric("Waste Risk", f"{high_risk + expired}", "items need action")
        c3.metric("Expiry Rate", f"{waste_pct}%", "already expired")


# ──────────────────────────────────────────
# TAB 2 — ADD FOOD
# ──────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-head"><span></span>Add New Item</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([3, 1.5, 2])

    with col_a:
        food = st.text_input("Food Name", placeholder="e.g. Greek Yoghurt, Spinach…")
    with col_b:
        qty = st.number_input("Quantity", min_value=1, max_value=9999, value=1, step=1)
    with col_c:
        expiry_date = st.date_input("Expiry Date", value=date.today() + timedelta(days=3))

    st.markdown("</div>", unsafe_allow_html=True)

    add_col, _ = st.columns([1, 3])
    with add_col:
        if st.button("＋  Add to Pantry", use_container_width=True):
            if food.strip() == "":
                st.warning("⚠️ Please enter a food name.")
            else:
                try:
                    supabase.table("food_items").insert({
                        "food_name": food.strip().title(),
                        "quantity": int(qty),
                        "expiry_date": str(expiry_date)
                    }).execute()
                    st.success(f"✅ **{food.strip().title()}** added successfully!")
                    st.cache_data.clear()
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # ── TIPS SECTION ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(61,255,160,0.04);border:1px solid rgba(61,255,160,0.12);border-radius:12px;padding:1.2rem 1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#3dffa0;font-size:0.85rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.6rem;">
            💡 Pro Tips
        </div>
        <div style="color:#6b8c79;font-size:0.88rem;line-height:1.8;">
            • Check expiry dates on packaging before entering &nbsp;·&nbsp; Use the exact date for best accuracy<br>
            • Items expiring within 3 days will trigger automatic AI alerts<br>
            • Quantities represent individual units (packets, bottles, pieces)
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────
# TAB 3 — INVENTORY
# ──────────────────────────────────────────
with tab3:
    foods = load_foods()
    today = date.today()

    st.markdown('<div class="section-head"><span></span>All Inventory</div>', unsafe_allow_html=True)

    if not foods:
        st.markdown('<div class="alert-card alert-ok">📦 No food items yet — head to Add Food to get started!</div>', unsafe_allow_html=True)
    else:
        # Build dataframe
        rows = []
        for item in foods:
            exp_date = pd.to_datetime(item["expiry_date"]).date()
            days_left = (exp_date - today).days

            if days_left < 0:
                status = "🔴 Expired"
            elif days_left <= 3:
                status = "🟠 Use Soon"
            else:
                status = "🟢 Fresh"

            days_str = "Expired" if days_left < 0 else f"{days_left}d"

            rows.append({
                "Food Item":    item["food_name"],
                "Qty":          item["quantity"],
                "Expiry Date":  str(item["expiry_date"]),
                "Days Left":    days_str,
                "Status":       status
            })

        df = pd.DataFrame(rows)

        # ── FILTER ROW ──
        filter_col1, filter_col2, _ = st.columns([1.5, 1.5, 3])
        with filter_col1:
            filter_status = st.selectbox(
                "Filter by Status",
                ["All", "🟢 Fresh", "🟠 Use Soon", "🔴 Expired"],
                label_visibility="collapsed"
            )
        with filter_col2:
            search_term = st.text_input("Search", placeholder="🔍 Search food…", label_visibility="collapsed")

        if filter_status != "All":
            df = df[df["Status"] == filter_status]
        if search_term:
            df = df[df["Food Item"].str.contains(search_term, case=False)]

        st.markdown(f"<div style='color:#6b8c79;font-size:0.8rem;margin-bottom:0.5rem;'>{len(df)} item(s) shown</div>", unsafe_allow_html=True)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Food Item": st.column_config.TextColumn("Food Item", width="medium"),
                "Qty":       st.column_config.NumberColumn("Qty", format="%d"),
                "Expiry Date": st.column_config.TextColumn("Expiry Date", width="small"),
                "Days Left": st.column_config.TextColumn("Days Left", width="small"),
                "Status":    st.column_config.TextColumn("Status", width="small"),
            }
        )

        # ── CSV EXPORT ──
        csv_data = df.to_csv(index=False).encode("utf-8")
        dl_col, _ = st.columns([1, 4])
        with dl_col:
            st.download_button(
                label="⬇️  Export CSV",
                data=csv_data,
                file_name=f"chiya_inventory_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="chiya-footer">
    Built with ❤️ by <b>Rakesh</b> &nbsp;·&nbsp; Chiya AI Smart Food Intelligence &nbsp;·&nbsp; Powered by Supabase + Streamlit
</div>
""", unsafe_allow_html=True)
