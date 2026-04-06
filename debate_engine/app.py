"""
AI Hedge Fund War Room UI
Premium neon-themed financial debate dashboard with glassmorphism design.
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import io
from typing import List, Dict
import random

# Load environment variables
load_dotenv()

from engines.market_data_engine import fetch_market_data
from engines.debate_engine import multi_round_debate

try:
    from services.llm_service import call_llm as call_llm_for_explain
except Exception:
    call_llm_for_explain = None

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ============================================================================
# PAGE CONFIG & NEON WAR ROOM STYLING
# ============================================================================

st.set_page_config(
    layout="wide",
    page_title="AI Hedge Fund War Room",
    initial_sidebar_state="collapsed"
)

# Modern glassmorphic design with neon accents
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --background: #0f172a;
        --foreground: #e8f2ff;
        --card: #1a2544;
        --secondary: #2d3b5c;
        --muted: #1a2750;
        --muted-foreground: #8b93a1;
        --neon-green: #22c55e;
        --neon-red: #ff3333;
        --neon-yellow: #facc15;
        --neon-blue: #3b82f6;
        --neon-purple: #a855f7;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 50%, #0d1628 100%);
        color: var(--foreground);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Glassmorphism base */
    .glass-card {
        background: rgba(26, 37, 68, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
    }

    /* Main container */
    .main {
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 24px !important;
    }

    /* Neon glows */
    .neon-glow-green {
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
    }

    .neon-glow-red {
        box-shadow: 0 0 20px rgba(255, 51, 51, 0.3);
    }

    .neon-glow-blue {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* Headings */
    h1, h2, h3 {
        color: var(--foreground);
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 { font-size: 24px; }
    h2 { font-size: 18px; }
    h3 { font-size: 14px; }

    /* Live indicator */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1px;
        color: var(--neon-green);
        font-family: 'JetBrains Mono', monospace;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        background: var(--neon-green);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* Agent messages */
    .agent-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 3px solid;
        margin: 8px 0;
        line-height: 1.5;
        animation: slideUp 0.4s ease-out;
    }

    .agent-bubble.aggressive {
        background: rgba(255, 51, 51, 0.12);
        border-left-color: var(--neon-red);
        color: #ff9999;
    }

    .agent-bubble.balanced {
        background: rgba(59, 130, 246, 0.12);
        border-left-color: var(--neon-blue);
        color: #93c5ff;
    }

    .agent-bubble.safe {
        background: rgba(34, 197, 94, 0.12);
        border-left-color: var(--neon-green);
        color: #86efac;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Agent header */
    .agent-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        padding: 6px 10px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 12px;
        font-weight: 600;
    }

    .agent-header.speaking {
        background: rgba(34, 197, 94, 0.08);
        border-color: rgba(34, 197, 94, 0.3);
    }

    .agent-avatar {
        font-size: 18px;
    }

    .agent-status {
        font-size: 10px;
        color: var(--muted-foreground);
    }

    .agent-status.speaking {
        color: var(--neon-green);
        font-weight: 600;
    }

    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }

    .metric-label {
        font-size: 10px;
        color: var(--muted-foreground);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 18px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--foreground);
    }

    /* Verdict boxes */
    .verdict-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid;
        border-radius: 8px;
        padding: 12px;
        margin: 6px 0;
        font-size: 13px;
    }

    .verdict-box.buy { border-left-color: var(--neon-green); }
    .verdict-box.hold { border-left-color: var(--neon-yellow); }
    .verdict-box.avoid { border-left-color: var(--neon-red); }

    /* Typing indicator */
    .typing-indicator {
        display: inline-flex;
        gap: 3px;
        align-items: center;
    }

    .typing-dot {
        width: 4px;
        height: 4px;
        border-radius: 50%;
        animation: typingBounce 1.4s ease-in-out infinite;
    }

    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
        30% { opacity: 1; transform: translateY(-4px); }
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--neon-green) 0%, #16a34a 100%);
        border: none;
        color: #0f172a;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
    }

    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
    }

    /* Checkbox */
    .stCheckbox {
        color: var(--foreground);
    }

    .stCheckbox label {
        font-size: 13px;
        font-weight: 500;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 16px 0;
    }

    /* Colors */
    .text-green { color: var(--neon-green) !important; }
    .text-red { color: var(--neon-red) !important; }
    .text-yellow { color: var(--neon-yellow) !important; }
    .text-blue { color: var(--neon-blue) !important; }
    .text-muted { color: var(--muted-foreground) !important; }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def speak(text: str, agent: str = "Balanced") -> bytes:
    """Convert text to speech with agent-specific tone."""
    if not TTS_AVAILABLE:
        raise RuntimeError("gTTS not installed")
    mp3_io = io.BytesIO()
    tts = gTTS(text, lang="en", slow=False)
    tts.write_to_fp(mp3_io)
    mp3_io.seek(0)
    return mp3_io.read()


def get_agent_tone_text(text: str, agent: str) -> str:
    """Adjust text pacing based on agent personality."""
    if agent == "Aggressive":
        text = text.replace(".", "!\n").replace("?", "?!\n")
    elif agent == "Safe":
        text = text.replace(".", "...\n").replace(",", "....\n")
    return text


def escape_html(s: str) -> str:
    """Escape HTML characters."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))


def risk_level(volatility: float) -> tuple:
    """Classify risk based on volatility."""
    if volatility < 0.2:
        return "LOW", "neon-green"
    elif volatility < 0.5:
        return "MODERATE", "neon-yellow"
    else:
        return "HIGH", "neon-red"


def compute_final_verdict(convo: List[Dict]) -> tuple:
    """Count BUY/HOLD/AVOID votes and determine majority."""
    votes = {"BUY": 0, "HOLD": 0, "AVOID": 0}
    final_msgs = [m for m in convo if m.get("round", "").lower() == "final verdict"]
    
    for msg in final_msgs:
        text = (msg.get("text", "") or "").upper()
        if "BUY" in text:
            votes["BUY"] += 1
        elif "AVOID" in text or "SELL" in text:
            votes["AVOID"] += 1
        elif "HOLD" in text:
            votes["HOLD"] += 1

    if votes["BUY"] > votes["HOLD"] and votes["BUY"] > votes["AVOID"]:
        majority = "BUY"
    elif votes["AVOID"] > votes["HOLD"] and votes["AVOID"] > votes["BUY"]:
        majority = "AVOID"
    elif votes["HOLD"] > votes["BUY"] and votes["HOLD"] > votes["AVOID"]:
        majority = "HOLD"
    else:
        majority = "TIE"

    return votes, majority


def get_agent_avatar(agent: str) -> str:
    """Return emoji avatar for agent."""
    avatars = {"Aggressive": "🔥", "Balanced": "📊", "Safe": "🛡"}
    return avatars.get(agent.split()[0], "🤖")


def render_agent_header_html(agent: str, is_speaking: bool = False) -> str:
    """Render agent header with HTML."""
    avatar = get_agent_avatar(agent)
    speaking_class = "speaking" if is_speaking else ""
    status = "● SPEAKING" if is_speaking else "WAITING"
    status_color = "text-green" if is_speaking else ""
    
    return f"""
    <div class="agent-header {speaking_class}">
        <span class="agent-avatar">{avatar}</span>
        <div style="flex: 1;">
            <div style="font-size: 12px; font-weight: 600;">{agent}</div>
            <div class="agent-status {status_color}" style="font-size: 10px;">{status}</div>
        </div>
    </div>
    """


def render_chat_bubble_html(text: str, agent_type: str) -> str:
    """Render a chat message bubble."""
    if len(text) > 400:
        text = text[:390].rsplit(" ", 1)[0] + "…"
    
    escaped = escape_html(text)
    agent_class = agent_type.lower() if agent_type.lower() in ["aggressive", "balanced", "safe"] else "balanced"
    
    return f'<div class="agent-bubble {agent_class}">{escaped}</div>'


# ============================================================================
# MAIN APP
# ============================================================================

st.markdown('<div style="padding: 0;">', unsafe_allow_html=True)

# Title bar
col_title, col_status = st.columns([1, 0.3])
with col_title:
    st.markdown("<h1>🏛️ AI Hedge Fund War Room</h1>", unsafe_allow_html=True)
with col_status:
    st.markdown(
        '<div class="live-indicator"><span class="live-dot"></span>LIVE</div>',
        unsafe_allow_html=True
    )

st.divider()

# Input controls
col_co, col_ti, col_btn, col_audio = st.columns([2, 1.5, 1.5, 1.5])

with col_co:
    company = st.text_input("Company", placeholder="e.g., Apple", key="company_input")

with col_ti:
    ticker = st.text_input("Ticker", placeholder="e.g., AAPL", key="ticker_input")

with col_btn:
    start_debate = st.button("🚀 START DEBATE", key="start_btn", use_container_width=True)

with col_audio:
    auto_play_audio = st.checkbox(
        "🔊 Voice",
        value=False,
        disabled=(not TTS_AVAILABLE),
        key="voice_toggle"
    )

st.divider()

# Only proceed if ticker & company are provided
if ticker and company:
    try:
        market_data = fetch_market_data(ticker)
    except Exception as e:
        st.error(f"Failed to fetch market data: {e}")
        st.stop()

    institutional_data = {
        "weighted_rating": 0.82,
        "consensus_strength": 0.76,
        "disagreement": 0.31
    }

    # Market snapshot metrics
    st.markdown("### 📊 Market Snapshot")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Price</div><div class="metric-value">${market_data["current_price"]:,.0f}</div></div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">P/E</div><div class="metric-value">{market_data["pe_ratio"]:.2f}x</div></div>',
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Volatility</div><div class="metric-value">{market_data["volatility"]:.2f}</div></div>',
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">1Y Return</div><div class="metric-value">{market_data["one_year_return"]*100:.1f}%</div></div>',
            unsafe_allow_html=True
        )

    st.divider()

    if start_debate:
        st.session_state.debate_started = True
        st.session_state.convo = []
        st.session_state.visible_msgs = []

    # Run debate if started
    if st.session_state.get("debate_started", False):
        with st.spinner("🤖 Agents debating..."):
            if not st.session_state.get("convo"):
                try:
                    st.session_state.convo = multi_round_debate(company, market_data, institutional_data)
                except Exception as e:
                    st.error(f"Debate error: {e}")
                    st.stop()

        # DEBATE ROOM
        st.markdown("<h2>💬 Live Debate Room</h2>", unsafe_allow_html=True)
        
        # Initialize tracking
        if "visible_msgs" not in st.session_state:
            st.session_state.visible_msgs = []
        if "last_shown_round" not in st.session_state:
            st.session_state.last_shown_round = None

        convo = st.session_state.convo

        # Display messages with animation
        for msg_idx, msg in enumerate(convo):
            agent = msg.get("agent", "Agent")
            round_name = msg.get("round", "Opening")
            text = msg.get("text", "").strip() or "[No response]"

            # Agent type for styling
            agent_type = agent.split()[0]  # "Aggressive", "Balanced", "Safe"

            st.markdown(render_agent_header_html(agent, True), unsafe_allow_html=True)
            st.markdown(render_chat_bubble_html(text, agent_type), unsafe_allow_html=True)

            # Optional audio
            if auto_play_audio and TTS_AVAILABLE:
                try:
                    tone_text = get_agent_tone_text(text, agent)
                    mp3_bytes = speak(tone_text, agent=agent)
                    st.audio(mp3_bytes, format="audio/mp3")
                except Exception:
                    pass

            time.sleep(0.3)

        # Analysis section
        st.divider()
        st.markdown("<h2>📈 Analysis & Verdict</h2>", unsafe_allow_html=True)

        col_risk, col_verdict, col_explain = st.columns([1, 1.2, 2])

        with col_risk:
            st.markdown("#### 🛡️ Risk Assessment")
            vol = market_data.get("volatility", 0.0)
            risk_name, risk_color = risk_level(vol)
            st.markdown(
                f'<div class="verdict-box"><span class="text-{risk_color}">Risk: {risk_name}</span><br/>Volatility: {vol:.3f}</div>',
                unsafe_allow_html=True
            )

        with col_verdict:
            st.markdown("#### 🏆 Final Verdict")
            votes, majority = compute_final_verdict(convo)
            st.markdown(f"**BUY:** {votes['BUY']} | **HOLD:** {votes['HOLD']} | **AVOID:** {votes['AVOID']}")
            
            if majority == "BUY":
                verdict_color = "text-green"
                verdict_icon = "✅"
            elif majority == "AVOID":
                verdict_color = "text-red"
                verdict_icon = "❌"
            elif majority == "HOLD":
                verdict_color = "text-yellow"
                verdict_icon = "⏸️"
            else:
                verdict_color = "text-muted"
                verdict_icon = "🤝"

            st.markdown(
                f'<div class="verdict-box {majority.lower()}"><strong class="{verdict_color}">{verdict_icon} {majority}</strong></div>',
                unsafe_allow_html=True
            )

        with col_explain:
            st.markdown("#### 📚 Simple Explanation")
            if call_llm_for_explain:
                try:
                    recent_msgs = convo[-6:] if len(convo) >= 6 else convo
                    msg_summary = "\n".join([
                        f"{m.get('agent', 'Agent')}: {m.get('text', '')[:100]}"
                        for m in recent_msgs
                    ])

                    response = call_llm_for_explain(
                        messages=[
                            {
                                "role": "system",
                                "content": "Explain this debate in 3 simple sentences for beginners."
                            },
                            {
                                "role": "user",
                                "content": f"Debate about {company}:\n{msg_summary}"
                            }
                        ],
                        temperature=0.2,
                        max_output_tokens=150
                    )
                    st.info(response)
                except Exception as e:
                    st.warning(f"Explanation unavailable: {str(e)[:60]}")
            else:
                st.warning("LLM service unavailable")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    "<div style='text-align: center; margin-top: 32px; font-size: 11px; color: #8b93a1;'>"
    "AI Hedge Fund War Room • Powered by Groq • Multi-Agent Debate"
    "</div>",
    unsafe_allow_html=True
)
