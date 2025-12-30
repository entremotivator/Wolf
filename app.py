import streamlit as st
import requests
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Storm | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered"
)

# ======================================================
# N8N WEBHOOK (FIXED)
# ======================================================
N8N_WEBHOOK_URL = (
    "https://agentonline-u29564.vm.elestio.app"
    "/webhook/f4afadf7-168a-wolf"
)

# ======================================================
# GLOBAL THEME (DARK / PREMIUM)
# ======================================================
st.markdown(
    """
    <style>
    body {
        background-color: #0b0f16;
        color: #e5e7eb;
    }

    .storm-header {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .storm-title {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }

    .storm-subtitle {
        font-size: 1.05rem;
        opacity: 0.8;
    }

    .divider {
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.5rem 0;
    }

    .stChatMessage.user div {
        background: #111827;
        border-radius: 12px;
        padding: 12px 16px;
    }

    .stChatMessage.assistant div {
        background: #020617;
        border-left: 3px solid #22c55e;
        border-radius: 12px;
        padding: 14px 16px;
    }

    .footer {
        text-align: center;
        font-size: 0.75rem;
        opacity: 0.55;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HEADER / LOGO
# ======================================================
st.markdown(
    """
    <div class="storm-header">
        <img src="https://raw.githubusercontent.com/your-org/assets/main/logo(1).jpeg"
             width="120"
             style="margin-bottom:10px;" />
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
# SESSION STATE (MEMORY)
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "I’m **Storm**, Wolves of Real Estate AI.\n\n"
                "I specialize in **tax deeds, tax liens, wholesale, and creative finance**.\n\n"
                "Bring me a deal, an auction, or a strategy — we’ll break it down professionally."
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
    # Add user message locally
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ==================================================
    # SEND TO N8N (FIXED PAYLOAD)
    # ==================================================
    payload = {
        "assistant": "Storm",
        "community": "Wolves of Real Estate",
        "message": user_input,
        "history": st.session_state.messages[-10:],  # limit memory
        "timestamp": datetime.utcnow().isoformat()
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
            storm_reply = "⚠️ Storm didn’t return a response."

    except requests.exceptions.RequestException as e:
        storm_reply = f"⚠️ Connection error: {e}"

    # ==================================================
    # DISPLAY ASSISTANT RESPONSE
    # ==================================================
    st.session_state.messages.append(
        {"role": "assistant", "content": storm_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(storm_reply)

# ======================================================
# FOOTER CONTROLS
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
