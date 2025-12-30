import streamlit as st
import requests
import time
from datetime import datetime, timezone

# ======================================================
# ADVANCED PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="STORM PRO | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================================================
# CORE CONFIGURATION & WEBHOOKS
# ======================================================
N8N_WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook-test/f4afadf7-168a-wolf"
LOGO_PATH = "assets/logo(1).jpeg"
PRIMARY_GREEN = "#CDFF00"  # Logo Neon Green
SECONDARY_GREEN = "#39FF14" # High-vis Neon
DEEP_BG = "#020802"        # Absolute Dark Green (No Grey)
MID_BG = "#051205"         # Subtle Green-Black
ACCENT_GLOW = "rgba(205, 255, 0, 0.15)"

# ======================================================
# PROFESSIONAL "NO GREY" CSS ARCHITECTURE
# ======================================================
st.markdown(
    f"""
    <meta name="theme-color" content="{DEEP_BG}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap');

    /* BASE RESET & NO GREY POLICY */
    * {{
        -webkit-tap-highlight-color: transparent;
        font-family: 'Inter', sans-serif;
    }}

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .stApp, .main {{
        background-color: {DEEP_BG} !important;
        background-image: 
            radial-gradient(circle at 50% -20%, {MID_BG} 0%, transparent 70%),
            radial-gradient(circle at 0% 100%, {MID_BG} 0%, transparent 40%) !important;
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    /* HIDE STREAMLIT OVERHEAD */
    #MainMenu, header, footer, .stDeployButton, .stAppDeployButton, 
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
        visibility: hidden !important;
        display: none !important;
    }}

    .block-container {{
        padding: env(safe-area-inset-top) 1.5rem 6rem 1.5rem !important;
        max-width: 800px !important;
        background: transparent !important;
    }}

    /* PROFESSIONAL HEADER SYSTEM */
    .pro-header {{
        position: relative;
        padding: 3rem 1.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(145deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 1px solid {PRIMARY_GREEN}33;
        border-radius: 32px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        overflow: hidden;
    }}

    .pro-header::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, {PRIMARY_GREEN}, transparent);
    }}

    .logo-frame {{
        display: inline-block;
        padding: 8px;
        background: {DEEP_BG};
        border: 2px solid {PRIMARY_GREEN};
        border-radius: 24px;
        box-shadow: 0 0 30px {PRIMARY_GREEN}44;
        margin-bottom: 1.5rem;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .logo-frame:hover {{
        transform: scale(1.05) rotate(2deg);
    }}

    .logo-frame img {{
        width: 160px;
        height: 160px;
        border-radius: 18px;
        object-fit: cover;
        display: block;
    }}

    .title-main {{
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        color: {PRIMARY_GREEN};
        margin: 0;
        line-height: 1;
        text-transform: uppercase;
        filter: drop-shadow(0 0 15px {PRIMARY_GREEN}66);
    }}

    .subtitle-pro {{
        font-size: 0.95rem;
        color: {SECONDARY_GREEN};
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 1rem;
        opacity: 0.9;
    }}

    /* CHAT INTERFACE - SOPHISTICATED BUBBLES */
    [data-testid="stChatMessageContainer"] {{
        gap: 1.5rem !important;
    }}

    .stChatMessage {{
        background: transparent !important;
    }}

    /* User Message Style */
    .stChatMessage.user > div {{
        background: {MID_BG} !important;
        border: 1px solid {SECONDARY_GREEN}44 !important;
        border-radius: 24px 24px 4px 24px !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }}

    /* Assistant Message Style */
    .stChatMessage.assistant > div {{
        background: linear-gradient(160deg, {MID_BG} 0%, {DEEP_BG} 100%) !important;
        border: 1px solid {PRIMARY_GREEN}66 !important;
        border-radius: 24px 24px 24px 4px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        position: relative;
    }}

    .stChatMessage.assistant::after {{
        content: 'WOLF AI';
        position: absolute;
        top: -10px; left: 20px;
        background: {PRIMARY_GREEN};
        color: {DEEP_BG};
        font-size: 0.65rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.1em;
    }}

    /* INPUT SYSTEM - FIXED & POLISHED */
    [data-testid="stChatInput"] {{
        background: {DEEP_BG} !important;
        border-top: 1px solid {PRIMARY_GREEN}22 !important;
        padding: 1.5rem !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
        backdrop-filter: blur(10px);
    }}

    .stChatInput textarea {{
        background: {MID_BG} !important;
        color: #ffffff !important;
        border: 2px solid {PRIMARY_GREEN} !important;
        border-radius: 16px !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }}

    .stChatInput textarea:focus {{
        box-shadow: 0 0 20px {PRIMARY_GREEN}33 !important;
        border-color: {SECONDARY_GREEN} !important;
    }}

    /* BUTTONS - PREMIUM FEEL */
    .stButton button {{
        background: linear-gradient(135deg, {PRIMARY_GREEN} 0%, {SECONDARY_GREEN} 100%) !important;
        color: {DEEP_BG} !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        box-shadow: 0 10px 25px {PRIMARY_GREEN}44 !important;
    }}

    .stButton button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px {PRIMARY_GREEN}66 !important;
        filter: brightness(1.1);
    }}

    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {DEEP_BG}; }}
    ::-webkit-scrollbar-thumb {{ 
        background: {PRIMARY_GREEN}44; 
        border-radius: 10px; 
    }}
    ::-webkit-scrollbar-thumb:hover {{ background: {PRIMARY_GREEN}; }}

    /* ANIMATIONS */
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .stChatMessage {{
        animation: slideUp 0.5s ease-out forwards;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# PROFESSIONAL UI COMPONENTS
# ======================================================

def render_header():
    st.markdown(
        f"""
        <div class="pro-header">
            <div class="logo-frame">
                <img src="https://raw.githubusercontent.com/manus-ai/assets/main/wolf_logo.png" alt="Storm Logo">
            </div>
            <h1 class="title-main">STORM PRO</h1>
            <p class="subtitle-pro">The Apex Predator of Real Estate Intelligence</p>
            <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <span style="background: {PRIMARY_GREEN}22; color: {PRIMARY_GREEN}; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; border: 1px solid {PRIMARY_GREEN}44;">TAX DEEDS</span>
                <span style="background: {PRIMARY_GREEN}22; color: {PRIMARY_GREEN}; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; border: 1px solid {PRIMARY_GREEN}44;">WHOLESALE</span>
                <span style="background: {PRIMARY_GREEN}22; color: {PRIMARY_GREEN}; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; border: 1px solid {PRIMARY_GREEN}44;">CREATIVE FINANCE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_footer():
    st.markdown(
        f"""
        <div style="margin-top: 4rem; padding: 3rem 1rem; text-align: center; border-top: 1px solid {PRIMARY_GREEN}22;">
            <div style="color: {PRIMARY_GREEN}; font-weight: 800; letter-spacing: 0.2em; margin-bottom: 0.5rem;">WOLVES OF REAL ESTATE</div>
            <div style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">© 2025 DOMINATION ENGINE • VERSION 2.0 PRO</div>
            <div style="margin-top: 1.5rem; color: {SECONDARY_GREEN}; font-size: 0.7rem; opacity: 0.6;">NO GREY ZONE • FULL GREEN PROTOCOL ACTIVE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# MAIN APPLICATION LOGIC
# ======================================================

render_header()

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🐺 **System Online.** I am Storm, your strategic partner in real estate domination. \n\n"
                       "I am currently optimized for analyzing **high-yield tax deeds, structuring wholesale spreads, and architecting creative finance solutions.**\n\n"
                       "How shall we attack the market today?"
        }
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Interaction
user_input = st.chat_input("Input deal parameters or strategy query...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Professional Loading State
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⚡ *Analyzing market data...*")
        
        # Webhook Integration
        payload = {
            "assistant": "Storm Pro",
            "message": user_input,
            "history": st.session_state.messages[-5:],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
            if response.status_code == 200:
                full_response = response.text.strip()
            else:
                full_response = "⚠️ *System encountered a processing delay. Please re-submit the data.*"
        except:
            full_response = "⚠️ *Connection to the intelligence core was interrupted.*"
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Reset & Footer
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 REINITIALIZE SESSION", use_container_width=True):
    st.session_state.messages = [{"role": "assistant", "content": "🐺 **Session Reinitialized.** Ready for new data."}]
    st.rerun()

render_footer()
