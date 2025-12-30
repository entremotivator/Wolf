import streamlit as st
import requests
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Storm | Wolves of Real Estate",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

N8N_WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook-test/f4afadf7-168a-wolf"

# =========================================================
# THEME & GLOBAL STYLES
# =========================================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #0e1117;
        color: #f5f5f5;
        font-family: 'Inter', sans-serif;
    }

    .storm-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }

    .storm-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        letter-spacing: 0.5px;
    }

    .storm-subtitle {
        font-size: 1.05rem;
        opacity: 0.85;
    }

    .storm-divider {
        margin: 1.25rem 0;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    .stChatMessage {
        background: transparent;
    }

    .stChatMessage.user div {
        background: linear-gradient(135deg, #1f2937, #111827);
        border-radius: 12px;
        padding: 12px 16px;
    }

    .stChatMessage.assistant div {
        background: linear-gradient(135deg, #111827, #020617);
        border-left: 3px solid #22c55e;
        border-radius: 12px;
        padding: 14px 16px;
    }

    .storm-footer {
        text-align: center;
        font-size: 0.8rem;
        opacity: 0.6;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOGO + HEADER
# =========================================================
with st.container():
    st.markdown(
        """
        <div class="storm-header">
            <img src="https://raw.githubusercontent.com/YOUR-REPO/assets/main/wolves_logo.png"
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

st.markdown('<div class="storm-divider"></div>', unsafe_allow_html=True)

# =========================================================
# SESSION MEMORY
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "I’m **Storm**, the Wolves of Real Estate AI.\n\n"
                "I help investors dominate **tax deeds, tax liens, wholesale, and creative finance**.\n\n"
                "Bring me a deal, a number, or a strategy — we’ll break it down like professionals."
            )
        }
    ]

# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# CHAT INPUT
# =========================================================
user_input = st.chat_input(
    "Ask about auctions, liens, wholesale spreads, seller finance, or deal structure…"
)

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # =====================================================
    # SEND TO N8N
    # =====================================================
    payload = {
        "assistant": "Storm",
        "community": "Wolves of Real Estate",
        "message": user_input,
        "conversation": st.session_state.messages,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=90
        )

        if response.status_code == 200:
            storm_reply = response.text.strip()
        else:
            storm_reply = "⚠️ Storm is unavailable. Try again shortly."

    except Exception as e:
        storm_reply = f"⚠️ Connection error: {e}"

    # =====================================================
    # DISPLAY RESPONSE
    # =====================================================
    st.session_state.messages.append(
        {"role": "assistant", "content": storm_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(storm_reply)

# =========================================================
# FOOTER CONTROLS
# =========================================================
st.markdown('<div class="storm-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🗑 Reset Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Conversation reset.\n\n"
                    "What real estate play are we executing next?"
                )
            }
        ]
        st.rerun()

st.markdown(
    """
    <div class="storm-footer">
        Wolves of Real Estate © 2025 • Built for serious operators
    </div>
    """,
    unsafe_allow_html=True
)
