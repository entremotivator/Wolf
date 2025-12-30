import streamlit as st
import requests
from datetime import datetime, timezone

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Storm | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered"
)

st.markdown(
    """
    <meta name="theme-color" content="#CDFF00">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Storm">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
# GLOBAL THEME (NEON YELLOW-GREEN BRAND COLORS)
# ======================================================
st.markdown(
    """
    <style>
    /* Hide all Streamlit branding, menus, and sharing buttons */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    .stAppDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    .css-18e3th9 {padding-top: 0rem;}
    .css-1d391kg {padding-top: 0rem;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* Full-screen mobile theming with green background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #000000 !important;
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #0a0a0a 50%, #000000 100%) !important;
    }
    
    body {
        background-color: #000000;
        color: #ffffff;
    }

    /* Enhanced mobile-responsive header */
    .storm-header {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        padding: 1.5rem 0.75rem;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        border-radius: 16px;
        border: 2px solid #CDFF00;
        box-shadow: 0 0 30px rgba(205, 255, 0, 0.3);
    }
    
    /* Logo container for perfect centering */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        border-radius: 12px;
        border: 3px solid #CDFF00;
        box-shadow: 0 0 25px rgba(205, 255, 0, 0.4);
        max-width: 100%;
        height: auto;
    }

    /* Mobile-optimized STORM title */
    .storm-title {
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 900;
        letter-spacing: 0.15em;
        margin-top: 1rem;
        color: #CDFF00;
        text-shadow: 0 0 20px rgba(205, 255, 0, 0.6);
        animation: glow 2s ease-in-out infinite alternate;
        line-height: 1.2;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 15px rgba(205, 255, 0, 0.6), 0 0 25px rgba(205, 255, 0, 0.4);
        }
        to {
            text-shadow: 0 0 25px rgba(205, 255, 0, 0.9), 0 0 40px rgba(205, 255, 0, 0.6);
        }
    }

    /* Mobile-responsive subtitle */
    .storm-subtitle {
        font-size: clamp(0.75rem, 2.5vw, 1.1rem);
        color: rgba(205, 255, 0, 0.9);
        font-weight: 500;
        margin-top: 0.5rem;
        line-height: 1.4;
        padding: 0 0.5rem;
    }

    /* Divider */
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #CDFF00 50%, transparent 100%);
        margin: 1.5rem 0;
        box-shadow: 0 0 10px rgba(205, 255, 0, 0.3);
    }

    /* Mobile-optimized chat messages */
    .stChatMessage.user div {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 2px solid #CDFF00;
        border-radius: 16px;
        padding: 12px 16px;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(205, 255, 0, 0.2);
        font-size: clamp(0.9rem, 3vw, 1rem);
    }

    .stChatMessage.assistant div {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        border-left: 5px solid #CDFF00;
        border-radius: 16px;
        padding: 14px 18px;
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(205, 255, 0, 0.3);
        font-size: clamp(0.9rem, 3vw, 1rem);
    }

    /* Mobile-optimized buttons */
    .stButton button {
        background: linear-gradient(135deg, #CDFF00 0%, #b8e600 100%);
        color: #000000;
        font-weight: 700;
        font-size: clamp(0.9rem, 3vw, 1rem);
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(205, 255, 0, 0.4);
        width: 100%;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #b8e600 0%, #CDFF00 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(205, 255, 0, 0.6);
    }

    /* Mobile-optimized chat input */
    .stChatInput input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #CDFF00;
        border-radius: 12px;
        transition: all 0.3s ease;
        font-size: clamp(0.9rem, 3vw, 1rem);
        padding: 0.875rem 1rem;
    }

    .stChatInput input:focus {
        border-color: #CDFF00;
        box-shadow: 0 0 0 3px rgba(205, 255, 0, 0.3);
        background-color: #0d0d0d;
    }
    
    .stChatInput input::placeholder {
        color: rgba(205, 255, 0, 0.6);
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: clamp(0.75rem, 2.5vw, 0.85rem);
        color: rgba(205, 255, 0, 0.7);
        margin-top: 2rem;
        padding: 1rem;
    }
    
    /* Mobile-optimized scrollbar with green theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CDFF00;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #b8e600;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .storm-header {
            padding: 1rem 0.5rem;
            margin-top: 0.25rem;
        }
        
        .stChatMessage {
            margin: 0.5rem 0 !important;
        }
        
        .divider {
            margin: 1rem 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HEADER + LOGO (PERFECTLY CENTERED)
# ======================================================
with st.container():
    st.markdown('<div class="storm-header">', unsafe_allow_html=True)
    
    st.markdown(
        '<div class="logo-container">',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo(1).jpeg", width=200)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                "I'm **Storm**, the Wolves of Real Estate AI.\n\n"
                "I help serious investors dominate **tax deeds, tax liens, wholesale, "
                "and creative finance**.\n\n"
                "Bring me a deal, auction, or strategy — we'll break it down professionally."
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
        "history": st.session_state.messages[-10:],  # limit memory
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
            storm_reply = "⚠️ Storm did not return a response."

    except requests.exceptions.RequestException as e:
        storm_reply = f"⚠️ Connection error: {e}"

    # ==================================================
    # DISPLAY RESPONSE
    # ==================================================
    st.session_state.messages.append(
        {"role": "assistant", "content": storm_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(storm_reply)

# ======================================================
# FOOTER + RESET
# ======================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("🔄 Reset Conversation", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Conversation reset. What deal are we analyzing next?"
        }
    ]
    st.rerun()

st.markdown(
    """
    <div class="footer">
        Wolves of Real Estate © 2025 • Built for serious operators
    </div>
    """,
    unsafe_allow_html=True
)
