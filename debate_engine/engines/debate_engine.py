from services.llm_service import call_llm

# -----------------------------
# AGENT PERSONALITIES
# -----------------------------

def get_aggressive_persona(user_context=None):
    """Generate Rajesh's persona with user personalization"""
    user_context = user_context or {}
    user_name = user_context.get("name", "")
    user_gender = user_context.get("gender", "other")
    user_expertise = user_context.get("expertise", "beginner")
    
    # Determine pronouns and terms based on gender
    if user_gender == "female":
        term1 = "girl"
        term2 = "boss"
        example_addr = "girl"
    elif user_gender == "male":
        term1 = "bro"
        term2 = "boss"
        example_addr = "bro"
    else:
        term1 = "boss"
        term2 = ""
        example_addr = "boss"
    
    # Build user-specific instruction
    user_instruction = ""
    if user_name:
        user_instruction = f"\n✅ CRITICAL: You MUST refer to {user_name} as '{term1}' and '{term2}' ALWAYS in EVERY response. Use their name {user_name} naturally in your speech. Example: '{example_addr} {user_name}, this is solid momentum!'"
    else:
        user_instruction = f"\n✅ CRITICAL: Use '{term1}' and '{term2}' when addressing the listener in EVERY response."
    
    # Add expertise-based guidance
    expertise_guidance = ""
    if user_expertise == "beginner":
        expertise_guidance = "\n📚 BEGINNER TRADER: Explain simply. Avoid jargon. Use round numbers. Highlight risks clearly."
    elif user_expertise == "intermediate":
        expertise_guidance = "\n📈 INTERMEDIATE TRADER: Balance enthusiasm with caution. Use technical metrics (PE, volatility). Consider sector context."
    else:  # advanced
        expertise_guidance = "\n🔬 ADVANCED TRADER: Provide deep insights. Discuss contrarian angles. Analyze institutional sentiment nuances."
    
    return f"""You are an aggressive South Indian trader named Aggressive.

Personality:
- Confident and conviction-driven
- Momentum-focused investor
- Professional but approachable
- Uses casual professional tone with light slang

MANDATORY INSTRUCTION:{user_instruction}{expertise_guidance}

Rules:
- Maximum 2–3 sentences
- Use concrete numbers and facts
- Speak clearly and directly
- Energetic but data-backed
- ALWAYS mention listener's name and use their preferred terms

Tone example:
"Girl, institutions accumulated 18% more—this is solid momentum boss. The accumulation is really strong, clear BUY signal!"

Keep it professional with balanced casual tone."""

def get_balanced_persona(user_context=None):
    """Generate Priya's persona with user personalization"""
    user_context = user_context or {}
    user_name = user_context.get("name", "")
    user_gender = user_context.get("gender", "other")
    user_expertise = user_context.get("expertise", "beginner")
    
    # Determine pronouns and terms based on gender
    if user_gender == "female":
        term1 = "girl"
        term2 = "boss"
        example_addr = "girl"
    elif user_gender == "male":
        term1 = "bro"
        term2 = "boss"
        example_addr = "bro"
    else:
        term1 = "boss"
        term2 = ""
        example_addr = "boss"
    
    # Build user-specific instruction
    user_instruction = ""
    if user_name:
        user_instruction = f"\n✅ CRITICAL: You MUST refer to {user_name} as '{term1}' and '{term2}' ALWAYS in EVERY response. Use their name {user_name} naturally in your speech. Example: 'True {example_addr} {user_name}, the PE is elevated but fundamentals solid boss.'"
    else:
        user_instruction = f"\n✅ CRITICAL: Use '{term1}' and '{term2}' when addressing the listener in EVERY response."
    
    # Add expertise-based guidance
    expertise_guidance = ""
    if user_expertise == "beginner":
        expertise_guidance = "\n📚 BEGINNER TRADER: Keep it simple. Explain both sides clearly. Avoid complex metrics. Give actionable guidance."
    elif user_expertise == "intermediate":
        expertise_guidance = "\n📈 INTERMEDIATE TRADER: Provide balanced technical analysis. Consider multiple scenarios. Discuss risk-reward ratios."
    else:  # advanced
        expertise_guidance = "\n🔬 ADVANCED TRADER: Deep fundamental analysis. Compare valuation metrics. Analyze macroeconomic factors."
    
    return f"""You are a balanced South Indian analyst named Balanced.

Personality:
- Logical and objective thinker
- Weighs pros and cons fairly
- Data-driven and transparent
- Professional with measured, conversational tone

MANDATORY INSTRUCTION:{user_instruction}{expertise_guidance}

Rules:
- Maximum 2–3 sentences
- Present balanced evidence
- Respond directly to counterpoints
- Fair and analytical
- ALWAYS mention listener's name and use their preferred terms

Tone example:
"Girl, the PE is elevated at 32 boss, but fundamentals look pretty solid honestly. It's a balanced risk-reward worth keeping an eye on!"

Professional yet approachable."""

def get_safe_persona(user_context=None):
    """Generate Vikram's persona with user personalization"""
    user_context = user_context or {}
    user_name = user_context.get("name", "")
    user_gender = user_context.get("gender", "other")
    user_expertise = user_context.get("expertise", "beginner")
    
    # Determine pronouns and terms based on gender
    if user_gender == "female":
        term1 = "girl"
        term2 = "boss"
        example_addr = "girl"
    elif user_gender == "male":
        term1 = "bro"
        term2 = "boss"
        example_addr = "bro"
    else:
        term1 = "boss"
        term2 = ""
        example_addr = "boss"
    
    # Build user-specific instruction
    user_instruction = ""
    if user_name:
        user_instruction = f"\n✅ CRITICAL: You MUST refer to {user_name} as '{term1}' and '{term2}' ALWAYS in EVERY response. Use their name {user_name} naturally in your speech. Example: '{example_addr} {user_name}, the debt concerns me boss. I'd wait for better entry.'"
    else:
        user_instruction = f"\n✅ CRITICAL: Use '{term1}' and '{term2}' when addressing the listener in EVERY response."
    
    # Add expertise-based guidance
    expertise_guidance = ""
    if user_expertise == "beginner":
        expertise_guidance = "\n📚 BEGINNER TRADER: Emphasize safety first. Point out clear risks. Suggest conservative positions. Explain why caution matters."
    elif user_expertise == "intermediate":
        expertise_guidance = "\n📈 INTERMEDIATE TRADER: Balance caution with opportunity. Discuss hedging strategies. Analyze downside scenarios."
    else:  # advanced
        expertise_guidance = "\n🔬 ADVANCED TRADER: Provide sophisticated risk analysis. Discuss black swan events. Analyze correlation patterns."
    
    return f"""You are a conservative South Indian wealth manager named Safe.

Personality:
- Risk-conscious and protective
- Capital preservation focus
- Highlights concerns clearly
- Professional and measured approach with casual touch

MANDATORY INSTRUCTION:{user_instruction}{expertise_guidance}

Rules:
- Maximum 2–3 sentences
- Lead with risk factors first
- Speak professionally but clearly
- Identify red flags without alarmism
- ALWAYS mention listener's name and use their preferred terms

Tone example:
"Girl, the debt concerns me boss. If interest rates go up, margins could hit hard. I'd wait for better entry point!"

Protective, clear, and relatable."""

# Keep old constants for backward compatibility
AGGRESSIVE_PERSONA = get_aggressive_persona()
BALANCED_PERSONA = get_balanced_persona()
SAFE_PERSONA = get_safe_persona()

# -----------------------------
# BUILD CONTEXT
# -----------------------------

def build_context(company, market_data, institutional_data, user_context=None):
    user_context = user_context or {}
    user_name = user_context.get("name", "")
    user_gender = user_context.get("gender", "other")
    
    # Add user personalization note to context
    user_note = ""
    if user_name:
        if user_gender == "female":
            user_note = f"\n\nYou're talking to {user_name} (she/her). Use 'girl', 'boss' when referring to her."
        elif user_gender == "male":
            user_note = f"\n\nYou're talking to {user_name} (he/him). Use 'bro', 'boss' when referring to him."
        else:
            user_note = f"\n\nYou're talking to {user_name}. Use 'boss' when referring to them."

    return f"""
Company: {company}

Market Data
Price: {market_data['current_price']}
PE Ratio: {market_data['pe_ratio']}
Volatility: {market_data['volatility']}
1Y Return: {market_data['one_year_return']}

Institutional Signals
Weighted Rating: {institutional_data['weighted_rating']}
Consensus Strength: {institutional_data['consensus_strength']}
Disagreement Index: {institutional_data['disagreement']}{user_note}
"""

# -----------------------------
# DEBATE ENGINE
# -----------------------------

def multi_round_debate(company, market_data, institutional_data, user_context=None):

    context = build_context(company, market_data, institutional_data, user_context)

    conversation = []

    # Generate personalized personas based on user context
    agents = {
        "Aggressive": get_aggressive_persona(user_context),
        "Balanced": get_balanced_persona(user_context),
        "Safe": get_safe_persona(user_context)
    }

    responses = {}
    
    # Extract user context for explicit instructions
    user_name = (user_context or {}).get("name", "")
    user_gender = (user_context or {}).get("gender", "other")
    
    # Determine terms for this user
    if user_gender == "female":
        terms_instruction = f"👤 Speaking to: {user_name} (female) → Use 'girl' and 'boss' ALWAYS when addressing them."
    elif user_gender == "male":
        terms_instruction = f"👤 Speaking to: {user_name} (male) → Use 'bro' and 'boss' ALWAYS when addressing them."
    else:
        terms_instruction = f"👤 Speaking to: {user_name} (other) → Use 'boss' ALWAYS when addressing them."

    # Build explicit personalization instruction for user prompt
    personalization_prompt = ""
    if user_name:
        personalization_prompt = f"\n\n{terms_instruction}\n⚠️ CRITICAL: Every sentence must include addressing {user_name} with their preferred terms!"

    # -----------------------------
    # ROUND 1 — OPENING ARGUMENTS
    # -----------------------------

    for name, persona in agents.items():

        messages = [
            {"role": "system", "content": persona},
            {
                "role": "user",
                "content": f"""
{context}{personalization_prompt}

Debate Round 1: Opening Argument.

Speak like you are in a LIVE debate.
Max 2–3 sentences.
Be sharp and conversational.
REMEMBER: Address the listener by their name and preferred terms!
"""
            }
        ]

        response = call_llm(messages)

        responses[name] = response
        conversation.append({
            "agent": name,
            "round": "Opening",
            "text": response
        })

    # -----------------------------
    # ROUND 2 — REBUTTAL ROUND
    # -----------------------------

    for name, persona in agents.items():

        others = "\n".join(
            [f"{k}: {v}" for k, v in responses.items() if k != name]
        )

        messages = [
            {"role": "system", "content": persona},
            {
                "role": "user",
                "content": f"""
{context}{personalization_prompt}

Other Analysts Said:
{others}

Debate Round 2: Rebuttal.

Challenge or agree with them.
Max 2–3 sentences.
Use facts.
REMEMBER: Address the listener by their name and preferred terms!
"""
            }
        ]

        response = call_llm(messages)

        conversation.append({
            "agent": name,
            "round": "Rebuttal",
            "text": response
        })

    # -----------------------------
    # ROUND 3 — FINAL VERDICT
    # -----------------------------

    for name, persona in agents.items():

        messages = [
            {"role": "system", "content": persona},
            {
                "role": "user",
                "content": f"""
{context}{personalization_prompt}

Debate Round 3: Final Decision.

Give final verdict:
BUY / HOLD / AVOID

Max 2 sentences.
Explain reasoning clearly.
REMEMBER: Address the listener by their name and preferred terms!
"""
            }
        ]

        response = call_llm(messages)

        conversation.append({
            "agent": name,
            "round": "Final Verdict",
            "text": response
        })

    return conversation