"""
AI Hedge Fund War Room UI
A premium, dark-themed Streamlit dashboard for live AI debate on investment decisions.
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import io
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()
from engines.market_data_engine import fetch_market_data
from engines.debate_engine import multi_round_debate
from utils.explanations import reliability_explanation

# Optional LLM explain function
try:
    from services.llm_service import call_llm as call_llm_for_explain
except Exception:
    call_llm_for_explain = None

# Text-to-speech support
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ============================================================================
# PAGE CONFIG & DARK THEME STYLING
# ============================================================================

st.set_page_config(
    layout="wide",
    page_title="AI Hedge Fund War Room",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS with rounded chat bubbles and financial dashboard feel
st.markdown(
    """
    <style>
    /* Color palette */
    :root {
        --bg-dark: #0b1221;
        --panel-dark: #0f1724;
        --text-light: #e6eef7;
        --text-muted: #9aa4b2;
        --accent-green: #16a34a;
        --accent-yellow: #f59e0b;
        --accent-red: #ef4444;
        --bubble-bg: #12202b;
    }

    body {
        background-color: var(--bg-dark);
        color: var(--text-light);
    }

    .warroom-container {
        background-color: var(--bg-dark);
        color: var(--text-light);
        padding: 20px;
        border-radius: 12px;
    }

    .agent-column {
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
        border-radius: 12px;
        padding: 12px;
        min-height: 450px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .agent-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        padding: 8px;
        border-radius: 8px;
    }

    .agent-header.active {
        background: rgba(22, 163, 74, 0.1);
        border: 1px solid rgba(22, 163, 74, 0.3);
        box-shadow: 0 0 16px rgba(22, 163, 74, 0.12);
    }

    .agent-avatar {
        font-size: 28px;
        line-height: 1;
    }

    .agent-name {
        font-weight: 600;
        color: var(--text-light);
        margin: 0;
        padding: 0;
    }

    .agent-status {
        font-size: 12px;
        color: var(--text-muted);
        margin: 0;
        padding: 0;
    }

    .agent-status.speaking {
        color: var(--accent-green);
        font-weight: 700;
    }

    .chat-bubble {
        padding: 12px 14px;
        border-radius: 12px;
        margin: 8px 0;
        line-height: 1.4;
        background: var(--bubble-bg);
        color: #d9e8ff;
        border-left: 3px solid var(--accent-green);
        font-size: 14px;
    }

    .round-divider {
        text-align: center;
        color: var(--text-muted);
        font-size: 12px;
        margin: 16px 0 12px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 16px 0;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 8px;
        padding: 12px;
        border: 1px solid rgba(255,255,255,0.05);
        text-align: center;
    }

    .metric-label {
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-light);
    }

    .typing-indicator {
        color: var(--text-muted);
        font-size: 13px;
        font-style: italic;
    }

    .verdict-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 8px;
        padding: 14px;
        border-left: 4px solid var(--accent-green);
        margin: 8px 0;
    }

    .verdict-box.buy {
        border-left-color: var(--accent-green);
    }

    .verdict-box.hold {
        border-left-color: var(--accent-yellow);
    }

    .verdict-box.avoid {
        border-left-color: var(--accent-red);
    }

    .risk-low { color: var(--accent-green); font-weight: 700; }
    .risk-medium { color: var(--accent-yellow); font-weight: 700; }
    .risk-high { color: var(--accent-red); font-weight: 700; }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def speak(text: str, agent: str = "Balanced") -> bytes:
    """
    Convert text to speech using gTTS with agent-specific tone.
    - Aggressive: Faster, energetic tempo
    - Balanced: Normal tempo, calm tone
    - Safe: Slower, cautious deliberation
    Returns mp3 bytes or raises on error.
    """
    if not TTS_AVAILABLE:
        raise RuntimeError("gTTS not installed. Run: pip install gTTS")
    
    # Set tempo/speed based on agent personality
    # Note: gTTS doesn't support direct speed control, but we can use TLD variants
    # and optimize the text for natural pacing
    
    mp3_io = io.BytesIO()
    
    # Use slow=False for all agents to keep it snappy (gTTS slow=True is very slow)
    tts = gTTS(text, lang="en", slow=False)
    
    tts.write_to_fp(mp3_io)
    mp3_io.seek(0)
    return mp3_io.read()


def get_agent_tone_text(text: str, agent: str) -> str:
    """
    Adjust text pacing for audio based on agent personality.
    This helps create natural tone variation even with same TTS engine.
    """
    # Add punctuation and emphasis cues for natural reading
    if agent == "Aggressive":
        # More exclamatory, direct statements
        text = text.replace(".", "!\n")
        text = text.replace("?", "?!\n")
    elif agent == "Safe":
        # Add pauses with ellipsis for deliberate, cautious tone
        text = text.replace(".", "...\n")
        text = text.replace(",", "....\n")
    # Balanced: keep as-is
    
    return text


def escape_html(s: str) -> str:
    """Escape special characters for safe HTML rendering."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))


def risk_level(volatility: float) -> tuple:
    """
    Classify risk based on volatility.
    Returns (level_name, css_class).
    """
    if volatility < 0.2:
        return "Low", "risk-low"
    elif volatility < 0.5:
        return "Medium", "risk-medium"
    else:
        return "High", "risk-high"


def compute_final_verdict(convo: List[Dict]) -> tuple:
    """
    Count BUY/HOLD/AVOID votes from final-round messages.
    Returns (votes_dict, majority_decision).
    """
    votes = {"BUY": 0, "HOLD": 0, "AVOID": 0}
    
    # Extract final-round messages
    final_msgs = [m for m in convo if m.get("round", "").lower() == "final verdict"]
    
    for msg in final_msgs:
        text = (msg.get("text", "") or "").upper()
        if "BUY" in text:
            votes["BUY"] += 1
        elif "AVOID" in text or "SELL" in text:
            votes["AVOID"] += 1
        elif "HOLD" in text:
            votes["HOLD"] += 1

    # Determine majority
    if votes["BUY"] > votes["HOLD"] and votes["BUY"] > votes["AVOID"]:
        majority = "BUY"
    elif votes["AVOID"] > votes["HOLD"] and votes["AVOID"] > votes["BUY"]:
        majority = "AVOID"
    elif votes["HOLD"] > votes["BUY"] and votes["HOLD"] > votes["AVOID"]:
        majority = "HOLD"
    elif votes["BUY"] == votes["HOLD"] == votes["AVOID"] == 0:
        majority = "NO VOTES"
    else:
        majority = "TIE"

    return votes, majority


def get_agent_avatar(agent: str) -> str:
    """Return emoji avatar for agent."""
    avatars = {
        "Aggressive": "🔥",
        "Balanced": "📊",
        "Safe": "🛡"
    }
    return avatars.get(agent.split()[0], "🤖")


def render_agent_header(agent: str, is_speaking: bool = False) -> str:
    """Render agent header with avatar, name, and status."""
    avatar = get_agent_avatar(agent)
    active_class = "active" if is_speaking else ""
    status_text = "● Speaking now..." if is_speaking else "Waiting..."
    status_class = "speaking" if is_speaking else ""
    
    html = f"""
    <div class="agent-header {active_class}">
        <div class="agent-avatar">{avatar}</div>
        <div>
            <div class="agent-name">{agent}</div>
            <div class="agent-status {status_class}">{status_text}</div>
        </div>
    </div>
    """
    return html


def render_chat_bubble(text: str) -> str:
    """Render a chat message bubble."""
    # Truncate if excessively long (UI limit)
    if len(text) > 400:
        text = text[:390].rsplit(" ", 1)[0] + "…"
    
    escaped = escape_html(text)
    html = f'<div class="chat-bubble">{escaped}</div>'
    return html


def render_round_divider(round_name: str) -> str:
    """Render a round section divider."""
    icons = {
        "Opening": "🎯",
        "Rebuttal": "⚔️",
        "Final Verdict": "🏆"
    }
    icon = icons.get(round_name, "📍")
    html = f'<div class="round-divider">{icon} {round_name} Round</div>'
    return html


# ============================================================================
# MAIN DEBATE RENDERER
# ============================================================================

def render_debate_ui(convo: List[Dict], auto_play_audio: bool = False):
    """
    Render the live debate sequentially across three agent columns.
    convo: list of dicts with keys: agent, round, text
    """
    # Initialize session state for message tracking
    if "warroom_messages" not in st.session_state:
        st.session_state.warroom_messages = {
            "Aggressive": [],
            "Balanced": [],
            "Safe": []
        }
    if "last_shown_round" not in st.session_state:
        st.session_state.last_shown_round = None

    # Create three columns for agents
    col_agg, col_bal, col_safe = st.columns([1, 1, 1], gap="large")

    agent_cols = {
        "Aggressive": col_agg,
        "Balanced": col_bal,
        "Safe": col_safe
    }

    # Pre-create containers for each agent's column
    col_containers = {}
    for agent, col in agent_cols.items():
        with col:
            col_containers[agent] = {
                "header": st.empty(),
                "body": st.container()
            }

    # Render headers (initially inactive)
    for agent in ["Aggressive", "Balanced", "Safe"]:
        col_containers[agent]["header"].markdown(
            render_agent_header(agent, is_speaking=False),
            unsafe_allow_html=True
        )

    # Sequentially process and display messages
    for msg_idx, msg in enumerate(convo):
        agent = msg.get("agent", "Agent")
        round_name = msg.get("round", "Opening")
        text = msg.get("text", "").strip() or "[No response]"

        # Show round divider on first message of each round
        if st.session_state.last_shown_round != round_name:
            for col_cont in col_containers.values():
                col_cont["body"].markdown(
                    render_round_divider(round_name),
                    unsafe_allow_html=True
                )
            st.session_state.last_shown_round = round_name
            time.sleep(0.4)

        # Highlight the speaking agent
        for a in ["Aggressive", "Balanced", "Safe"]:
            is_active = (a == agent)
            col_containers[a]["header"].markdown(
                render_agent_header(a, is_speaking=is_active),
                unsafe_allow_html=True
            )

        # Typing indicator
        typing_slot = col_containers[agent]["body"].empty()
        typing_slot.markdown(
            '<div class="typing-indicator">✎ typing...</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.5)

        # Add message to session state
        st.session_state.warroom_messages[agent].append({
            "text": text,
            "round": round_name
        })

        # Re-render all agent columns with accumulated messages
        for agent_name, col_cont in col_containers.items():
            msgs = st.session_state.warroom_messages.get(agent_name, [])
            body_html = ""
            for m in msgs:
                body_html += render_chat_bubble(m["text"])
            col_cont["body"].markdown(body_html, unsafe_allow_html=True)

        # Optional: play audio with agent-specific tone
        if auto_play_audio and TTS_AVAILABLE:
            try:
                # Adjust text tone based on agent personality
                tone_adjusted_text = get_agent_tone_text(text, agent)
                mp3_bytes = speak(tone_adjusted_text, agent=agent)
                st.audio(mp3_bytes, format="audio/mp3")
            except Exception:
                pass

        time.sleep(0.3)

    # Clear speaking indicators
    for agent in ["Aggressive", "Balanced", "Safe"]:
        col_containers[agent]["header"].markdown(
            render_agent_header(agent, is_speaking=False),
            unsafe_allow_html=True
        )


# ============================================================================
# MAIN APP LAYOUT
# ============================================================================

st.markdown('<div class="warroom-container">', unsafe_allow_html=True)

# Title & instructions
st.markdown(
    "<h1 style='color:#e6eef7;margin-bottom:8px'>🏛 AI Hedge Fund War Room</h1>",
    unsafe_allow_html=True
)
st.write(
    "Enter a company and ticker to watch three AI analyst personas debate the investment case in real-time."
)

# Input controls
col_co, col_ti, col_btn = st.columns([2, 2, 1.5], gap="small")

with col_co:
    company = st.text_input("Company Name", placeholder="e.g., Apple", key="company_input")

with col_ti:
    ticker = st.text_input("Ticker", placeholder="e.g., AAPL", key="ticker_input")

with col_btn:
    st.write("")  # spacer for alignment
    start_debate = st.button("🚀 Start War Room", key="start_btn", use_container_width=True)

# Audio toggle
col_audio, col_space = st.columns([2, 5])
with col_audio:
    auto_play_audio = st.checkbox(
        "🔊 Auto-play audio",
        value=False,
        disabled=(not TTS_AVAILABLE),
        help="Enable text-to-speech for each agent message" if TTS_AVAILABLE else "gTTS not installed"
    )

st.divider()

# Only proceed if ticker & company are provided
if ticker and company:
    # Fetch market data
    try:
        market_data = fetch_market_data(ticker)
    except Exception as e:
        st.error(f"Failed to fetch market data for {ticker}: {e}")
        st.stop()

    # Hardcoded institutional data (you can replace with API call if available)
    institutional_data = {
        "weighted_rating": 0.82,
        "consensus_strength": 0.76,
        "disagreement": 0.31
    }

    # Display market metrics
    st.markdown("### 📊 Market Snapshot")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Price</div>'
            f'<div class="metric-value">${market_data["current_price"]:,.0f}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">PE Ratio</div>'
            f'<div class="metric-value">{market_data["pe_ratio"]:.2f}x</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Volatility</div>'
            f'<div class="metric-value">{market_data["volatility"]:.2f}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">1Y Return</div>'
            f'<div class="metric-value">{market_data["one_year_return"]*100:.1f}%</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # When user clicks "Start War Room"
    if start_debate:
        # Reset session state for fresh debate
        st.session_state.warroom_messages = {
            "Aggressive": [],
            "Balanced": [],
            "Safe": []
        }
        st.session_state.last_shown_round = None

        # Run the debate
        with st.spinner("🤖 Agents are debating... this may take 30-60 seconds"):
            try:
                convo = multi_round_debate(company, market_data, institutional_data)
            except Exception as e:
                st.error(f"Debate failed: {e}")
                st.stop()

        # LIVE DEBATE ROOM (core feature)
        st.markdown("---")
        st.markdown("<h2 style='color:#e6eef7'>💬 LIVE Debate Room</h2>", unsafe_allow_html=True)
        render_debate_ui(convo, auto_play_audio=auto_play_audio)

        # Bottom section: Risk Monitor | Final Verdict | Explanation
        st.markdown("---")
        st.markdown("<h2 style='color:#e6eef7'>📈 Analysis & Verdict</h2>", unsafe_allow_html=True)

        bottom_col1, bottom_col2, bottom_col3 = st.columns([1, 1.2, 2], gap="large")

        # Risk Monitor
        with bottom_col1:
            st.markdown("#### 🛡 Risk Monitor")
            vol = market_data.get("volatility", 0.0)
            risk_name, risk_css = risk_level(vol)
            st.markdown(
                f'<div class="verdict-box"><span class="{risk_css}">Risk: {risk_name}</span>'
                f'<br/>Volatility: {vol:.3f}</div>',
                unsafe_allow_html=True
            )

        # Final Verdict (vote count & majority)
        with bottom_col2:
            st.markdown("#### 🏆 Final Verdict")
            votes, majority = compute_final_verdict(convo)
            
            # Display vote counts
            st.markdown(
                f"**BUY:** {votes['BUY']} | **HOLD:** {votes['HOLD']} | **AVOID:** {votes['AVOID']}"
            )
            
            # Display majority decision
            if majority == "BUY":
                verdict_css = "verdict-box buy"
                verdict_icon = "✅ BUY"
            elif majority == "AVOID":
                verdict_css = "verdict-box avoid"
                verdict_icon = "❌ AVOID"
            elif majority == "HOLD":
                verdict_css = "verdict-box hold"
                verdict_icon = "⏸ HOLD"
            else:
                verdict_css = "verdict-box"
                verdict_icon = f"🤝 {majority}"

            st.markdown(
                f'<div class="{verdict_css}"><strong>{verdict_icon}</strong></div>',
                unsafe_allow_html=True
            )

        # Beginner Explanation (call LLM)
        with bottom_col3:
            st.markdown("#### 📚 Beginner Explanation")
            explanation_slot = st.empty()

            if call_llm_for_explain is not None:
                try:
                    # Build a concise prompt from recent messages
                    recent_msgs = convo[-6:] if len(convo) >= 6 else convo
                    msg_summary = "\n".join([
                        f"{m.get('agent', 'Agent')}: {m.get('text', '')[:100]}"
                        for m in recent_msgs
                    ])

                    explain_response = call_llm_for_explain(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a financial explainer. Summarize the debate in 3-4 simple sentences for a beginner investor."
                            },
                            {
                                "role": "user",
                                "content": f"Here's what three analysts debated about {company}:\n\n{msg_summary}\n\nExplain this simply."
                            }
                        ],
                        temperature=0.2,
                        max_output_tokens=200
                    )
                    explanation_slot.info(explain_response)
                except Exception as e:
                    explanation_slot.warning(f"Explanation unavailable: {str(e)[:100]}")
            else:
                explanation_slot.warning("LLM explain service not available.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    "<hr/><p style='color:#9aa4b2;font-size:12px;text-align:center'>"
    "AI Hedge Fund War Room • Powered by Groq LLM • Multi-Agent Debate Framework"
    "</p>",
    unsafe_allow_html=True
)
