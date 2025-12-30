import streamlit as st
import requests
from datetime import datetime, timezone

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Storm | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================================================
# FULL MOBILE & BROWSER THEME - VIBRANT GREEN EVERYWHERE
# ======================================================
# Color Palette:
# Primary Green: #CDFF00 (Vibrant Lime Green)
# Dark Green BG: #051005 (Deep Forest Black-Green)
# Mid Green BG: #0a1a0a (Dark Moss)
# Accent Green: #39FF14 (Neon Green)
# No Grey Policy: All greys replaced with green-tinted darks or pure black/white.

st.markdown(
    """
    <meta name="theme-color" content="#051005">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Storm">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <style>
    /* HIDE ALL STREAMLIT BRANDING */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    
    /* GLOBAL STYLES - NO GREY */
    * {
        -webkit-tap-highlight-color: rgba(205, 255, 0, 0.2);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .stApp, .main {
        background-color: #051005 !important;
        background-image: 
            radial-gradient(circle at 50% 0%, #0a2a0a 0%, transparent 50%),
            radial-gradient(circle at 0% 100%, #051505 0%, transparent 40%) !important;
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    .block-container {
        padding: env(safe-area-inset-top) 1rem 5rem 1rem !important;
        max-width: 100% !important;
        background: transparent !important;
    }

    /* ENHANCED MOBILE HEADER */
    .storm-header {
        text-align: center;
        margin: 0 auto 2rem auto;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(145deg, #0a1a0a 0%, #051005 100%);
        border-radius: 24px;
        border: 2px solid #CDFF00;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.6),
            0 0 20px rgba(205, 255, 0, 0.2),
            inset 0 0 15px rgba(205, 255, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .storm-header::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(205, 255, 0, 0.03) 1px, rgba(205, 255, 0, 0.03) 2px);
        pointer-events: none;
    }

    /* LOGO CONTAINER */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
        z-index: 2;
    }
    
    .logo-container img {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 3px solid #CDFF00;
        box-shadow: 0 0 30px rgba(205, 255, 0, 0.4);
        object-fit: cover;
    }
    
    /* TITLES */
    .storm-title {
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        margin: 0;
        color: #CDFF00;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(205, 255, 0, 0.5);
    }
    
    .storm-subtitle {
        font-size: 0.9rem;
        color: #39FF14;
        font-weight: 500;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        margin-top: 0.5rem;
        opacity: 0.8;
    }

    /* CHAT MESSAGES - GREEN THEME */
    [data-testid="stChatMessageContainer"] {
        background: transparent !important;
    }
    
    .stChatMessage {
        background: transparent !important;
        padding: 0.5rem 0 !important;
    }
    
    /* User Message */
    .stChatMessage.user > div {
        background: #0a2a0a !important;
        border: 1px solid #39FF14 !important;
        border-radius: 20px 20px 4px 20px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Assistant Message */
    .stChatMessage.assistant > div {
        background: linear-gradient(135deg, #051505 0%, #0a1a0a 100%) !important;
        border: 1px solid #CDFF00 !important;
        border-radius: 20px 20px 20px 4px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(205, 255, 0, 0.1) !important;
    }

    /* INPUT AREA - FIXED TO BOTTOM FOR IPHONE */
    [data-testid="stChatInput"] {
        background-color: #051005 !important;
        border-top: 1px solid #0a2a0a !important;
        padding: 1rem !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
    }
    
    .stChatInput textarea {
        background: #0a1a0a !important;
        color: #ffffff !important;
        border: 2px solid #CDFF00 !important;
        border-radius: 12px !important;
    }

    /* BUTTONS */
    .stButton button {
        background: #CDFF00 !important;
        color: #051005 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background: #39FF14 !important;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.4);
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #051005;
    }
    ::-webkit-scrollbar-thumb {
        background: #0a2a0a;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #CDFF00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# UI COMPONENTS
# ======================================================

# Header Section
st.markdown(
    """
    <div class="storm-header">
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/manus-ai/assets/main/wolf_logo.png" alt="Wolf Logo">
        </div>
        <div class="storm-title">STORM</div>
        <div class="storm-subtitle">Wolves of Real Estate</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Chat Interface Logic
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🐺 **Storm is online.** Ready to dominate the market. What's the play?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Analyze a deal...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Placeholder for response
    with st.chat_message("assistant"):
        response = "Analyzing the data with a predatory lens... (Webhook integration active)"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown(
    """
    <div style="text-align: center; padding: 2rem; color: #39FF14; font-size: 0.7rem; letter-spacing: 0.2em; opacity: 0.6;">
        © 2025 WOLVES OF REAL ESTATE | NO GREY ZONE
    </div>
    """,
    unsafe_allow_html=True
)
