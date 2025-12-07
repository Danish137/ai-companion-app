import json
from json import JSONDecodeError
from typing import List

from .schema import ExtractedMemory
from ..llm.client import llm_chat


EXTRACTION_SYSTEM_PROMPT = """
You are a memory extraction module for a personal AI companion.

Goal:
From the LAST 30 USER MESSAGES ONLY, extract:
1) User preferences
2) Emotional patterns
3) Facts worth remembering

Rules:
- Only include information that is likely to be useful in future conversations.
- Ignore one-off details that are unlikely to matter later.
- Prefer stable, long-term traits over temporary states.
- Include a confidence score between 0 and 1.
- Use message indices (0..n-1) as evidence_messages.

Output format:
- You MUST return ONLY raw JSON. Do NOT wrap it in backticks or Markdown.
- The JSON must strictly follow this shape:

{
  "preferences": [
    {
      "category": "string",
      "value": "string",
      "evidence_messages": [0],
      "confidence": 0.9,
      "stability": "short_term" or "long_term"
    }
  ],
  "emotional_patterns": [
    {
      "trigger": "string",
      "typical_emotion": "string",
      "description": "string",
      "evidence_messages": [0],
      "confidence": 0.9
    }
  ],
  "facts": [
    {
      "fact_type": "string",
      "value": "string",
      "evidence_messages": [0],
      "confidence": 0.9,
      "expiry": "none" or "YYYY-MM-DD"
    }
  ]
}

If you cannot find any meaningful memory, return:
{
  "preferences": [],
  "emotional_patterns": [],
  "facts": []
}
"""


def _clean_json_text(raw: str) -> str:
    """
    Clean LLM output so it becomes valid JSON text:
    - Strip whitespace
    - Remove Markdown code fences ```...``` (with or without 'json')
    - Extract substring between first '{' and last '}' if needed
    """
    if not raw:
        return ""

    text = raw.strip()

    # Remove leading/trailing ``` fences if present
    if text.startswith("```"):
        lines = text.splitlines()

        # Drop first line if it's a fence (``` or ```json)
        if lines and lines[0].lstrip().startswith("```"):
            lines = lines[1:]

        # Drop last line if it's a fence
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # Sometimes there's extra commentary before/after, so grab JSON region
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1].strip()

    return text


def extract_memory_from_messages(messages: List[str]) -> ExtractedMemory:
    """
    Given the last N (up to 30) user messages, ask the LLM to extract
    structured memory and parse it into an ExtractedMemory object.

    This function is robust against:
    - Empty LLM responses
    - Markdown-wrapped JSON (```json ... ```)
    - Extra text around the JSON

    On parse failure, it returns an empty ExtractedMemory instead of crashing.
    """
    numbered = [f"[{i}] {m}" for i, m in enumerate(messages)]

    #see how many messages are used for memory extraction
    print(f"[MEMORY] Extracting from {len(messages)} messages")

    user_prompt = "Here are the last user messages:\n\n" + "\n".join(numbered)

    raw = llm_chat(
        system=EXTRACTION_SYSTEM_PROMPT,
        user=user_prompt,
    )

    if not raw or not raw.strip():
        print("[MEMORY] Empty response from LLM, returning empty memory.")
        return ExtractedMemory()

    cleaned = _clean_json_text(raw)

    try:
        data = json.loads(cleaned)
    except JSONDecodeError:
        print("[MEMORY] Failed to parse JSON from LLM. Raw output:\n", raw)
        print("[MEMORY] Cleaned string was:\n", cleaned)
        return ExtractedMemory()

    try:
        mem = ExtractedMemory(**data)
        print(
            f"[MEMORY] Parsed successfully: "
            f"{len(mem.preferences)} prefs, "
            f"{len(mem.emotional_patterns)} patterns, "
            f"{len(mem.facts)} facts"
        )
        return mem
    except Exception as e:
        print("[MEMORY] Failed to map JSON into ExtractedMemory:", e)
        print("JSON was:", data)
        return ExtractedMemory()
