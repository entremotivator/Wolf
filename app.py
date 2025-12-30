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
    body {
        background-color: #000000;
        color: #ffffff;
    }

    .storm-header {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }

    .storm-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        margin-top: 0.5rem;
        color: #ffffff;
    }

    .storm-subtitle {
        font-size: 1.05rem;
        color: rgba(255,255,255,0.85);
    }

    .divider {
        border-top: 2px solid #CDFF00;
        margin: 1.5rem 0;
    }

    .stChatMessage.user div {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 12px 16px;
        color: #ffffff;
    }

    .stChatMessage.assistant div {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        border-left: 4px solid #CDFF00;
        border-radius: 12px;
        padding: 14px 16px;
        color: #ffffff;
    }

    .stButton button {
        background-color: #CDFF00;
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #b8e600;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(205, 255, 0, 0.3);
    }

    .stChatInput input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 8px;
    }

    .stChatInput input:focus {
        border-color: #CDFF00;
        box-shadow: 0 0 0 1px #CDFF00;
    }

    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.6);
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# ======================================================
with st.container():
    st.markdown('<div class="storm-header">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("/images/logo-281-29.jpeg", width=180)
    
    st.markdown(
        """
        <div class="storm-title">Storm</div>
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
