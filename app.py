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
# FULL MOBILE THEME - GREEN BACKGROUND EVERYWHERE
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
    
    /* FULL SCREEN DARK GREEN THEME FOR IPHONE */
    * {
        -webkit-tap-highlight-color: rgba(205, 255, 0, 0.2);
    }
    
    html {
        background: #0a0a0a !important;
        overflow-x: hidden;
    }
    
    body {
        background: #0a0a0a !important;
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp,
    .main {
        background: #0a0a0a !important;
        min-height: 100vh;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .block-container {
        padding: env(safe-area-inset-top) 1rem 1rem 1rem !important;
        max-width: 100% !important;
        background: #0a0a0a !important;
    }
    
    /* ENHANCED MOBILE HEADER WITH PERFECT CENTERING */
    .storm-header {
        text-align: center;
        margin: 0 auto 1.5rem auto;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        border-radius: 20px;
        border: 3px solid #CDFF00;
        box-shadow: 
            0 0 40px rgba(205, 255, 0, 0.4),
            inset 0 0 20px rgba(205, 255, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .storm-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(205, 255, 0, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    /* LOGO CONTAINER - PERFECTLY CENTERED */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-container img {
        width: 180px;
        height: 180px;
        border-radius: 20px;
        border: 4px solid #CDFF00;
        box-shadow: 
            0 0 40px rgba(205, 255, 0, 0.6),
            0 8px 32px rgba(0, 0, 0, 0.4);
        object-fit: cover;
        display: block;
        margin: 0 auto;
    }
    
    /* STORM TITLE - ENHANCED MOBILE */
    .storm-title {
        font-size: clamp(2.5rem, 10vw, 4rem);
        font-weight: 900;
        letter-spacing: 0.2em;
        margin: 1rem 0 0.5rem 0;
        color: #CDFF00;
        text-shadow: 
            0 0 30px rgba(205, 255, 0, 0.8),
            0 0 60px rgba(205, 255, 0, 0.4),
            0 4px 8px rgba(0, 0, 0, 0.5);
        animation: titleGlow 3s ease-in-out infinite alternate;
        line-height: 1.1;
        position: relative;
        z-index: 1;
        text-align: center;
    }
    
    @keyframes titleGlow {
        0% {
            text-shadow: 
                0 0 20px rgba(205, 255, 0, 0.6),
                0 0 40px rgba(205, 255, 0, 0.3),
                0 4px 8px rgba(0, 0, 0, 0.5);
            transform: scale(1);
        }
        100% {
            text-shadow: 
                0 0 40px rgba(205, 255, 0, 1),
                0 0 80px rgba(205, 255, 0, 0.6),
                0 4px 12px rgba(0, 0, 0, 0.5);
            transform: scale(1.02);
        }
    }
    
    /* SUBTITLE - MOBILE OPTIMIZED */
    .storm-subtitle {
        font-size: clamp(0.85rem, 3vw, 1.2rem);
        color: rgba(205, 255, 0, 0.95);
        font-weight: 600;
        margin-top: 0.75rem;
        line-height: 1.5;
        padding: 0 1rem;
        position: relative;
        z-index: 1;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* DIVIDER WITH GLOW */
    .divider {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #CDFF00 20%, 
            #CDFF00 80%, 
            transparent 100%);
        margin: 2rem 0;
        box-shadow: 0 0 15px rgba(205, 255, 0, 0.5);
        border-radius: 2px;
    }
    
    /* CHAT MESSAGES - FULL GREEN THEME */
    [data-testid="stChatMessageContainer"] {
        background: #0a0a0a !important;
        padding: 0.5rem 0;
    }
    
    .stChatMessage {
        background: #0a0a0a !important;
        margin: 0.75rem 0 !important;
    }
    
    .stChatMessage.user > div {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%) !important;
        border: 2px solid #CDFF00 !important;
        border-radius: 18px !important;
        padding: 1rem 1.25rem !important;
        color: #ffffff !important;
        box-shadow: 
            0 4px 16px rgba(205, 255, 0, 0.3),
            inset 0 1px 0 rgba(205, 255, 0, 0.2) !important;
        font-size: clamp(0.95rem, 3.5vw, 1.1rem) !important;
        line-height: 1.5 !important;
    }
    
    .stChatMessage.assistant > div {
        background: linear-gradient(135deg, #0d1a0d 0%, #1a2a1a 100%) !important;
        border-left: 5px solid #CDFF00 !important;
        border-radius: 18px !important;
        padding: 1.1rem 1.25rem !important;
        color: #ffffff !important;
        box-shadow: 
            0 4px 20px rgba(205, 255, 0, 0.4),
            inset 0 1px 0 rgba(205, 255, 0, 0.2) !important;
        font-size: clamp(0.95rem, 3.5vw, 1.1rem) !important;
        line-height: 1.6 !important;
    }
    
    /* BUTTONS - FULL GREEN THEME */
    .stButton button {
        background: linear-gradient(135deg, #CDFF00 0%, #a8d600 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: clamp(1rem, 3.5vw, 1.1rem) !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 6px 20px rgba(205, 255, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #e0ff33 0%, #CDFF00 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 
            0 10px 30px rgba(205, 255, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
        box-shadow: 
            0 4px 15px rgba(205, 255, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    /* CHAT INPUT - FULL GREEN THEME */
    [data-testid="stChatInput"] {
        background: #0a0a0a !important;
        padding: 1rem 0 !important;
    }
    
    .stChatInput input {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%) !important;
        color: #ffffff !important;
        border: 3px solid #CDFF00 !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
        font-size: clamp(1rem, 3.5vw, 1.1rem) !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 
            0 4px 16px rgba(205, 255, 0, 0.3),
            inset 0 1px 0 rgba(205, 255, 0, 0.1) !important;
    }
    
    .stChatInput input:focus {
        border-color: #CDFF00 !important;
        box-shadow: 
            0 0 0 4px rgba(205, 255, 0, 0.3),
            0 4px 20px rgba(205, 255, 0, 0.5),
            inset 0 1px 0 rgba(205, 255, 0, 0.2) !important;
        background: linear-gradient(135deg, #0d1a0d 0%, #1a2a1a 100%) !important;
        outline: none !important;
    }
    
    .stChatInput input::placeholder {
        color: rgba(205, 255, 0, 0.6) !important;
        font-weight: 500;
    }
    
    /* FOOTER - GREEN THEME */
    .footer {
        text-align: center;
        font-size: clamp(0.8rem, 2.5vw, 0.9rem);
        color: rgba(205, 255, 0, 0.8);
        margin-top: 2.5rem;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        border-radius: 16px;
        border: 2px solid rgba(205, 255, 0, 0.3);
        box-shadow: 0 0 20px rgba(205, 255, 0, 0.2);
        font-weight: 600;
    }
    
    /* SCROLLBAR - GREEN THEME */
    ::-webkit-scrollbar {
        width: 10px;
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d0d0d;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #CDFF00 0%, #a8d600 100%);
        border-radius: 5px;
        border: 2px solid #0d0d0d;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #e0ff33 0%, #CDFF00 100%);
    }
    
    /* MOBILE RESPONSIVE - IPHONE OPTIMIZATION */
    @media (max-width: 768px) {
        .block-container {
            padding: max(env(safe-area-inset-top), 1rem) 0.75rem 1rem 0.75rem !important;
        }
        
        .storm-header {
            padding: 1.5rem 0.75rem;
            margin: 0 0 1rem 0;
            border-radius: 16px;
        }
        
        .logo-container img {
            width: 150px;
            height: 150px;
        }
        
        .storm-title {
            font-size: clamp(2rem, 9vw, 3rem);
            letter-spacing: 0.15em;
        }
        
        .storm-subtitle {
            font-size: clamp(0.8rem, 2.8vw, 1rem);
            padding: 0 0.75rem;
        }
        
        .divider {
            margin: 1.5rem 0;
        }
        
        .stChatMessage {
            margin: 0.6rem 0 !important;
        }
        
        .stChatMessage.user > div,
        .stChatMessage.assistant > div {
            padding: 0.9rem 1rem !important;
            border-radius: 14px !important;
        }
        
        .footer {
            margin-top: 2rem;
            padding: 1.25rem 0.75rem;
        }
    }
    
    /* EXTRA SMALL SCREENS */
    @media (max-width: 380px) {
        .logo-container img {
            width: 130px;
            height: 130px;
        }
        
        .storm-title {
            font-size: clamp(1.75rem, 8vw, 2.5rem);
        }
        
        .storm-subtitle {
            font-size: clamp(0.75rem, 2.5vw, 0.9rem);
        }
    }
    
    /* LANDSCAPE MODE */
    @media (max-height: 500px) and (orientation: landscape) {
        .storm-header {
            padding: 1rem 0.75rem;
        }
        
        .logo-container {
            margin-bottom: 0.75rem;
        }
        
        .logo-container img {
            width: 100px;
            height: 100px;
        }
        
        .storm-title {
            font-size: clamp(1.5rem, 6vw, 2rem);
            margin: 0.5rem 0 0.25rem 0;
        }
        
        .storm-subtitle {
            font-size: clamp(0.7rem, 2vw, 0.85rem);
            margin-top: 0.5rem;
        }
    }
    
    /* LOADING ANIMATION */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stChatMessage {
        animation: fadeIn 0.3s ease-out;
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
    
    # Logo Container - Perfectly Centered
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("assets/logo(1).jpeg", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                "Whether you're analyzing auction properties, calculating ROI, or structuring creative financing — "
                "I'm here to help you dominate the market.\n\n"
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
    "Ask Storm about auctions, liens, wholesale spreads, or creative finance…"
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
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=60
        )

        if response.status_code == 200 and response.text:
            storm_reply = response.text.strip()
        else:
            storm_reply = "⚠️ Storm encountered an issue. Let's try that again."

    except requests.exceptions.RequestException as e:
        storm_reply = f"⚠️ Connection error: Unable to reach Storm's server. Please check your connection."

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

if st.button("🔄 Reset Conversation", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "🐺 **Conversation Reset**\n\n"
                "Ready to analyze your next deal. What are we working on?"
            )
        }
    ]
    st.rerun()

st.markdown(
    """
    <div class="footer">
        <strong>Wolves of Real Estate © 2025</strong><br>
        Built for serious operators who dominate the market
    </div>
    """,
    unsafe_allow_html=True
)
