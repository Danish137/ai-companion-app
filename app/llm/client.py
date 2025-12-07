import os
from typing import List, Dict, Optional

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Please add it to your environment or .env file.")

# Initialise Groq client
client = Groq(api_key=GROQ_API_KEY)

DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def llm_chat(
    system: Optional[str] = None,
    user: Optional[str] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.3,
    max_tokens: int = 768,
) -> str:
    """
    Simple wrapper around Groq's chat completion API.

    Usage patterns:
        llm_chat(system="You are...", user="Hello")
        llm_chat(messages=[{"role": "system", "content": "You are..."}, {"role": "user", "content": "Hi"}])

    Returns:
        reply content as a string.
    """

    # Build messages list if caller used (system, user) pattern
    if messages is None:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        if user:
            messages.append({"role": "user", "content": user})

    if not messages:
        raise ValueError("llm_chat called without any messages.")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    
    content = response.choices[0].message.content
    return content.strip() if content else ""
