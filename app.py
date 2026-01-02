import streamlit as st
import requests
import base64
import os
import json
from datetime import datetime, timezone
from typing import List, Dict


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
# 2. CORE CONFIGURATION & BRANDING
# ======================================================
N8N_WEBHOOK_URL = (
    "https://agentonline-u29564.vm.elestio.app"
    "/webhook/f4afadf7-168a-wolf"
)
PRIMARY_GREEN = "#CDFF00"
SECONDARY_GREEN = "#39FF14"
DEEP_BG = "#020802"
MID_BG = "#051205"
ACCENT_GLOW = "rgba(205, 255, 0, 0.2)"


# ======================================================
# 3. ROBUST IMAGE LOADING (BASE64)
# ======================================================
def get_base64_image(image_filename):
    """Searches for images and returns them as base64 strings for HTML embedding."""
    possible_paths = [
        os.path.join("assets", image_filename),
        os.path.join("/home/ubuntu/upload", image_filename),
        image_filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                ext = image_filename.split('.')[-1].lower()
                mime_type = f"image/{ext}" if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp'] else "image/jpeg"
                return f"data:{mime_type};base64,{encoded}"
    
    return "https://raw.githubusercontent.com/manus-ai/assets/main/wolf_logo.png"

LOGO_DATA = get_base64_image("logo(1).jpeg")
CHATBOT_ICON_DATA = get_base64_image("IMG_1100.png")


# ======================================================
# 4. ADVANCED CUSTOM CSS WITH STEALTH MODE
# ======================================================
# Hide Streamlit branding, menu, footer, and profile elements
st.markdown(
    f"""
    <style>
    /* ============================================
       STREAMLIT BRANDING REMOVAL - MAXIMUM STEALTH
       ============================================ */
    
    /* Hide Streamlit header, menu, footer, and all branding */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Hide "Made with Streamlit" footer */
    .css-1dp5vir {{display: none;}}
    .css-164nlkn {{display: none;}}
    footer {{display: none !important;}}
    .viewerBadge_link__1S137 {{display: none !important;}}
    .viewerBadge_container__1QSob {{display: none !important;}}
    
    /* Hide hamburger menu and settings */
    button[title="View fullscreen"] {{display: none;}}
    button[kind="header"] {{display: none;}}
    [data-testid="stToolbar"] {{display: none !important;}}
    [data-testid="stDecoration"] {{display: none !important;}}
    [data-testid="stStatusWidget"] {{display: none !important;}}
    
    /* Hide deploy button and app menu */
    .css-18e3th9 {{display: none;}}
    .css-1dp5vir {{display: none;}}
    
    /* Hide profile/avatar icon */
    [data-testid="manage-app-button"] {{display: none;}}
    
    /* Remove top padding caused by hidden header */
    .block-container {{
        padding-top: 2rem !important;
    }}
    
    /* Hide hosting message if present */
    [data-testid="stAppViewBlockContainer"] > div:first-child {{
        display: none;
    }}
    
    /* ============================================
       STORM BRAND STYLES
       ============================================ */
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* Background & Body */
    .stApp {{
        background: linear-gradient(180deg, {DEEP_BG} 0%, {MID_BG} 50%, {DEEP_BG} 100%);
        color: #FFFFFF;
    }}
    
    /* Hide default Streamlit elements */
    .css-1v0mbdj {{display: none;}}
    
    /* ============================================
       STORM HEADER
       ============================================ */
    .storm-header-container {{
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border-radius: 30px;
        border: 3px solid {PRIMARY_GREEN}22;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 80px {ACCENT_GLOW};
    }}
    
    .logo-outer-frame {{
        display: inline-block;
        padding: 8px;
        background: linear-gradient(135deg, {PRIMARY_GREEN}44 0%, {SECONDARY_GREEN}22 100%);
        border-radius: 50%;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px {ACCENT_GLOW};
        animation: logo-pulse 3s ease-in-out infinite;
    }}
    
    @keyframes logo-pulse {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 8px 32px {ACCENT_GLOW}; }}
        50% {{ transform: scale(1.05); box-shadow: 0 12px 48px {ACCENT_GLOW}; }}
    }}
    
    .logo-outer-frame img {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid {PRIMARY_GREEN};
    }}
    
    .main-title {{
        font-size: 4rem;
        font-weight: 900;
        color: {PRIMARY_GREEN};
        margin: 0.5rem 0;
        letter-spacing: 0.3em;
        text-shadow: 0 0 40px {ACCENT_GLOW}, 0 0 80px {ACCENT_GLOW};
        animation: title-glow 2s ease-in-out infinite;
    }}
    
    @keyframes title-glow {{
        0%, 100% {{ text-shadow: 0 0 40px {ACCENT_GLOW}, 0 0 80px {ACCENT_GLOW}; }}
        50% {{ text-shadow: 0 0 60px {ACCENT_GLOW}, 0 0 120px {ACCENT_GLOW}; }}
    }}
    
    .sub-title {{
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }}
    
    /* ============================================
       GREETING SECTION WITH CHATBOT
       ============================================ */
    .greeting-section {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 2px solid {PRIMARY_GREEN}33;
        border-radius: 25px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}
    
    .greeting-text {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    .greeting-text h2 {{
        color: {PRIMARY_GREEN};
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.05em;
    }}
    
    .chatbot-icon {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid {PRIMARY_GREEN};
        box-shadow: 0 0 30px {ACCENT_GLOW};
        animation: icon-float 3s ease-in-out infinite;
    }}
    
    @keyframes icon-float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .chatbot-icon-small {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid {PRIMARY_GREEN};
        box-shadow: 0 0 20px {ACCENT_GLOW};
        animation: icon-float 3s ease-in-out infinite;
    }}
    
    /* ============================================
       INFO SECTION
       ============================================ */
    .info-section {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border-left: 5px solid {PRIMARY_GREEN};
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }}
    
    .info-section h3 {{
        color: {PRIMARY_GREEN};
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    .info-section ul {{
        list-style: none;
        padding: 0;
    }}
    
    .info-section li {{
        padding: 0.75rem 0;
        color: rgba(255,255,255,0.9);
        line-height: 1.7;
        border-bottom: 1px solid {PRIMARY_GREEN}11;
    }}
    
    .info-section li:last-child {{
        border-bottom: none;
    }}
    
    .info-section strong {{
        color: {PRIMARY_GREEN};
        font-weight: 700;
    }}
    
    /* ============================================
       FEATURE CARDS
       ============================================ */
    .feature-card {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 2px solid {PRIMARY_GREEN}22;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        border-color: {PRIMARY_GREEN}55;
        box-shadow: 0 12px 40px {ACCENT_GLOW};
    }}
    
    .feature-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        min-width: 60px;
        text-align: center;
    }}
    
    .feature-title {{
        color: {PRIMARY_GREEN};
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.05em;
    }}
    
    .feature-description {{
        color: rgba(255,255,255,0.85);
        line-height: 1.7;
        font-size: 1rem;
        margin: 0;
    }}
    
    /* ============================================
       TABS STYLING
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: {MID_BG};
        border-radius: 15px;
        padding: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 10px;
        color: rgba(255,255,255,0.6);
        font-weight: 700;
        font-size: 1rem;
        padding: 1rem 1.5rem;
        border: 2px solid transparent;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {PRIMARY_GREEN}11;
        color: {PRIMARY_GREEN};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {PRIMARY_GREEN}22;
        color: {PRIMARY_GREEN};
        border-color: {PRIMARY_GREEN}55;
    }}
    
    /* ============================================
       CHAT INTERFACE
       ============================================ */
    .stChatMessage {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 1px solid {PRIMARY_GREEN}22;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}
    
    .stChatMessage[data-testid="user-message"] {{
        border-left: 4px solid {SECONDARY_GREEN};
    }}
    
    .stChatMessage[data-testid="assistant-message"] {{
        border-left: 4px solid {PRIMARY_GREEN};
    }}
    
    /* ============================================
       INPUT & BUTTONS
       ============================================ */
    .stTextInput > div > div > input {{
        background-color: {MID_BG};
        color: #FFFFFF;
        border: 2px solid {PRIMARY_GREEN}33;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY_GREEN};
        box-shadow: 0 0 20px {ACCENT_GLOW};
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_GREEN} 0%, {SECONDARY_GREEN} 100%);
        color: {DEEP_BG};
        font-weight: 800;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px {ACCENT_GLOW};
    }}
    
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {SECONDARY_GREEN} 0%, {PRIMARY_GREEN} 100%);
        color: {DEEP_BG};
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
    }}
    
    /* ============================================
       EXPANDER STYLING
       ============================================ */
    .streamlit-expanderHeader {{
        background-color: {MID_BG};
        color: {PRIMARY_GREEN};
        border: 2px solid {PRIMARY_GREEN}33;
        border-radius: 12px;
        font-weight: 700;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {PRIMARY_GREEN}11;
        border-color: {PRIMARY_GREEN}55;
    }}
    
    /* ============================================
       SCROLLBAR STYLING
       ============================================ */
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {DEEP_BG};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {PRIMARY_GREEN}55;
        border-radius: 6px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {PRIMARY_GREEN};
    }}
    
    /* ============================================
       MOBILE RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2.5rem;
            letter-spacing: 0.2em;
        }}
        
        .logo-outer-frame img {{
            width: 80px;
            height: 80px;
        }}
        
        .chatbot-icon {{
            width: 60px;
            height: 60px;
        }}
        
        .greeting-text h2 {{
            font-size: 1.8rem;
        }}
        
        .feature-card {{
            padding: 1.5rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# 5. UTILITY FUNCTIONS
# ======================================================

def count_message_stats() -> Dict[str, int]:
    """Calculate message statistics."""
    total = len(st.session_state.messages)
    user_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
    assistant_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "assistant")
    return {
        "total": total,
        "user": user_msgs,
        "assistant": assistant_msgs
    }

def export_conversation_json():
    """Export conversation to JSON format."""
    export_data = {
        "session_id": st.session_state.get("session_id", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stats": count_message_stats(),
        "conversation": st.session_state.messages
    }
    return json.dumps(export_data, indent=2)

def export_conversation_text():
    """Export conversation to plain text format."""
    lines = []
    lines.append("=" * 60)
    lines.append("STORM CONVERSATION EXPORT")
    lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("")
    
    for msg in st.session_state.messages:
        role = "YOU" if msg["role"] == "user" else "STORM"
        lines.append(f"[{role}]")
        lines.append(msg["content"])
        lines.append("")
        lines.append("-" * 60)
        lines.append("")
    
    stats = count_message_stats()
    lines.append("STATISTICS")
    lines.append(f"Total Messages: {stats['total']}")
    lines.append(f"Your Messages: {stats['user']}")
    lines.append(f"Storm Responses: {stats['assistant']}")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def export_conversation_markdown():
    """Export conversation to markdown format."""
    lines = []
    lines.append("# 🐺 Storm Conversation Export")
    lines.append(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lines.append(f"### 👤 You")
            lines.append(msg["content"])
        else:
            lines.append(f"### 🐺 Storm")
            lines.append(msg["content"])
        lines.append("")
    
    lines.append("---")
    lines.append("")
    stats = count_message_stats()
    lines.append("## 📊 Statistics")
    lines.append(f"- **Total Messages:** {stats['total']}")
    lines.append(f"- **Your Messages:** {stats['user']}")
    lines.append(f"- **Storm Responses:** {stats['assistant']}")
    
    return "\n".join(lines)


# ======================================================
# 6. UI COMPONENT RENDERING
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
            <div style="margin-top: 2rem; display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">TAX DEEDS</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">TAX LIENS</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">WHOLESALE</span>
                <span style="background: {PRIMARY_GREEN}15; color: {PRIMARY_GREEN}; padding: 6px 16px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; border: 1px solid {PRIMARY_GREEN}33;">CREATIVE FINANCE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_greeting_section():
    """Render the greeting section with chatbot icon."""
    st.markdown(
        f"""
        <div class="greeting-section">
            <div class="greeting-text">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm Chatbot" class="chatbot-icon">
                <h2>Hi I'm Storm</h2>
            </div>
            <p style="text-align: center; color: rgba(255,255,255,0.8); margin-top: 1.5rem; font-size: 1.1rem; line-height: 1.8;">
                Your specialized AI assistant for <strong style="color: {PRIMARY_GREEN};">tax deeds, tax liens, wholesale deals, and creative finance strategies</strong>. 
                I'm here to help you analyze properties, calculate ROI, structure deals, and dominate the real estate market with data-driven insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_stats_dashboard():
    """Render conversation statistics dashboard."""
    stats = count_message_stats()
    
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            <div style="background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%); border: 2px solid {PRIMARY_GREEN}33; border-radius: 20px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: {PRIMARY_GREEN};">{stats['total']}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.5rem;">Total Messages</div>
            </div>
            <div style="background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%); border: 2px solid {PRIMARY_GREEN}33; border-radius: 20px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: {SECONDARY_GREEN};">{stats['user']}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.5rem;">Your Questions</div>
            </div>
            <div style="background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%); border: 2px solid {PRIMARY_GREEN}33; border-radius: 20px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: {PRIMARY_GREEN};">{stats['assistant']}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.5rem;">Storm Responses</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_chat_insights():
    """Render insights about the current conversation."""
    stats = count_message_stats()
    
    if stats['total'] > 1:
        insights = []
        
        if stats['user'] >= 5:
            insights.append("💬 You're having a detailed conversation with Storm")
        if stats['total'] >= 10:
            insights.append("🔥 This is turning into a productive session")
        if stats['user'] >= 10:
            insights.append("🎯 You're really diving deep into real estate strategies")
        
        if insights:
            st.markdown(
                f"""
                <div style="background: {MID_BG}; border-left: 4px solid {PRIMARY_GREEN}; border-radius: 15px; padding: 1.5rem; margin: 2rem 0;">
                    <div style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.1em;">Session Insights</div>
                    <div style="color: rgba(255,255,255,0.85); line-height: 1.8;">
                        {"<br>".join(insights)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_conversation_topics():
    """Analyze and display conversation topics."""
    if len(st.session_state.messages) > 1:
        # Extract keywords from user messages
        user_messages = [msg["content"].lower() for msg in st.session_state.messages if msg["role"] == "user"]
        all_text = " ".join(user_messages)
        
        topics_found = []
        topic_keywords = {
            "Tax Deeds": ["tax deed", "auction", "bidding", "county auction"],
            "Tax Liens": ["tax lien", "lien", "redemption", "interest rate"],
            "Wholesale": ["wholesale", "assignment", "arv", "spread"],
            "Creative Finance": ["seller financing", "lease option", "subject-to", "creative finance"],
            "ROI Analysis": ["roi", "return", "profit", "cash flow"],
            "Due Diligence": ["due diligence", "title", "research", "inspection"],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                topics_found.append(topic)
        
        if topics_found:
            st.markdown(
                f"""
                <div style="margin: 2rem 0;">
                    <div style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.1em;">Topics Discussed</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.75rem;">
                        {"".join([f'<span style="background: {PRIMARY_GREEN}22; border: 1px solid {PRIMARY_GREEN}44; color: {PRIMARY_GREEN}; padding: 0.5rem 1rem; border-radius: 15px; font-size: 0.85rem; font-weight: 600;">{topic}</span>' for topic in topics_found])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_expertise_section():
    """Render the expertise information section."""
    st.markdown(
        f"""
        <div class="info-section">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h3 style="margin: 0;">Storm's Expertise</h3>
            </div>
            <p>Storm is your specialized AI assistant for real estate investment strategies. Here's what Storm can help you with:</p>
            <ul>
                <li><strong>Tax Deed Analysis:</strong> Evaluate auction properties, calculate equity positions, assess risks, and determine bidding strategies</li>
                <li><strong>Tax Lien Investing:</strong> Analyze interest rates, redemption periods, lien priorities, and portfolio diversification strategies</li>
                <li><strong>Wholesale Deals:</strong> Calculate assignment fees, analyze ARV (After Repair Value), estimate repair costs, and evaluate deal spreads</li>
                <li><strong>Creative Finance:</strong> Structure seller financing, owner carries, lease options, subject-to deals, and wrap-around mortgages</li>
                <li><strong>Market Analysis:</strong> Research county auction schedules, analyze market trends, and identify high-opportunity zones</li>
                <li><strong>ROI Calculations:</strong> Project returns, calculate cash-on-cash returns, IRR, and break-even analysis</li>
                <li><strong>Due Diligence:</strong> Property research, title checks, lien searches, and risk assessment frameworks</li>
                <li><strong>Exit Strategies:</strong> Flip analysis, rental property evaluation, and portfolio scaling strategies</li>
                <li><strong>Negotiation Tactics:</strong> Deal structuring, counter-offer strategies, and win-win scenario creation</li>
                <li><strong>Legal Compliance:</strong> Understanding state-specific laws, redemption rights, and investor protections</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_feature_cards():
    """Render detailed feature cards."""
    features = [
        {
            "icon": "🏛️",
            "title": "Tax Deed Mastery",
            "description": "Navigate county auctions like a pro. Storm helps you identify undervalued properties, calculate maximum bid amounts, assess title risks, and structure your acquisition strategy for maximum ROI."
        },
        {
            "icon": "💰",
            "title": "Tax Lien Intelligence",
            "description": "Build a profitable tax lien portfolio. Get expert guidance on interest rate analysis, redemption period evaluation, county-specific rules, and diversification strategies to minimize risk while maximizing returns."
        },
        {
            "icon": "🤝",
            "title": "Wholesale Deal Analyzer",
            "description": "Master the art of wholesaling. Calculate optimal assignment fees, evaluate ARV with precision, estimate repair costs accurately, and ensure your deals have enough spread to satisfy both you and your buyers."
        },
        {
            "icon": "🎯",
            "title": "Creative Finance Architect",
            "description": "Structure deals that banks won't touch. From seller financing and lease options to subject-to acquisitions and wrap-around mortgages, Storm helps you create win-win scenarios that close more deals."
        },
        {
            "icon": "📊",
            "title": "Market Intelligence Hub",
            "description": "Stay ahead of the competition. Track auction schedules across multiple counties, identify emerging market trends, spot undervalued areas, and position yourself where the best opportunities exist."
        },
        {
            "icon": "🔍",
            "title": "Due Diligence Command Center",
            "description": "Never get burned by a bad deal. Property research frameworks, title examination checklists, lien priority analysis, and risk assessment tools to protect your investments."
        },
        {
            "icon": "💼",
            "title": "Portfolio Strategy Builder",
            "description": "Scale your real estate empire systematically. Get guidance on portfolio allocation, risk management, capital deployment, market timing, and long-term wealth building strategies."
        },
        {
            "icon": "📈",
            "title": "Financial Modeling Expert",
            "description": "Make data-driven investment decisions. Advanced ROI calculations, cash flow projections, sensitivity analysis, and scenario planning to maximize your returns and minimize risks."
        },
        {
            "icon": "🏆",
            "title": "Competitive Advantage Analysis",
            "description": "Outmaneuver other investors. Learn how to spot opportunities others miss, negotiate better deals, move faster, and build systems that give you an unfair advantage in any market."
        },
        {
            "icon": "🎓",
            "title": "Education & Training Hub",
            "description": "Continuously improve your skills. Access real-world case studies, best practices from top investors, common pitfalls to avoid, and strategies that work in any economic climate."
        }
    ]
    
    for feature in features:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-header">
                    <div class="feature-icon">{feature['icon']}</div>
                    <h3 class="feature-title">{feature['title']}</h3>
                </div>
                <p class="feature-description">{feature['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_example_prompts_tab():
    """Render example prompts in a grid layout."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h2 style="color: {PRIMARY_GREEN}; font-size: 2rem; font-weight: 800; margin: 0;">Example Questions</h2>
            </div>
            <p style="color: rgba(255,255,255,0.7);">Click any example to instantly start a conversation with Storm</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    examples = [
        {
            "icon": "📊",
            "title": "Tax Deed ROI Analysis",
            "query": "I'm looking at a tax deed property with a $50k opening bid. The estimated market value is $120k. It needs about $25k in repairs. Can you help me analyze if this is a good deal and calculate my potential ROI?"
        },
        {
            "icon": "🏦",
            "title": "Seller Financing Structure",
            "query": "I want to buy a property worth $200k but the seller wants all cash. How can I structure a creative financing deal with seller financing where I put minimal money down?"
        },
        {
            "icon": "📈",
            "title": "Wholesale Spread Calculator",
            "query": "I found a distressed property. The seller wants $80k, ARV is $150k, and repairs are estimated at $35k. What should my wholesale assignment fee be?"
        },
        {
            "icon": "💰",
            "title": "Tax Lien Investment Guide",
            "query": "I'm new to tax lien investing. Can you explain how tax liens work and what factors I should consider when choosing which liens to buy?"
        },
        {
            "icon": "🎯",
            "title": "Auction Bidding Strategy",
            "query": "I'm going to my first tax deed auction next week. What bidding strategies should I use, and how do I determine my maximum bid?"
        },
        {
            "icon": "🔍",
            "title": "Due Diligence Checklist",
            "query": "What due diligence should I perform before buying a tax deed property at auction?"
        },
        {
            "icon": "🏆",
            "title": "First Auction Preparation",
            "query": "I'm attending my first county tax deed auction. What's the best strategy for identifying which properties to bid on and how to determine my maximum bid?"
        },
        {
            "icon": "💼",
            "title": "Subject-To Deal Structure",
            "query": "I found a motivated seller with $150k remaining on their mortgage. The property is worth $220k. How do I structure a subject-to deal and what are the risks I need to be aware of?"
        },
        {
            "icon": "📉",
            "title": "Distressed Property Analysis",
            "query": "I found a property that's been vacant for 2 years with $45k in back taxes. The owner wants to walk away. How should I approach this deal?"
        },
        {
            "icon": "🎓",
            "title": "Portfolio Scaling Strategy",
            "query": "I've successfully flipped 3 properties. How do I scale to 10+ deals per year while managing risk and maintaining quality?"
        },
        {
            "icon": "🏛️",
            "title": "Lien Priority Assessment",
            "query": "I'm looking at a tax deed with multiple liens attached. How do I determine which liens survive the sale and calculate my true acquisition cost?"
        },
        {
            "icon": "💡",
            "title": "Creative Exit Strategies",
            "query": "I bought a tax deed property but the market has softened. What are alternative exit strategies beyond a traditional sale?"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, example in enumerate(examples):
        with col1 if idx % 2 == 0 else col2:
            if st.button(f"{example['icon']} {example['title']}", key=f"example_{idx}", use_container_width=True):
                st.session_state.example_query = example['query']
                st.rerun()

def render_export_tab():
    """Render the export and conversation management tab."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 3rem;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h2 style="color: {PRIMARY_GREEN}; font-size: 2rem; font-weight: 800; margin: 0;">Export & Manage</h2>
            </div>
            <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">Save your conversations, analyze insights, and manage your Storm sessions</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    stats = count_message_stats()
    
    # Statistics Overview
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%); border: 2px solid {PRIMARY_GREEN}33; border-radius: 25px; padding: 2rem; margin: 2rem 0;">
            <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">CURRENT SESSION STATISTICS</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1.5rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; font-weight: 900; color: {PRIMARY_GREEN};">{stats['total']}</div>
                    <div style="color: rgba(255,255,255,0.6); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.1em;">Total Messages</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; font-weight: 900; color: {SECONDARY_GREEN};">{stats['user']}</div>
                    <div style="color: rgba(255,255,255,0.6); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.1em;">Your Questions</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; font-weight: 900; color: {PRIMARY_GREEN};">{stats['assistant']}</div>
                    <div style="color: rgba(255,255,255,0.6); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.1em;">Storm Responses</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Export Options
    st.markdown(
        f"""
        <div style="margin: 3rem 0 2rem 0;">
            <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;">📥 Export Options</h3>
            <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Download your conversation in multiple formats for your records</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="background: {MID_BG}; border: 2px solid {PRIMARY_GREEN}22; border-radius: 20px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📄</div>
                <div style="color: {PRIMARY_GREEN}; font-weight: 700; margin-bottom: 0.5rem;">Plain Text</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Simple readable format</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Download TXT", key="export_txt", use_container_width=True):
            txt_content = export_conversation_text()
            st.download_button(
                label="💾 Save Text File",
                data=txt_content,
                file_name=f"storm_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        st.markdown(
            f"""
            <div style="background: {MID_BG}; border: 2px solid {PRIMARY_GREEN}22; border-radius: 20px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📝</div>
                <div style="color: {PRIMARY_GREEN}; font-weight: 700; margin-bottom: 0.5rem;">Markdown</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Formatted document</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Download MD", key="export_md", use_container_width=True):
            md_content = export_conversation_markdown()
            st.download_button(
                label="💾 Save Markdown File",
                data=md_content,
                file_name=f"storm_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: {MID_BG}; border: 2px solid {PRIMARY_GREEN}22; border-radius: 20px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🗂️</div>
                <div style="color: {PRIMARY_GREEN}; font-weight: 700; margin-bottom: 0.5rem;">JSON</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Structured data</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Download JSON", key="export_json", use_container_width=True):
            json_content = export_conversation_json()
            st.download_button(
                label="💾 Save JSON File",
                data=json_content,
                file_name=f"storm_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Conversation Preview
    if stats['total'] > 1:
        st.markdown(
            f"""
            <div style="margin: 3rem 0 2rem 0;">
                <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;">👁️ Conversation Preview</h3>
                <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Review your conversation before exporting</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.expander("📖 View Full Conversation", expanded=False):
            for idx, msg in enumerate(st.session_state.messages):
                role_label = "YOU" if msg["role"] == "user" else "STORM"
                role_color = SECONDARY_GREEN if msg["role"] == "user" else PRIMARY_GREEN
                
                st.markdown(
                    f"""
                    <div style="background: {MID_BG}; border-left: 4px solid {role_color}; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
                        <div style="color: {role_color}; font-weight: 800; font-size: 0.9rem; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;">{role_label} • Message {idx + 1}</div>
                        <div style="color: rgba(255,255,255,0.9); line-height: 1.7;">{msg['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Conversation Analysis
    st.markdown(
        f"""
        <div style="margin: 3rem 0 2rem 0;">
            <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;">📊 Conversation Analysis</h3>
            <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Insights about your discussion with Storm</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    render_conversation_topics()
    render_chat_insights()
    
    # Session Management
    st.markdown(
        f"""
        <div style="margin: 3rem 0 2rem 0;">
            <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;">⚙️ Session Management</h3>
            <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Control your Storm session</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Conversation", key="reset_export_tab", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "🐺 **Conversation Reset**\n\nReady to analyze your next deal. What are we working on?"
                }
            ]
            st.rerun()
    
    with col2:
        if st.button("🚀 New Session", key="new_session_export_tab", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Session Info
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    
    session_duration = datetime.now() - st.session_state.session_start_time
    minutes = int(session_duration.total_seconds() / 60)
    
    st.markdown(
        f"""
        <div style="background: {MID_BG}; border: 1px solid {PRIMARY_GREEN}22; border-radius: 15px; padding: 1.5rem; margin: 2rem 0; text-align: center;">
            <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Session Duration</div>
            <div style="color: {PRIMARY_GREEN}; font-size: 1.5rem; font-weight: 800;">{minutes} minutes</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# 7. MAIN APPLICATION ENGINE
# ======================================================

render_storm_header()
render_greeting_section()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🐺 **Ready to dominate real estate.**\n\n"
                       "I specialize in **tax deeds, tax liens, wholesale deals, and creative finance strategies**.\n\n"
                       "Whether you're analyzing auction properties, calculating ROI, structuring creative financing, or building your investment portfolio — "
                       "I'm here to help you execute with precision and confidence.\n\n"
                       "**What deal are we tackling today?**"
        }
    ]

if "example_query" not in st.session_state:
    st.session_state.example_query = None

if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = datetime.now()

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat with Storm", "📊 Export & Analytics", "📚 Features & Capabilities", "💡 Example Questions"])

with tab1:
    st.markdown(
        f"""
        <div style="margin: 2rem 0;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; letter-spacing: 0.1em; margin: 0;">CONVERSATION</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if len(st.session_state.messages) > 1:
        render_stats_dashboard()
        render_conversation_topics()
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if len(st.session_state.messages) > 5:
        render_chat_insights()
    
    # Handle example query injection
    if st.session_state.example_query:
        user_input = st.session_state.example_query
        st.session_state.example_query = None
    else:
        user_input = st.chat_input("Ask about auctions, liens, wholesale spreads, creative finance, ROI calculations, or market analysis…")
    
    # User Interaction & Webhook Logic
    if user_input:
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
    
        # Assistant Response
        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            status_placeholder.markdown("🐺 *Storm is analyzing your query and preparing a detailed response...*")
            
            # Prepare Payload for N8N
            payload = {
                "assistant": "Storm",
                "community": "Wolves of Real Estate",
                "message": user_input,
                "history": st.session_state.messages[-10:],
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "session_stats": count_message_stats()
            }
            
            try:
                # Execute Webhook Call
                response = requests.post(
                    N8N_WEBHOOK_URL, 
                    json=payload, 
                    timeout=90
                )
                
                if response.status_code == 200 and response.text:
                    final_reply = response.text.strip()
                elif response.status_code == 200:
                    final_reply = "⚠️ Storm received your question but encountered a processing issue. Please try rephrasing your query."
                else:
                    final_reply = f"⚠️ Storm encountered an issue (Status: {response.status_code}). Let's try that again."
                    
            except requests.exceptions.Timeout:
                final_reply = "⚠️ **Request timed out.** Storm is taking longer than expected. Please try again or simplify your question."
            except requests.exceptions.ConnectionError:
                final_reply = "⚠️ **Connection error:** Unable to reach Storm's server. Please check your internet connection and try again."
            except requests.exceptions.RequestException as e:
                final_reply = f"⚠️ **Network error:** {str(e)[:100]}. Please try again in a moment."
            
            # Update UI with response
            status_placeholder.markdown(final_reply)
            st.session_state.messages.append({"role": "assistant", "content": final_reply})
    
    # Control buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Conversation", key="reset_chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "🐺 **Conversation Reset**\n\nReady to analyze your next deal. What are we working on?"
                }
            ]
            st.rerun()
    
    with col2:
        if st.button("🚀 New Session", key="new_session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

with tab2:
    render_export_tab()

with tab3:
    render_expertise_section()
    
    st.markdown(
        f"""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h2 style="color: {PRIMARY_GREEN}; font-size: 2rem; font-weight: 800; letter-spacing: 0.05em;">CAPABILITIES</h2>
            <p style="color: rgba(255,255,255,0.7); margin-top: 1rem;">Everything you need to succeed in alternative real estate investing</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    render_feature_cards()

with tab4:
    render_example_prompts_tab()

# Footer
st.markdown(
    f"""
    <div style="margin-top: 5rem; padding: 4rem 1rem; text-align: center; border-top: 2px solid {PRIMARY_GREEN}11;">
        <div style="margin-bottom: 2rem;">
            <img src="{CHATBOT_ICON_DATA}" alt="Storm Chatbot" class="chatbot-icon">
        </div>
        <div style="color: {PRIMARY_GREEN}; font-weight: 900; letter-spacing: 0.3em; margin-bottom: 0.75rem; font-size: 1.2rem;">WOLVES OF REAL ESTATE</div>
        <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; letter-spacing: 0.1em; margin-bottom: 1.5rem;">© 2025 Built for Serious Operators</div>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1.5rem;">
            <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">🔒 Secure Connection</span>
            <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">⚡ Real-Time AI</span>
            <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">🐺 Pack Powered</span>
        </div>
        <div style="margin-top: 2rem; color: rgba(255,255,255,0.5); font-size: 0.75rem;">
            Powered by Storm AI Engine • Advanced Natural Language Processing
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
