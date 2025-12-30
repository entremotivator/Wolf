import streamlit as st
import requests
import base64
import os
from datetime import datetime, timezone

# ======================================================
# 1. MAXIMUM STEALTH PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="STORM | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ======================================================
# 2. CORE CONFIGURATION & BRANDING - FIXED WEBHOOK
# ======================================================
N8N_WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook-test/f4afadf7-168a-wolf"
PRIMARY_GREEN = "#CDFF00"
SECONDARY_GREEN = "#39FF14"
DEEP_BG = "#020802"
MID_BG = "#051205"
ACCENT_GLOW = "rgba(205, 255, 0, 0.2)"

# ======================================================
# 3. ROBUST LOGO LOADING (BASE64)
# ======================================================
def get_base64_image(image_filename):
    """Searches for the logo and returns it as a base64 string for HTML embedding."""
    possible_paths = [
        os.path.join("assets", image_filename),
        os.path.join("/home/ubuntu/upload", image_filename),
        image_filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                return f"data:image/jpeg;base64,{encoded}"
    
    return "https://raw.githubusercontent.com/manus-ai/assets/main/wolf_logo.png"

LOGO_DATA = get_base64_image("logo(1).jpeg")

# ======================================================
# 4. ABSOLUTE STREAMLIT HIDING CSS ENGINE
# ======================================================
st.markdown(
    f"""
    <meta name="theme-color" content="{DEEP_BG}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap');

    /* GLOBAL RESET */
    * {{
        -webkit-tap-highlight-color: transparent;
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    /* COMPLETE BACKGROUND CONTROL */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], 
    .stApp, .main, [class*="appview"], section[tabindex="0"] {{
        background-color: {DEEP_BG} !important;
        background-image: 
            radial-gradient(circle at 50% -20%, {MID_BG} 0%, transparent 70%),
            radial-gradient(circle at 0% 100%, {MID_BG} 0%, transparent 40%) !important;
        color: #ffffff !important;
        overflow-x: hidden;
    }}

    /* NUCLEAR OPTION - HIDE ALL STREAMLIT UI ELEMENTS */
    #MainMenu, header, footer, 
    .stDeployButton, .stAppDeployButton, .reportview-container,
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"],
    [data-testid="stToolbarActions"],
    [data-testid="stActionButtonIcon"],
    [data-testid="collapsedControl"],
    .css-18e3th9, .css-1d391kg,
    div[data-testid="stSidebarNav"],
    button[kind="header"],
    [class*="viewerBadge"],
    [data-testid="stAppViewBlockContainer"] > div:first-child,
    section[data-testid="stSidebar"] > div:first-child,
    .styles_viewerBadge__1yB5_,
    [data-testid="stException"],
    [data-testid="stNotification"],
    div.element-container:has(> div.stAlert),
    div[data-testid="stFileUploadDropzone"],
    button[title="View fullscreen"],
    [data-testid="baseButton-header"],
    [data-testid="baseButton-headerNoPadding"],
    .stChatFloatingInputContainer {{
        visibility: hidden !important;
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    /* AGGRESSIVE PADDING OVERRIDE */
    .block-container, [data-testid="block-container"] {{
        padding: 2rem 1.5rem 8rem 1.5rem !important;
        max-width: 800px !important;
        background: transparent !important;
        margin: 0 auto !important;
    }}

    /* MOBILE SAFE AREA SUPPORT */
    @supports (padding: max(0px)) {{
        .block-container {{
            padding: max(2rem, env(safe-area-inset-top)) 
                     max(1.5rem, env(safe-area-inset-right)) 
                     max(8rem, env(safe-area-inset-bottom)) 
                     max(1.5rem, env(safe-area-inset-left)) !important;
        }}
    }}

    /* PREMIUM HEADER SYSTEM */
    .storm-header-container {{
        position: relative;
        padding: 3.5rem 1.5rem;
        margin-bottom: 2.5rem;
        background: linear-gradient(145deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 2px solid {PRIMARY_GREEN}33;
        border-radius: 40px;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
        overflow: hidden;
    }}

    .storm-header-container::after {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 50% 50%, {PRIMARY_GREEN}05, transparent 70%);
        pointer-events: none;
    }}

    .logo-outer-frame {{
        display: inline-block;
        padding: 10px;
        background: {DEEP_BG};
        border: 3px solid {PRIMARY_GREEN};
        border-radius: 30px;
        box-shadow: 0 0 40px {PRIMARY_GREEN}33;
        margin-bottom: 1.5rem;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .logo-outer-frame:hover {{
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 0 60px {PRIMARY_GREEN}55;
    }}

    .logo-outer-frame img {{
        width: 180px;
        height: 180px;
        border-radius: 20px;
        object-fit: cover;
        display: block;
    }}

    .main-title {{
        font-size: clamp(3rem, 10vw, 5rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        color: {PRIMARY_GREEN};
        margin: 0;
        line-height: 0.9;
        text-transform: uppercase;
        filter: drop-shadow(0 0 20px {PRIMARY_GREEN}44);
    }}

    .sub-title {{
        font-size: 1rem;
        color: {SECONDARY_GREEN};
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 1.25rem;
        opacity: 0.85;
    }}

    /* CHAT INTERFACE - PREMIUM BUBBLES */
    [data-testid="stChatMessageContainer"] {{
        gap: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    .stChatMessage {{
        background: transparent !important;
        border: none !important;
    }}

    /* User Message Bubble */
    [data-testid="stChatMessage"][data-testid*="user"] > div,
    .stChatMessage[class*="user"] > div {{
        background: {MID_BG} !important;
        border: 1px solid {SECONDARY_GREEN}33 !important;
        border-radius: 28px 28px 4px 28px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        color: #ffffff !important;
    }}

    /* Assistant Message Bubble */
    [data-testid="stChatMessage"][data-testid*="assistant"] > div,
    .stChatMessage[class*="assistant"] > div {{
        background: linear-gradient(165deg, {MID_BG} 0%, {DEEP_BG} 100%) !important;
        border: 1px solid {PRIMARY_GREEN}55 !important;
        border-radius: 28px 28px 28px 4px !important;
        padding: 1.75rem !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4) !important;
        position: relative;
    }}

    /* Assistant Label Badge */
    [data-testid="stChatMessage"][data-testid*="assistant"]::before,
    .stChatMessage[class*="assistant"]::before {{
        content: 'STORM ASSISTANT';
        position: absolute;
        top: -12px;
        left: 30px;
        background: {PRIMARY_GREEN};
        color: {DEEP_BG};
        font-size: 0.7rem;
        font-weight: 900;
        padding: 3px 12px;
        border-radius: 6px;
        letter-spacing: 0.15em;
        z-index: 10;
    }}

    /* INPUT SYSTEM - FIXED TO BOTTOM */
    [data-testid="stChatInput"],
    [data-testid="stChatInputContainer"],
    .stChatFloatingInputContainer {{
        display: block !important;
        visibility: visible !important;
        background: {DEEP_BG} !important;
        border-top: 2px solid {PRIMARY_GREEN}11 !important;
        padding: 1.5rem !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
        backdrop-filter: blur(15px);
    }}

    [data-testid="stChatInput"] textarea,
    .stChatInput textarea {{
        background: {MID_BG} !important;
        color: #ffffff !important;
        border: 2px solid {PRIMARY_GREEN} !important;
        border-radius: 20px !important;
        font-size: 1.1rem !important;
        padding: 15px 20px !important;
        transition: all 0.3s ease !important;
    }}

    [data-testid="stChatInput"] textarea:focus,
    .stChatInput textarea:focus {{
        box-shadow: 0 0 30px {PRIMARY_GREEN}22 !important;
        border-color: {SECONDARY_GREEN} !important;
        outline: none !important;
    }}

    /* BUTTONS - APEX STYLE */
    .stButton button,
    button[kind="primary"],
    button[kind="secondary"] {{
        background: linear-gradient(135deg, {PRIMARY_GREEN} 0%, {SECONDARY_GREEN} 100%) !important;
        color: {DEEP_BG} !important;
        font-weight: 800 !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        box-shadow: 0 12px 30px {PRIMARY_GREEN}33 !important;
        width: 100% !important;
    }}

    .stButton button:hover,
    button[kind="primary"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 45px {PRIMARY_GREEN}55 !important;
        filter: brightness(1.1);
    }}

    /* SCROLLBAR CUSTOMIZATION */
    ::-webkit-scrollbar {{ 
        width: 10px; 
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{ 
        background: {DEEP_BG}; 
    }}
    
    ::-webkit-scrollbar-thumb {{ 
        background: linear-gradient({PRIMARY_GREEN}44, {SECONDARY_GREEN}44); 
        border-radius: 10px; 
    }}
    
    ::-webkit-scrollbar-thumb:hover {{ 
        background: {PRIMARY_GREEN}; 
    }}

    /* ANIMATIONS */
    @keyframes entryFade {{
        from {{ 
            opacity: 0; 
            transform: translateY(30px); 
        }}
        to {{ 
            opacity: 1; 
            transform: translateY(0); 
        }}
    }}

    .stChatMessage {{
        animation: entryFade 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }}

    /* HIDE EXCEPTION MESSAGES */
    .element-container:has(.stException),
    [data-testid="stException"] {{
        display: none !important;
    }}

    /* TEXT AND MARKDOWN STYLING */
    p, span, div {{
        color: #ffffff !important;
    }}

    code {{
        background: {MID_BG} !important;
        color: {PRIMARY_GREEN} !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* RESPONSIVE ADJUSTMENTS */
    @media (max-width: 768px) {{
        .storm-header-container {{
            padding: 2rem 1rem;
            border-radius: 30px;
        }}
        
        .logo-outer-frame img {{
            width: 140px;
            height: 140px;
        }}
        
        .main-title {{
            font-size: 2.5rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# 5. UI COMPONENT RENDERING
# ======================================================

def render_storm_header():
    st.markdown(
        f"""
        <div class="storm-header-container">
            <div class="logo-outer-frame">
                <img src="{LOGO_DATA}" alt="Storm Logo">
            </div>
            <h1 class="main-title">STORM</h1>
            <p class="sub-title">Wolves of Real Estate • AI Assistant</p>
            <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap;">
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">TAX DEEDS</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">TAX LIENS</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">WHOLESALE</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">CREATIVE FINANCE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_storm_footer():
    st.markdown(
        f"""
        <div style="margin-top: 5rem; padding: 4rem 1rem; text-align: center; border-top: 2px solid {PRIMARY_GREEN}11;">
            <div style="color: {PRIMARY_GREEN}; font-weight: 900; letter-spacing: 0.3em; margin-bottom: 0.75rem; font-size: 1.2rem;">WOLVES OF REAL ESTATE</div>
            <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; letter-spacing: 0.1em;">© 2025 Built for Serious Operators</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# 6. MAIN APPLICATION ENGINE
# ======================================================

render_storm_header()

# Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🐺 **Welcome to Storm** — the Wolves of Real Estate AI.\n\n"
                       "I specialize in **tax deeds, tax liens, wholesale deals, and creative finance strategies**.\n\n"
                       "Whether you're analyzing auction properties, calculating ROI, or structuring creative financing — "
                       "I'm here to help you dominate the market.\n\n"
                       "**What deal are we attacking today?**"
        }
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Interaction & Webhook Logic
user_input = st.chat_input("Ask about auctions, liens, wholesale spreads, or creative finance strategies…")

if user_input:
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Professional Assistant Response
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.markdown("🐺 *Storm is analyzing...*")
        
        # Prepare Payload for N8N - CORRECT FORMAT
        payload = {
            "assistant": "Storm",
            "community": "Wolves of Real Estate",
            "message": user_input,
            "history": st.session_state.messages[-10:],
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
        }
        
        try:
            # Execute Webhook Call with proper timeout
            response = requests.post(
                N8N_WEBHOOK_URL, 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200 and response.text:
                final_reply = response.text.strip()
            else:
                final_reply = "⚠️ Storm encountered an issue. Let's try that again."
                
        except requests.exceptions.Timeout:
            final_reply = "⚠️ **Request timed out.** Storm is taking longer than expected. Please try again."
        except requests.exceptions.RequestException as e:
            final_reply = "⚠️ **Connection error:** Unable to reach Storm's server. Please check your connection."
        
        # Update UI with response
        status_placeholder.markdown(final_reply)
        st.session_state.messages.append({"role": "assistant", "content": final_reply})

# Reset & Footer Section
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 RESET CONVERSATION", width="stretch"):
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🐺 **Conversation Reset**\n\nReady to analyze your next deal. What are we working on?"
        }
    ]
    st.rerun()

render_storm_footer()
