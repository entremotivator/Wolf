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
        max-width: 900px !important;
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

    /* Added chatbot icon styles */
    .chatbot-icon {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid {PRIMARY_GREEN};
        box-shadow: 0 0 25px {PRIMARY_GREEN}44;
        display: inline-block;
        vertical-align: middle;
        margin-right: 1rem;
        transition: all 0.3s ease;
    }}

    .chatbot-icon:hover {{
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 0 40px {PRIMARY_GREEN}77;
    }}

    .chatbot-icon-small {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid {PRIMARY_GREEN};
        box-shadow: 0 0 15px {PRIMARY_GREEN}33;
        display: inline-block;
        vertical-align: middle;
        margin-right: 0.75rem;
    }}

    .greeting-section {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 2px solid {PRIMARY_GREEN}44;
        border-radius: 35px;
        padding: 2.5rem;
        margin: 2.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    .greeting-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, {PRIMARY_GREEN}08, transparent 70%);
        animation: rotate 20s linear infinite;
    }}

    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    .greeting-text {{
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1rem;
    }}

    .greeting-text h2 {{
        color: {PRIMARY_GREEN};
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 30px {PRIMARY_GREEN}66;
    }}

    /* STAT CARDS */
    .stat-card {{
        background: linear-gradient(135deg, {MID_BG} 0%, {DEEP_BG} 100%);
        border: 1px solid {PRIMARY_GREEN}33;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .stat-card:hover {{
        border-color: {PRIMARY_GREEN};
        box-shadow: 0 10px 30px {PRIMARY_GREEN}22;
        transform: translateY(-3px);
    }}

    .stat-number {{
        font-size: 2rem;
        font-weight: 800;
        color: {PRIMARY_GREEN};
        margin-bottom: 0.5rem;
    }}

    .stat-label {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}

    /* INFO SECTIONS */
    .info-section {{
        background: {MID_BG};
        border: 1px solid {PRIMARY_GREEN}22;
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }}

    .info-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, {PRIMARY_GREEN}, {SECONDARY_GREEN});
    }}

    .info-section h3 {{
        color: {PRIMARY_GREEN};
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .info-section p {{
        color: rgba(255,255,255,0.85);
        line-height: 1.8;
        margin-bottom: 1rem;
    }}

    .info-section ul {{
        list-style: none;
        padding: 0;
    }}

    .info-section li {{
        color: rgba(255,255,255,0.85);
        padding: 0.75rem 0;
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.6;
    }}

    .info-section li::before {{
        content: '▸';
        position: absolute;
        left: 0;
        color: {PRIMARY_GREEN};
        font-weight: bold;
    }}

    /* Enhanced feature cards with icons */
    .feature-card {{
        background: linear-gradient(135deg, {MID_BG}dd 0%, {DEEP_BG}dd 100%);
        border: 2px solid {PRIMARY_GREEN}22;
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}

    .feature-card:hover {{
        border-color: {PRIMARY_GREEN}66;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px {PRIMARY_GREEN}22;
    }}

    .feature-card::after {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, {PRIMARY_GREEN}11, transparent);
        border-radius: 0 0 0 100%;
    }}

    .feature-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }}

    .feature-icon {{
        font-size: 2.5rem;
        filter: drop-shadow(0 0 15px {PRIMARY_GREEN}44);
    }}

    .feature-title {{
        color: {PRIMARY_GREEN};
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
    }}

    .feature-description {{
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
        padding-left: 0.5rem;
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

    /* EXPANDABLE SECTIONS */
    .stExpander {{
        background: {MID_BG} !important;
        border: 1px solid {PRIMARY_GREEN}22 !important;
        border-radius: 20px !important;
        margin: 1rem 0 !important;
    }}

    .stExpander summary {{
        color: {PRIMARY_GREEN} !important;
        font-weight: 700 !important;
        padding: 1rem !important;
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

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}

    .pulse-animation {{
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
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

        .chatbot-icon {{
            width: 60px;
            height: 60px;
        }}

        .greeting-text h2 {{
            font-size: 1.8rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# 5. UTILITY FUNCTIONS
# ======================================================

def export_conversation_json() -> str:
    """Export conversation history as JSON string."""
    return json.dumps(st.session_state.messages, indent=2)

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

def get_conversation_summary() -> str:
    """Generate a summary of the conversation."""
    stats = count_message_stats()
    if stats["total"] <= 1:
        return "No conversation yet. Start by asking a question!"
    return f"**Conversation active:** {stats['user']} questions asked, {stats['assistant']} responses provided."

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

def render_expertise_section():
    """Render the expertise information section."""
    st.markdown(
        f"""
        <div class="info-section">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h3 style="margin: 0;">Storm's Expertise</h3>
            </div>
            <p>Storm is your specialized AI assistant for real estate investment strategies that serious operators use to dominate the market. Here's what Storm can help you with:</p>
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
            "description": "Never get burned by a bad deal. Comprehensive property research frameworks, title examination checklists, lien priority analysis, and risk assessment tools to protect your investments."
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

def render_quick_examples():
    """Render quick example prompts section."""
    st.markdown(
        f"""
        <div class="info-section">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
                <h3 style="margin: 0;">Quick Start Examples</h3>
            </div>
            <p>Not sure where to begin? Try asking Storm about these common scenarios:</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Analyze Tax Deed ROI", key="example1"):
            st.session_state.example_query = "I'm looking at a tax deed property with a $50k opening bid. The estimated market value is $120k. It needs about $25k in repairs. Can you help me analyze if this is a good deal and calculate my potential ROI?"
        
        if st.button("🏦 Structure Seller Financing", key="example2"):
            st.session_state.example_query = "I want to buy a property worth $200k but the seller wants all cash. How can I structure a creative financing deal with seller financing where I put minimal money down?"
        
        if st.button("📈 Calculate Wholesale Spread", key="example3"):
            st.session_state.example_query = "I found a distressed property. The seller wants $80k, ARV is $150k, and repairs are estimated at $35k. What should my wholesale assignment fee be?"
    
        if st.button("🎯 County Auction Strategy", key="example7"):
            st.session_state.example_query = "I'm attending my first county tax deed auction. What's the best strategy for identifying which properties to bid on and how to determine my maximum bid?"
    
    with col2:
        if st.button("💰 Tax Lien Strategy", key="example4"):
            st.session_state.example_query = "I'm new to tax lien investing. Can you explain how tax liens work and what factors I should consider when choosing which liens to buy?"
        
        if st.button("🎯 Auction Bidding Strategy", key="example5"):
            st.session_state.example_query = "I'm going to my first tax deed auction next week. What bidding strategies should I use, and how do I determine my maximum bid?"
        
        if st.button("🔍 Due Diligence Checklist", key="example6"):
            st.session_state.example_query = "What due diligence should I perform before buying a tax deed property at auction?"

        if st.button("💼 Subject-To Deal Structure", key="example8"):
            st.session_state.example_query = "I found a motivated seller with $150k remaining on their mortgage. The property is worth $220k. How do I structure a subject-to deal and what are the risks I need to be aware of?"

def render_stats_dashboard():
    """Render conversation statistics dashboard."""
    stats = count_message_stats()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{stats['user']}</div>
                <div class="stat-label">Questions Asked</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{stats['assistant']}</div>
                <div class="stat-label">Storm Responses</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_advanced_features():
    """Render advanced features section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.expander("⚙️ ADVANCED FEATURES & SETTINGS", expanded=False):
        st.markdown(f"<p style='color: {PRIMARY_GREEN}; font-weight: 600; margin-bottom: 1rem;'>Conversation Management</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Conversation", key="export_btn", use_container_width=True):
                conversation_json = export_conversation_json()
                st.download_button(
                    label="⬇️ Download JSON",
                    data=conversation_json,
                    file_name=f"storm_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_json"
                )
                st.success("✅ Conversation ready for download!")
        
        with col2:
            if st.button("📋 Copy Last Response", key="copy_btn", use_container_width=True):
                if st.session_state.messages:
                    last_assistant_msg = [msg for msg in reversed(st.session_state.messages) if msg["role"] == "assistant"]
                    if last_assistant_msg:
                        st.code(last_assistant_msg[0]["content"], language=None)
                        st.info("💡 Select and copy the text above")
                else:
                    st.warning("No messages to copy yet")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {PRIMARY_GREEN}; font-weight: 600; margin-bottom: 1rem;'>Conversation Summary</p>", unsafe_allow_html=True)
        summary = get_conversation_summary()
        st.markdown(summary)
        
        stats = count_message_stats()
        if stats["total"] > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: rgba(255,255,255,0.7); font-size: 0.85rem;'>Session started: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>", unsafe_allow_html=True)

def render_storm_footer():
    """Render footer with chatbot icon."""
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

# ======================================================
# 7. MAIN APPLICATION ENGINE
# ======================================================

render_storm_header()

render_greeting_section()

# Session State Management
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

if "show_stats" not in st.session_state:
    st.session_state.show_stats = False

if "example_query" not in st.session_state:
    st.session_state.example_query = None

# Render Expertise and Examples sections
render_expertise_section()

st.markdown(
    f"""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: {PRIMARY_GREEN}; font-size: 2rem; font-weight: 800; letter-spacing: 0.05em;">COMPREHENSIVE CAPABILITIES</h2>
        <p style="color: rgba(255,255,255,0.7); margin-top: 1rem;">Everything you need to succeed in alternative real estate investing</p>
    </div>
    """,
    unsafe_allow_html=True
)
render_feature_cards()

render_quick_examples()

# Statistics Dashboard Toggle
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 SHOW CONVERSATION STATS", key="toggle_stats"):
    st.session_state.show_stats = not st.session_state.show_stats

if st.session_state.show_stats:
    render_stats_dashboard()

# Display Chat History
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="border-top: 2px solid {PRIMARY_GREEN}22; padding-top: 2rem; margin-top: 2rem;">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
            <img src="{CHATBOT_ICON_DATA}" alt="Storm" class="chatbot-icon-small">
            <h3 style="color: {PRIMARY_GREEN}; font-weight: 800; letter-spacing: 0.1em; margin: 0;">CONVERSATION</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


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

    # Professional Assistant Response
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
            # Execute Webhook Call with proper timeout
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
            final_reply = "⚠️ **Request timed out.** Storm is taking longer than expected—likely processing a complex query. Please try again or simplify your question."
        except requests.exceptions.ConnectionError:
            final_reply = "⚠️ **Connection error:** Unable to reach Storm's server. Please check your internet connection and try again."
        except requests.exceptions.RequestException as e:
            final_reply = f"⚠️ **Network error:** {str(e)[:100]}. Please try again in a moment."
        
        # Update UI with response
        status_placeholder.markdown(final_reply)
        st.session_state.messages.append({"role": "assistant", "content": final_reply})

# Advanced Features
render_advanced_features()

# Reset & Control Buttons Section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="border-top: 2px solid {PRIMARY_GREEN}11; padding-top: 2rem; margin-top: 3rem;">
        <h3 style="color: {PRIMARY_GREEN}; text-align: center; font-weight: 800; letter-spacing: 0.1em; margin-bottom: 1.5rem;">🎛️ CONTROLS</h3>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 RESET CONVERSATION", key="reset_main", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🐺 **Conversation Reset**\n\nReady to analyze your next deal. What are we working on?"
            }
        ]
        st.session_state.show_stats = False
        st.rerun()

with col2:
    if st.button("🚀 NEW SESSION", key="new_session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

render_storm_footer()
