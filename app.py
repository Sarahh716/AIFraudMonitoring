import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random

# --- 1. CORE SYSTEM LOGIC ---
def mock_apply_scoring(df, watchlist, location, threshold):
    df['Merchant_Risk'] = df['Merchant'].apply(lambda x: 80 if x in watchlist else random.randint(5, 45))
    df['Geo_Risk'] = [random.randint(10, 90) for _ in range(len(df))]
    df['Risk_Score'] = (df['Merchant_Risk'] + df['Geo_Risk']) / 2
    df['Flagged'] = df['Risk_Score'].apply(lambda x: "🚨 CRITICAL" if x > 70 else ("⚠️ WARNING" if x > 40 else "✅ CLEAN"))
    return df

# --- 2. GLOBAL CONFIGURATION ---
st.set_page_config(
    page_title="RedLine AI | Terminal",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_MAP = {
    "🚨 CRITICAL": "#FF0000",
    "⚠️ WARNING": "#FFA500",
    "✅ CLEAN": "#00FF41"
}

# --- 3. THE REDLINE TERMINAL CSS (STABILIZING GLITCH + FADE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

    /* Global UI Overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Space Mono', monospace !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    [data-testid="collapsedControl"] { display: none !important; }

    /* Floating Command Deck (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 2px solid #FF0000 !important;
        margin: 15px;
        height: calc(100vh - 30px) !important;
        border-radius: 10px;
    }

    /* --- ANIMATION ENGINE --- */
    @keyframes headingFade {
        0% { opacity: 0; filter: blur(10px); transform: translateY(-5px); }
        100% { opacity: 1; filter: blur(0); transform: translateY(0); }
    }

    @keyframes glitch-jitter-finite {
        0% { transform: translate(0); opacity: 0.8; }
        25% { transform: translate(-8px, 4px); }
        50% { transform: translate(8px, -4px); }
        75% { transform: translate(-4px, 2px); }
        100% { transform: translate(0); opacity: 0; }
    }

    .glitch-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px 0 20px 0;
        animation: headingFade 1.5s ease-out forwards;
    }

    .main-title {
        position: relative;
        font-family: 'Space Mono', monospace !important;
        font-size: clamp(40px, 8vw, 95px) !important;
        font-weight: 700;
        color: #FF0000 !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        margin: 0;
        z-index: 1;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
    }

    /* Finite Glitch Pseudo-elements */
    .main-title::before {
        content: "RedLine AI";
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        color: #FF0000; text-shadow: -4px 0 #00FFFF;
        animation: glitch-jitter-finite 0.1s linear 15; /* Ends after 1.5s */
        animation-fill-mode: forwards;
        z-index: -1;
    }

    .main-title::after {
        content: "RedLine AI";
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        color: #FF0000; text-shadow: 4px 0 #FF00FF;
        animation: glitch-jitter-finite 0.12s linear 12; /* Ends after 1.5s */
        animation-fill-mode: forwards;
        z-index: -2;
    }

    .sub-title {
        text-align: center;
        color: #666;
        letter-spacing: 5px;
        font-size: 14px;
        margin-top: 10px;
        text-transform: uppercase;
        animation: headingFade 2.5s ease-out forwards;
    }

    /* Metrics & Cards */
    [data-testid="stMetricValue"] { color: #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BRANDING ---
st.markdown("""
    <div class="glitch-container">
        <h1 class="main-title">RedLine AI</h1>
        <p class="sub-title">> YOUR MUCH NEEDED FRAUD MONITORING SYSTEM_</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. FLOATING SIDEBAR (COMMAND DECK) ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF0000; text-align:center; font-size:20px;'>COMMAND DECK</h2>", unsafe_allow_html=True)
    st.divider()
    
    is_live = st.toggle("🛰️ LOG - JSON", value=False)
    node_select = st.selectbox("Office Location", ["London HQ", "New York HQ", "Singapore HQ"])
    km_limit = st.slider("RADAR_SENSITIVITY (KM)", 0, 20000, 5000)
    
    st.divider()
    watchlist = st.multiselect("MERCHANT WATCHLIST", 
                               ["Global Casino", "Dark-Web Vendor", "Crypto-Tumbler"],
                               default=["Global Casino"])

    if not is_live:
        uploaded_file = st.file_uploader("LOG_INGESTION (XLSX)", type=['xlsx'])
    else:
        pulse_rate = st.slider("PULSE_RATE (SEC)", 0.5, 3.0, 1.0)

# --- 6. MAIN WORKSPACE ---
if not is_live:
    if uploaded_file:
        with st.status("Analyzing Data Stream...", expanded=True) as status:
            time.sleep(1)
            df_raw = pd.DataFrame({
                'ID': [f"TXN-{i}" for i in range(100)],
                'Merchant': [random.choice(["Amazon", "Global Casino", "Apple"]) for _ in range(100)],
                'Amount': [random.randint(10, 5000) for _ in range(100)]
            })
            df = mock_apply_scoring(df_raw, watchlist, node_select, km_limit)
            status.update(label="Analysis Complete", state="complete")

        m1, m2, m3 = st.columns(3)
        m1.metric("SCAN_TOTAL", len(df))
        m2.metric("ACTIVE_NODE", node_select)
        m3.metric("REDLINE_BREACHES", len(df[df['Flagged'] == "🚨 CRITICAL"]))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### RISK_STRATIFICATION")
            fig = px.strip(df, y="Risk_Score", x="Flagged", color="Flagged", color_discrete_map=COLOR_MAP, template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Space Mono")
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.markdown("### ENGINE_REASONING")
            reason_df = pd.DataFrame({"Factor": ["Merchant", "Geo", "Velocity"], "Weight": [40, 30, 30]})
            fig2 = px.bar(reason_df, x="Weight", y="Factor", orientation='h', color_continuous_scale=["#220000", "#FF0000"], template="plotly_dark")
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Space Mono")
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df.sort_values("Risk_Score", ascending=False), use_container_width=True)
    else:
        st.info(">> SYSTEM_IDLE: AWAITING_DATA_INGESTION_")

else:
    # --- 7. LIVE INTERCEPT MODE ---
    st.error(f"🔴 JSON INTERCEPT ACTIVE - Office: {node_select}")
    if 'live_data' not in st.session_state: st.session_state.live_data = []
    placeholder = st.empty()
    
    while is_live:
        new_txn = {"ID": f"TXN-{random.randint(1000, 9999)}", "Merchant": random.choice(["Global Casino", "Apple"]), "Risk_Score": random.randint(10, 100)}
        new_txn['Flagged'] = "🚨 CRITICAL" if new_txn['Risk_Score'] > 75 else "✅ CLEAN"
        st.session_state.live_data.insert(0, new_txn)
        st.session_state.live_data = st.session_state.live_data[:10]
        
        with placeholder.container():
            lc1, lc2 = st.columns([1, 2])
            with lc1:
                live_df = pd.DataFrame(st.session_state.live_data)
                fig_pie = px.pie(live_df, names="Flagged", hole=0.6, color="Flagged", color_discrete_map=COLOR_MAP, template="plotly_dark")
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig_pie, use_container_width=True)
            with lc2:
                st.table(st.session_state.live_data)
        
        time.sleep(pulse_rate)
        st.rerun()