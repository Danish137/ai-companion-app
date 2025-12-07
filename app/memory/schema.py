from pydantic import BaseModel
from typing import List, Optional, Literal

class UserPreference(BaseModel):
    id: Optional[str] = None
    category: str          # e.g. "food", "work", "learning_style"
    value: str             # e.g. "prefers late-night coding"
    evidence_messages: List[int]  # indexes or ids from the 30 msgs
    confidence: float      # 0–1
    stability: Literal["short_term", "long_term"]

class EmotionalPattern(BaseModel):
    id: Optional[str] = None
    trigger: str           # "talking about college friends"
    typical_emotion: str   # "sad", "anxious", "excited"
    description: str       # small explanation
    evidence_messages: List[int]
    confidence: float      # 0–1

class Fact(BaseModel):
    id: Optional[str] = None
    fact_type: str         # "bio", "goal", "constraint"
    value: str             # "Finished BTech in AIML in 2025"
    evidence_messages: List[int]
    confidence: float
    expiry: Optional[str] = None  # ISO date or "none"

class ExtractedMemory(BaseModel):
    preferences: List[UserPreference] = []
    emotional_patterns: List[EmotionalPattern] = []
    facts: List[Fact] = []