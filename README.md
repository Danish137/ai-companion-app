---
title: AI Companion – Memory & Personality Engine
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "0.0.1"
app_file: app.py
pinned: false
---

# Guppshupp – Memory Extraction + Personality Engine  
### *AI Companion Assignment – GupPshupp | Built by Danish Akhtar*  

...
# Guppshupp – Memory Extraction + Personality Engine
**AI Companion Assignment – Guppshupp | Built by Danish Akhtar**

This project implements a lightweight **AI Companion System** capable of:

- **Extracting** user preferences, emotional patterns, and important facts from chat history
- **Maintaining** a memory store that evolves as the user chats
- **Applying** dynamic personalities (witty friend, calm mentor, therapist-style, etc.) to the model's responses
- **Demonstrating** the before/after transformation with persona rewriting
- **Running** fully in-browser using Streamlit, with Groq LLM powering all logic

This assignment showcases **modular design**, **structured output parsing**, **prompt engineering**, **memory conditioning**, and **personality transformation**.

---

## 🚀 Live Demo

👉 **Live App:** [https://huggingface.co/spaces/imdanishakhtar7/ai-companion-app](https://huggingface.co/spaces/imdanishakhtar7/ai-companion-app)


---

## 📦 Repository Structure
```
GUPPSHUPP_Assignment/
│
├── app.py                         # Streamlit UI (main entrypoint)
│
├── app/
│   ├── llm/
│   │   ├── client.py              # Groq LLM wrapper
│   │
│   ├── memory/
│   │   ├── extractor.py           # Memory extraction engine
│   │   ├── schema.py              # Pydantic models
│   │   ├── store.py               # In-memory memory storage
│   │
│   ├── personality/
│       ├── personas.py            # Persona definitions
│       ├── engine.py              # Persona transformation logic
│
├── requirements.txt
├── README.md
```

---

## 🧠 Core Features

### 1. Memory Extraction from Last 30 Messages

The system takes **only the last 30 user messages** and extracts:

✔ **User Preferences**
- Interests
- Likes/dislikes
- Long-term traits (e.g., AIML background, sports love)

✔ **Emotional Patterns**
- Consistent emotional reactions
- Triggers that cause anxiety, excitement, frustration, etc.

✔ **Facts Worth Remembering**
- Education
- Career goals
- Life details that could matter to a companion AI

**Prompt Design:**  
The LLM is instructed to output **strict JSON**, with:
```json
{
  "preferences": [...],
  "emotional_patterns": [...],
  "facts": [...]
}
```

The system is resilient to model imperfections (handles backticks, malformed JSON, trailing text, etc.).

---

### 2. Memory Store (Session-Based)

Each session gets its own memory object:
```
memory_store[session_id] → ExtractedMemory
```

- **Not shared** across users
- **Not persisted** (reset on app restart)
- Clean & expandable design

---

### 3. Personality Engine (Before → After Transformation)

The system first generates a **neutral reply**, then **rewrites** it in the chosen persona style:

**Available personas:**
- Calm Mentor
- Witty Friend
- Therapist
- Neutral

**Personality Engine Rules:**
- Preserve factual correctness
- Maintain all key advice
- Transform **only the tone**
- Never hallucinate new facts not present in base reply

---

### 4. Full Streamlit UI

- Live chat
- Persona selector
- Memory debug panel
- Last 30 messages viewer

**Shows:**
- Neutral reply
- Persona-transformed reply
- Memory used in this response


---

## 🔧 Model Used (via Groq API)

This project uses **Groq** for ultra-fast inference with the model:
```
meta-llama/llama-4-scout-17b-16e-instruct
```

**Why this model:**
- Highly instruction-following
- Strong JSON compliance
- Perfect for memory extraction + persona rewriting
- Fast inference on Groq hardware

---

## 🛠 Installation

### 1. Clone the repo
```bash
git clone https://github.com/Danish137/ai-companion-app
cd ai-companion-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key

Create `.env`:
```
GROQ_API_KEY=your_key_here
```

### 4. Run locally
```bash
streamlit run app.py
```


## 🧩 How It Works (Step-by-Step)

1. **User sends a message**  
   Stored in `st.session_state.history`.

2. **System extracts last 30 messages**  
```python
   last_30 = history[-30:]
```

3. **Memory extractor builds structured JSON**  
   From the LLM:
   - `preferences[]`
   - `emotional_patterns[]`
   - `facts[]`

4. **Memory is merged into the session memory store**

5. **Neutral reply is generated**  
   With memory summary injected.

6. **Personality engine rewrites reply**

7. **Final UI shows:**
   - Neutral reply
   - Persona reply
   - Memory used
   - Last chat window

---

## 📊 Example Output

**Neutral reply:**
> You seem to enjoy AIML and cricket, and you're planning career options...

**Persona reply — Witty Friend:**
> Broooo AIML + cricket? You're literally coding bouncers in Python...

**Persona reply — Calm Mentor:**
> Let's take this step by step. You have a strong AIML foundation already...

---

## 🔮 Future Scope / Expansion

This architecture is designed to grow. Here are realistic next steps:

### 1. Persistent Long-Term Memory (SQLite / Redis / Chroma)
Store memory beyond session restarts.

### 2. Semantic Memory Retrieval
Using embedding similarity → retrieval of past experiences.

### 3. Emotion-Aware Response Generation
LLM conditioned on emotional trends over time.

### 4. Automatic Persona Learning
Infer the user's preferred communication style.

### 5. Voice Companion Mode
Streaming input + emotion inferences.

### 6. Memory Decay & Expiry
Important for long-term companion behavior.

### 7. Multi-Agent System
- One agent for memory
- One for reasoning
- One for personality tone

---



---

## 👤 Author

**Danish Akhtar**  

---
