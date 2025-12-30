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

st.markdown(
    """
    <meta name="theme-color" content="#0a0a0a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Storm">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="format-detection" content="telephone=no">
    <meta name="msapplication-TileColor" content="#0a0a0a">
    <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0a0a0a">
    <meta name="theme-color" media="(prefers-color-scheme: light)" content="#0a0a0a">
    """,
    unsafe_allow_html=True
)

# ======================================================
# N8N WEBHOOK (LIVE TEST URL)
# ======================================================
N8N_WEBHOOK_URL = (
    "https://agentonline-u29564.vm.elestio.app"
    "/webhook-test/f4afadf7-168a-wolf"
)

# ======================================================
# FULL BROWSER GREEN THEME - DESKTOP & MOBILE
# ======================================================
st.markdown(
    """
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
    .css-18e3th9 {padding-top: 0rem;}
    .css-1d391kg {padding-top: 0rem;}
    
    /* FULL BROWSER GREEN THEME - EVERYWHERE */
    * {
        -webkit-tap-highlight-color: rgba(205, 255, 0, 0.2);
        box-sizing: border-box;
    }
    
    html {
        background: #0a0a0a !important;
        overflow-x: hidden;
        height: 100%;
        min-height: 100vh;
    }
    
    body {
        background: #0a0a0a !important;
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
        height: 100%;
        min-height: 100vh;
    }
    
    /* FORCE GREEN BACKGROUND ON ALL STREAMLIT CONTAINERS */
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stHeader"],
    [data-testid="stBottom"],
    .stApp,
    .main,
    section {
        background: #0a0a0a !important;
        min-height: 100vh;
    }
    
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: #0a0a0a;
        z-index: -1;
    }
    
    .block-container {
        padding: env(safe-area-inset-top, 1rem) 1rem 2rem 1rem !important;
        max-width: 900px !important;
        background: #0a0a0a !important;
    }
    
    /* BROWSER CHROME GREEN THEME */
    :root {
        color-scheme: dark;
        background-color: #0a0a0a;
    }
    
    /* ENHANCED MOBILE & DESKTOP HEADER */
    .storm-header {
        text-align: center;
        margin: 0 auto 2rem auto;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        border-radius: 24px;
        border: 3px solid #CDFF00;
        box-shadow: 
            0 0 50px rgba(205, 255, 0, 0.5),
            inset 0 0 30px rgba(205, 255, 0, 0.1);
        position: relative;
        overflow: hidden;
        max-width: 800px;
    }
    
    .storm-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(205, 255, 0, 0.15) 0%, transparent 70%);
        animation: pulse 5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.15) rotate(180deg); opacity: 0.8; }
    }
    
    /* LOGO CONTAINER - PERFECTLY CENTERED */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.75rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-wrapper {
        display: inline-block;
        position: relative;
    }
    
    .logo-wrapper::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: radial-gradient(circle, rgba(205, 255, 0, 0.3) 0%, transparent 70%);
        border-radius: 24px;
        animation: logoGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes logoGlow {
        0% { opacity: 0.5; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1.05); }
    }
    
    .logo-container img {
        width: 200px;
        height: 200px;
        border-radius: 20px;
        border: 4px solid #CDFF00;
        box-shadow: 
            0 0 50px rgba(205, 255, 0, 0.7),
            0 10px 40px rgba(0, 0, 0, 0.5),
            inset 0 0 20px rgba(205, 255, 0, 0.1);
        object-fit: cover;
        display: block;
        position: relative;
        z-index: 1;
        transition: transform 0.3s ease;
    }
    
    .logo-container img:hover {
        transform: scale(1.05);
    }
    
    /* STORM TITLE - ENHANCED FOR ALL SCREENS */
    .storm-title {
        font-size: clamp(3rem, 8vw, 5rem);
        font-weight: 900;
        letter-spacing: 0.25em;
        margin: 1.5rem 0 0.75rem 0;
        color: #CDFF00;
        text-shadow: 
            0 0 40px rgba(205, 255, 0, 0.9),
            0 0 80px rgba(205, 255, 0, 0.5),
            0 5px 10px rgba(0, 0, 0, 0.6);
        animation: titleGlow 3s ease-in-out infinite alternate;
        line-height: 1.1;
        position: relative;
        z-index: 1;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
    }
    
    @keyframes titleGlow {
        0% {
            text-shadow: 
                0 0 30px rgba(205, 255, 0, 0.7),
                0 0 60px rgba(205, 255, 0, 0.4),
                0 5px 10px rgba(0, 0, 0, 0.6);
            transform: scale(1);
        }
        100% {
            text-shadow: 
                0 0 50px rgba(205, 255, 0, 1),
                0 0 100px rgba(205, 255, 0, 0.7),
                0 5px 15px rgba(0, 0, 0, 0.6);
            transform: scale(1.02);
        }
    }
    
    /* SUBTITLE - ENHANCED */
    .storm-subtitle {
        font-size: clamp(1rem, 2.5vw, 1.3rem);
        color: rgba(205, 255, 0, 0.95);
        font-weight: 600;
        margin-top: 1rem;
        line-height: 1.6;
        padding: 0 1.5rem;
        position: relative;
        z-index: 1;
        text-align: center;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
    }
    
    /* DIVIDER WITH ENHANCED GLOW */
    .divider {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #CDFF00 20%, 
            #CDFF00 80%, 
            transparent 100%);
        margin: 2.5rem auto;
        max-width: 800px;
        box-shadow: 0 0 20px rgba(205, 255, 0, 0.6);
        border-radius: 2px;
    }
    
    /* CHAT CONTAINER - FULL GREEN THEME */
    [data-testid="stChatMessageContainer"] {
        background: #0a0a0a !important;
        padding: 1rem 0;
    }
    
    .stChatMessage {
        background: #0a0a0a !important;
        margin: 1rem 0 !important;
    }
    
    .stChatMessage.user > div {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%) !important;
        border: 2.5px solid #CDFF00 !important;
        border-radius: 20px !important;
        padding: 1.25rem 1.5rem !important;
        color: #ffffff !important;
        box-shadow: 
            0 6px 20px rgba(205, 255, 0, 0.35),
            inset 0 1px 0 rgba(205, 255, 0, 0.25) !important;
        font-size: clamp(1rem, 2vw, 1.15rem) !important;
        line-height: 1.6 !important;
        max-width: 85%;
        margin-left: auto !important;
    }
    
    .stChatMessage.assistant > div {
        background: linear-gradient(135deg, #0d1a0d 0%, #1a2a1a 100%) !important;
        border-left: 6px solid #CDFF00 !important;
        border-radius: 20px !important;
        padding: 1.25rem 1.5rem !important;
        color: #ffffff !important;
        box-shadow: 
            0 6px 24px rgba(205, 255, 0, 0.45),
            inset 0 1px 0 rgba(205, 255, 0, 0.25) !important;
        font-size: clamp(1rem, 2vw, 1.15rem) !important;
        line-height: 1.7 !important;
        max-width: 85%;
    }
    
    /* BUTTONS - ENHANCED GREEN THEME */
    .stButton {
        margin: 1rem 0;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #CDFF00 0%, #a8d600 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: clamp(1.05rem, 2.5vw, 1.2rem) !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.15rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 24px rgba(205, 255, 0, 0.5),
            inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        cursor: pointer;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #e0ff33 0%, #CDFF00 100%) !important;
        transform: translateY(-4px) !important;
        box-shadow: 
            0 12px 36px rgba(205, 255, 0, 0.7),
            inset 0 2px 0 rgba(255, 255, 255, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 6px 20px rgba(205, 255, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
    }
    
    /* CHAT INPUT - ENHANCED GREEN THEME */
    [data-testid="stChatInput"] {
        background: #0a0a0a !important;
        padding: 1.5rem 0 !important;
        position: sticky;
        bottom: 0;
        z-index: 100;
    }
    
    .stChatInput input {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%) !important;
        color: #ffffff !important;
        border: 3px solid #CDFF00 !important;
        border-radius: 18px !important;
        transition: all 0.3s ease !important;
        font-size: clamp(1.05rem, 2.5vw, 1.15rem) !important;
        padding: 1.15rem 1.5rem !important;
        box-shadow: 
            0 6px 20px rgba(205, 255, 0, 0.35),
            inset 0 1px 0 rgba(205, 255, 0, 0.15) !important;
    }
    
    .stChatInput input:focus {
        border-color: #CDFF00 !important;
        box-shadow: 
            0 0 0 5px rgba(205, 255, 0, 0.35),
            0 6px 24px rgba(205, 255, 0, 0.55),
            inset 0 1px 0 rgba(205, 255, 0, 0.25) !important;
        background: linear-gradient(135deg, #0d1a0d 0%, #1a2a1a 100%) !important;
        outline: none !important;
    }
    
    .stChatInput input::placeholder {
        color: rgba(205, 255, 0, 0.65) !important;
        font-weight: 500;
    }
    
    /* FOOTER - ENHANCED GREEN THEME */
    .footer {
        text-align: center;
        font-size: clamp(0.9rem, 2vw, 1rem);
        color: rgba(205, 255, 0, 0.85);
        margin-top: 3rem;
        padding: 1.75rem 1.5rem;
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        border-radius: 20px;
        border: 2px solid rgba(205, 255, 0, 0.35);
        box-shadow: 0 0 30px rgba(205, 255, 0, 0.25);
        font-weight: 600;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .footer strong {
        color: #CDFF00;
        font-size: 1.1em;
    }
    
    /* SCROLLBAR - ENHANCED GREEN THEME */
    ::-webkit-scrollbar {
        width: 12px;
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d0d0d;
        border-radius: 6px;
        margin: 4px 0;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #CDFF00 0%, #a8d600 100%);
        border-radius: 6px;
        border: 2px solid #0d0d0d;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #e0ff33 0%, #CDFF00 100%);
    }
    
    /* DESKTOP SPECIFIC ENHANCEMENTS */
    @media (min-width: 769px) {
        .block-container {
            padding: 2rem 2rem 3rem 2rem !important;
        }
        
        .storm-header {
            padding: 3rem 2rem;
        }
        
        .logo-container img {
            width: 220px;
            height: 220px;
        }
        
        .storm-title {
            font-size: clamp(3.5rem, 6vw, 5rem);
        }
        
        .storm-subtitle {
            font-size: clamp(1.1rem, 2vw, 1.35rem);
        }
        
        .stChatMessage.user > div,
        .stChatMessage.assistant > div {
            max-width: 75%;
        }
    }
    
    /* TABLET RESPONSIVE */
    @media (min-width: 481px) and (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1.5rem 2rem 1.5rem !important;
        }
        
        .storm-header {
            padding: 2rem 1.5rem;
        }
        
        .logo-container img {
            width: 180px;
            height: 180px;
        }
    }
    
    /* MOBILE RESPONSIVE - IPHONE OPTIMIZATION */
    @media (max-width: 480px) {
        .block-container {
            padding: max(env(safe-area-inset-top), 1rem) 0.875rem 1.5rem 0.875rem !important;
        }
        
        .storm-header {
            padding: 1.75rem 1rem;
            margin: 0 0 1.25rem 0;
            border-radius: 18px;
        }
        
        .logo-container img {
            width: 160px;
            height: 160px;
        }
        
        .storm-title {
            font-size: clamp(2.25rem, 9vw, 3.25rem);
            letter-spacing: 0.18em;
            margin: 1rem 0 0.5rem 0;
        }
        
        .storm-subtitle {
            font-size: clamp(0.85rem, 3vw, 1.05rem);
            padding: 0 0.875rem;
        }
        
        .divider {
            margin: 1.75rem 0;
        }
        
        .stChatMessage {
            margin: 0.75rem 0 !important;
        }
        
        .stChatMessage.user > div,
        .stChatMessage.assistant > div {
            padding: 1rem 1.15rem !important;
            border-radius: 16px !important;
            max-width: 90%;
            font-size: clamp(0.95rem, 3.5vw, 1.05rem) !important;
        }
        
        .footer {
            margin-top: 2.5rem;
            padding: 1.5rem 1rem;
        }
    }
    
    /* EXTRA SMALL SCREENS */
    @media (max-width: 360px) {
        .logo-container img {
            width: 140px;
            height: 140px;
        }
        
        .storm-title {
            font-size: clamp(2rem, 8vw, 2.75rem);
        }
        
        .storm-subtitle {
            font-size: clamp(0.8rem, 2.8vw, 0.95rem);
        }
    }
    
    /* LANDSCAPE MODE */
    @media (max-height: 500px) and (orientation: landscape) {
        .storm-header {
            padding: 1.25rem 1rem;
            margin-bottom: 1rem;
        }
        
        .logo-container {
            margin-bottom: 0.875rem;
        }
        
        .logo-container img {
            width: 100px;
            height: 100px;
        }
        
        .storm-title {
            font-size: clamp(1.75rem, 6vw, 2.25rem);
            margin: 0.5rem 0 0.35rem 0;
        }
        
        .storm-subtitle {
            font-size: clamp(0.75rem, 2vw, 0.9rem);
            margin-top: 0.5rem;
        }
        
        .divider {
            margin: 1rem 0;
        }
    }
    
    /* LOADING ANIMATION */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(15px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .stChatMessage {
        animation: fadeIn 0.4s ease-out;
    }
    
    /* SELECTION COLOR */
    ::selection {
        background-color: rgba(205, 255, 0, 0.3);
        color: #ffffff;
    }
    
    ::-moz-selection {
        background-color: rgba(205, 255, 0, 0.3);
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HEADER WITH CENTERED LOGO
# ======================================================
with st.container():
    st.markdown('<div class="storm-header">', unsafe_allow_html=True)
    
    # Logo Container - Perfectly Centered with Wrapper
    st.markdown(
        '<div class="logo-container"><div class="logo-wrapper">',
        unsafe_allow_html=True
    )
    st.image("assets/logo(1).jpeg", width=200)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Title and Subtitle
    st.markdown(
        """
        <div class="storm-title">STORM</div>
        <div class="storm-subtitle">
            Wolves of Real Estate AI • Tax Deeds • Tax Liens • Wholesale • Creative Finance
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ======================================================
# SESSION STATE (CHAT MEMORY)
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "🐺 **Welcome to Storm** — the Wolves of Real Estate AI.\n\n"
                "I specialize in **tax deeds, tax liens, wholesale deals, and creative finance strategies**.\n\n"
                "Whether you're analyzing auction properties, calculating ROI on tax liens, "
                "structuring seller financing, or wholesale assignments — I'm here to help you dominate.\n\n"
                "**What deal are we attacking today?**"
            )
        }
    ]

# ======================================================
# DISPLAY CHAT HISTORY
# ======================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================================================
# USER INPUT
# ======================================================
user_input = st.chat_input(
    "Ask Storm about auctions, liens, wholesale spreads, or creative finance strategies…"
)

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ==================================================
    # SEND TO N8N (CLEAN PAYLOAD)
    # ==================================================
    payload = {
        "assistant": "Storm",
        "community": "Wolves of Real Estate",
        "message": user_input,
        "history": st.session_state.messages[-10:],
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
    }

    try:
        with st.spinner("🐺 Storm is analyzing..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=60
            )

        if response.status_code == 200 and response.text:
            storm_reply = response.text.strip()
        else:
            storm_reply = (
                "⚠️ Storm encountered an issue processing your request. "
                "Let's try that again."
            )

    except requests.exceptions.Timeout:
        storm_reply = (
            "⚠️ **Request timed out.** Storm is taking longer than expected. "
            "Please try again or rephrase your question."
        )
    except requests.exceptions.RequestException as e:
        storm_reply = (
            "⚠️ **Connection error:** Unable to reach Storm's server. "
            "Please check your connection and try again."
        )

    # ==================================================
    # DISPLAY RESPONSE
    # ==================================================
    st.session_state.messages.append(
        {"role": "assistant", "content": storm_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(storm_reply)

# ======================================================
# FOOTER + RESET BUTTON
# ======================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("🔄 Reset Conversation", width="stretch"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "🐺 **Conversation Reset**\n\n"
                "Ready to analyze your next deal. What property or strategy "
                "are we working on?"
            )
        }
    ]
    st.rerun()

st.markdown(
    """
    <div class="footer">
        <strong>Wolves of Real Estate © 2025</strong><br>
        Built for serious operators who dominate the market<br>
        <span style="font-size: 0.9em; opacity: 0.8;">Tax Deeds • Tax Liens • Wholesale • Creative Finance</span>
    </div>
    """,
    unsafe_allow_html=True
)
