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

# ======================================================
# N8N WEBHOOK (LIVE TEST URL)
# ======================================================
N8N_WEBHOOK_URL = (
    "https://agentonline-u29564.vm.elestio.app"
    "/webhook-test/f4afadf7-168a-wolf"
)

# ======================================================
# ======================================================
st.markdown(
    """
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #0a0a0a 50%, #000000 100%);
    }
    
    body {
        background-color: #000000;
        color: #ffffff;
    }

    /* Header Section */
    .storm-header {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        border-radius: 16px;
        border: 1px solid #CDFF00;
        box-shadow: 0 0 30px rgba(205, 255, 0, 0.2);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }
    
    .logo-container img {
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(205, 255, 0, 0.3);
        border: 2px solid #CDFF00;
    }

    .storm-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-top: 1rem;
        color: #CDFF00;
        text-shadow: 0 0 20px rgba(205, 255, 0, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 10px rgba(205, 255, 0, 0.5), 0 0 20px rgba(205, 255, 0, 0.3);
        }
        to {
            text-shadow: 0 0 20px rgba(205, 255, 0, 0.8), 0 0 30px rgba(205, 255, 0, 0.5);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .storm-subtitle {
        font-size: 1.1rem;
        color: rgba(205, 255, 0, 0.9);
        font-weight: 500;
        margin-top: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }

    /* Divider */
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #CDFF00 50%, transparent 100%);
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(205, 255, 0, 0.5);
    }

    /* Chat Messages */
    .stChatMessage.user div {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 1px solid #CDFF00;
        border-radius: 16px;
        padding: 14px 18px;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(205, 255, 0, 0.15);
    }

    .stChatMessage.assistant div {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        border-left: 5px solid #CDFF00;
        border-radius: 16px;
        padding: 16px 20px;
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(205, 255, 0, 0.25);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #CDFF00 0%, #b8e600 100%);
        color: #000000;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(205, 255, 0, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #b8e600 0%, #CDFF00 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(205, 255, 0, 0.5);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }

    /* Chat Input */
    .stChatInput {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stChatInput input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #333333;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stChatInput input:focus {
        border-color: #CDFF00;
        box-shadow: 0 0 0 3px rgba(205, 255, 0, 0.2);
        background-color: #0d0d0d;
    }
    
    .stChatInput input::placeholder {
        color: rgba(205, 255, 0, 0.5);
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: rgba(205, 255, 0, 0.7);
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(205, 255, 0, 0.2);
        background: linear-gradient(180deg, transparent 0%, rgba(205, 255, 0, 0.05) 100%);
        border-radius: 8px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CDFF00;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #b8e600;
    }
    
    /* Chat Container */
    .stChatFloatingInputContainer {
        background-color: #000000;
        border-top: 1px solid #CDFF00;
        box-shadow: 0 -4px 12px rgba(205, 255, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# ======================================================
with st.container():
    st.markdown('<div class="storm-header">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("/images/logo-281-29.jpeg", width=200)
    
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
        🐺 Wolves of Real Estate © 2025 • Built for serious operators
    </div>
    """,
    unsafe_allow_html=True
)
