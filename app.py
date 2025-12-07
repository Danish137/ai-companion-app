import streamlit as st
from typing import List

from app.memory.extractor import extract_memory_from_messages
from app.memory.store import memory_store
from app.personality.engine import apply_persona
from app.personality.personas import PersonaType
from app.llm.client import llm_chat


# STREAMLIT UI

st.set_page_config(page_title="GupPshupp – Memory & Personality Engine", page_icon="💬")

st.title("GupPshupp – Memory & Personality Engine Demo")


# Session state

if "history" not in st.session_state:
    st.session_state.history: List[str] = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "demo_user"

session_id = st.text_input("Session ID", value=st.session_state.session_id)
st.session_state.session_id = session_id

persona: PersonaType = st.selectbox(
    "Choose persona",
    options=["calm_mentor", "witty_friend", "therapist", "neutral"],
    index=0,
)

user_msg = st.text_input("Your message", "")


# On Send

if st.button("Send") and user_msg:
    st.session_state.history.append(user_msg)
    history = st.session_state.history

    # 1) Extract memory from last 30 messages
    last_30 = history[-30:]
    extracted = extract_memory_from_messages(last_30)
    memory_store.update(session_id, extracted)

    # 2) Build memory summary
    user_mem = memory_store.get(session_id)

    prefs_lines = [f"- {p.value}" for p in user_mem.preferences]
    emo_lines = [
        f"- When {e.trigger} → typically feels {e.typical_emotion}"
        for e in user_mem.emotional_patterns
    ]
    fact_lines = [f"- {f.value}" for f in user_mem.facts]

    memory_summary = "Known user memory:\n"
    if prefs_lines:
        memory_summary += "\nPreferences:\n" + "\n".join(prefs_lines)
    if emo_lines:
        memory_summary += "\n\nEmotional patterns:\n" + "\n".join(emo_lines)
    if fact_lines:
        memory_summary += "\n\nFacts:\n" + "\n".join(fact_lines)
    if not (prefs_lines or emo_lines or fact_lines):
        memory_summary += "\n(none yet)"

    # 3) Neutral reply (core AI answer)
    neutral = llm_chat(
        system=(
            "You are a neutral, helpful assistant.\n"
            "Use the provided user memory to personalize your answer when relevant.\n"
            "Always finish your thoughts fully."
        ),
        user=f"{memory_summary}\n\nUser: {user_msg}",
        max_tokens=768,
        temperature=0.2,
    )

    # 4) Personality transform (after)
    persona_reply = apply_persona(user_msg, neutral, persona)

    # 5) Show UI results
    st.markdown("### Neutral reply (before personality)")
    st.write(neutral)

    st.markdown(f"### Persona reply (after) — `{persona}`")
    st.write(persona_reply)

    with st.expander("🔍 Debug: Memory used"):
        st.code(memory_summary)

    with st.expander("🔍 Debug: History (last 30)"):
        st.write(last_30)

else:
    st.info("Type a message and click **Send** to start.")
