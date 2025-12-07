from .personas import PERSONA_DEFINITIONS, PersonaType
from ..llm.client import llm_chat

PERSONALITY_SYSTEM_PROMPT = """
You are a style adapter for an AI assistant.
Given:
1) The user's message
2) A base reply (neutral, factual)
3) A target persona description

Task:
- Rewrite the base reply in the target persona's tone.
- Preserve ALL factual content and instructions.
- Do not invent new facts.
- Do not contradict the original answer.

Return ONLY the rewritten reply, as plain text.
"""

def apply_persona(
    user_message: str,
    base_reply: str,
    persona: PersonaType
) -> str:
    persona_desc = PERSONA_DEFINITIONS[persona]

    user_prompt = f"""
[USER MESSAGE]
{user_message}

[BASE REPLY]
{base_reply}

[PERSONA]
{persona_desc}
"""

    return llm_chat(
        system=PERSONALITY_SYSTEM_PROMPT,
        user=user_prompt,
    )
