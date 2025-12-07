# app/memory/store.py
from collections import defaultdict
from typing import Dict
from .schema import ExtractedMemory

class MemoryStore:
    def __init__(self):
        # session_id -> ExtractedMemory
        self._store: Dict[str, ExtractedMemory] = defaultdict(ExtractedMemory)

    def get(self, session_id: str) -> ExtractedMemory:
        return self._store[session_id]

    def update(self, session_id: str, new_memory: ExtractedMemory):
        existing = self._store[session_id]

        # naive merge: just append for now
        existing.preferences.extend(new_memory.preferences)
        existing.emotional_patterns.extend(new_memory.emotional_patterns)
        existing.facts.extend(new_memory.facts)
memory_store = MemoryStore()