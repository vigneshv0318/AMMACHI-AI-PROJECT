# 🏗️ Ammachi AI — Backend System: End-to-End Implementation & Description

> **Project**: Ammachi AI (AI-Native Language Tutor)
> **Backend Framework**: FastAPI (Python)
> **Frontend**: Streamlit
> **Database**: SQLite (local-first)
> **AI Stack**: LangChain · LangGraph · Groq LLMs · Whisper · MediaPipe · Tesseract OCR · ElevenLabs / gTTS

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Project Directory Structure](#3-project-directory-structure)
4. [Entrypoint & Application Bootstrap](#4-entrypoint--application-bootstrap)
5. [CORS & Middleware](#5-cors--middleware)
6. [Database Layer](#6-database-layer)
7. [Data Models (Pydantic)](#7-data-models-pydantic)
8. [API Router Modules](#8-api-router-modules)
   - 8.1 [Auth Module (`api/auth.py`)](#81-auth-module-apiauthpy)
   - 8.2 [Vision Module (`api/vision.py`)](#82-vision-module-apivisionpy)
   - 8.3 [Voice Module (`api/voice.py`)](#83-voice-module-apivoicepy)
   - 8.4 [Culture Module (`api/culture.py`)](#84-culture-module-apiculturepy)
9. [AI & ML Pipeline Details](#9-ai--ml-pipeline-details)
10. [LangGraph Agent Orchestration](#10-langgraph-agent-orchestration)
11. [External Service Integrations](#11-external-service-integrations)
12. [Frontend ↔ Backend Integration](#12-frontend--backend-integration)
13. [Environment Variables](#13-environment-variables)
14. [Dependencies](#14-dependencies)
15. [Data Flow Diagrams](#15-data-flow-diagrams)
16. [Error Handling Strategy](#16-error-handling-strategy)
17. [Security Considerations](#17-security-considerations)
18. [How to Run](#18-how-to-run)

---

## 1. System Overview

Ammachi AI is an AI-powered language tutor designed for children, with a persona of a warm Tamil grandmother ("Ammachi"). The backend system powers three core learning modules:

| Module | Purpose | Key Technology |
|--------|---------|---------------|
| **Vision Node** | Handwriting analysis & stroke-order tutoring | MediaPipe Hands, Tesseract OCR, Groq LLM (Llama-4 Scout multimodal) |
| **Voice Node** | Pronunciation practice & conversational fluency | Groq Whisper (STT), LLM-based stutter cleaning, ElevenLabs / gTTS (TTS) |
| **Cultural Discovery** | Festival-based gamified learning via an AI agent | LangGraph agent, DuckDuckGo search, SQLite gamification |

The backend exposes a **RESTful API** via FastAPI. The Streamlit frontend communicates with it over HTTP.

---

## 2. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        STREAMLIT FRONTEND                        │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────────────┐    │
│  │  Auth UI  │   │  Vision UI   │   │  Cultural Discovery   │    │
│  │ (auth.py) │   │ (vision.py)  │   │  Chat UI (culture.py) │    │
│  └─────┬─────┘   └──────┬───────┘   └──────────┬────────────┘    │
│        │                │                       │                │
│  ┌─────┴─────┐   ┌──────┴───────┐   ┌──────────┴────────────┐   │
│  │  Voice UI  │   │              │   │                       │   │
│  │ (voice.py) │   │              │   │                       │   │
│  └─────┬──────┘   │              │   │                       │   │
└────────┼──────────┼──────────────┼───┼───────────────────────┘   │
         │          │              │                                │
    HTTP │     HTTP │         HTTP │                                │
─────────┼──────────┼──────────────┼────────────────────────────────┘
         ▼          ▼              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND (main.py)                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │                    CORS Middleware                           ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────┐ ┌──────────────┐ ┌────────────┐ ┌─────────────┐│
│  │ Auth Router│ │ Vision Router│ │Voice Router│ │Culture Router││
│  │  /login    │ │ /vision/*    │ │ /voice/*   │ │ /culture/*  ││
│  │  /signup   │ │              │ │            │ │             ││
│  │  /auth/*   │ │              │ │            │ │             ││
│  └──────┬─────┘ └──────┬───────┘ └─────┬──────┘ └──────┬──────┘│
│         │              │               │               │        │
│  ┌──────┴──────────────┴───────────────┴───────────────┴──────┐ │
│  │                    DATABASE LAYER (database.py)             │ │
│  │                    SQLite: ammachi.db                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              EXTERNAL AI/ML SERVICES                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌─────────────┐ │  │
│  │  │ Groq API │ │ Whisper  │ │ ElevenLabs│ │ DuckDuckGo  │ │  │
│  │  │ (LLMs)   │ │  (STT)   │ │  (TTS)    │ │  (Search)   │ │  │
│  │  └──────────┘ └──────────┘ └───────────┘ └─────────────┘ │  │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐                 │  │
│  │  │MediaPipe │ │Tesseract │ │   gTTS    │                 │  │
│  │  │ (Hands)  │ │  (OCR)   │ │(Fallback) │                 │  │
│  │  └──────────┘ └──────────┘ └───────────┘                 │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Project Directory Structure

```
nri-Agent/
├── README.md                          # Project overview
├── BACKEND_ARCHITECTURE.md            # High-level architecture notes
├── abi.jpeg                           # Project logo
│
├── backend/                           # ← BACKEND (FastAPI)
│   ├── main.py                        # Application entrypoint & router registration
│   ├── database.py                    # SQLite database layer (users, scores, stamps)
│   ├── models.py                      # Pydantic request/response models
│   ├── requirements.txt               # Python dependencies
│   ├── ammachi.db                     # SQLite database file (auto-created)
│   ├── diag.py                        # Diagnostic script (import & JWT tests)
│   ├── debug_mp.py                    # MediaPipe debug script
│   ├── test_graph.py                  # LangGraph compilation test
│   │
│   └── api/                           # API router modules
│       ├── __init__.py                # Package init
│       ├── auth.py                    # Authentication endpoints (login, signup, Google OAuth)
│       ├── vision.py                  # Handwriting/image analysis endpoints
│       ├── voice.py                   # Voice analysis & TTS endpoints
│       └── culture.py                 # Cultural discovery agent (LangGraph)
│
└── ammachi/                           # ← FRONTEND (Streamlit)
    ├── app.py                         # Streamlit main app
    ├── auth.py                        # Login/signup UI
    ├── util.py                        # Helpers (API URL, CSS, speech bubble)
    ├── oauth_utils.py                 # Google Sign-In HTML component
    ├── requirements.txt               # Frontend dependencies
    └── modules/
        ├── __init__.py
        ├── vision.py                  # Vision Node UI
        ├── voice.py                   # Voice Node UI
        └── culture.py                 # Cultural Discovery chat UI
```

---

## 4. Entrypoint & Application Bootstrap

**File**: `backend/main.py`

The application starts by:

1. **Loading environment variables** from `.env` via `python-dotenv`.
2. **Initializing the SQLite database** — `database.init_db()` creates the `users` table if it doesn't exist, runs schema migrations, and bootstraps a default `student` user.
3. **Creating the FastAPI app** with the title `"Ammachi Backend"`.
4. **Registering CORS middleware** to allow cross-origin requests from the Streamlit frontend.
5. **Including four API routers**:

| Router | Prefix | Tag | Source |
|--------|--------|-----|--------|
| `auth.router` | *(none)* | Auth | `api/auth.py` |
| `vision.router` | `/vision` | Vision | `api/vision.py` |
| `voice.router` | `/voice` | Voice | `api/voice.py` |
| `culture.router` | `/culture` | Culture | `api/culture.py` |

6. **Defining a health-check root endpoint** `GET /` that returns `{"message": "Ammachi API is running!"}`.

**Start command**:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

---

## 5. CORS & Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allows all origins (Streamlit, dev, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This wide-open CORS policy allows the Streamlit frontend (typically at `http://localhost:8501`) and any other client to communicate with the backend without cross-origin restrictions.

---

## 6. Database Layer

**File**: `backend/database.py`
**Engine**: SQLite (`ammachi.db`)
**Password Hashing**: `passlib` with `pbkdf2_sha256`

### Schema

```sql
CREATE TABLE IF NOT EXISTS users (
    username      TEXT PRIMARY KEY,
    password_hash TEXT,              -- bcrypt/pbkdf2 hash (NULL for Google OAuth users)
    google_id     TEXT,              -- Google OAuth subject ID (NULL for password users)
    points        INTEGER DEFAULT 0, -- Gamification score
    stamps        TEXT DEFAULT '[]'  -- JSON array of earned cultural stamps
);
```

### Functions

| Function | Description |
|----------|-------------|
| `init_db()` | Creates the `users` table, runs column migration for `password_hash`, bootstraps a default `student` user with password `password123`. |
| `get_user(username)` | Returns a dict with `username`, `points`, `stamps`, `password_hash`, `google_id` or `None`. |
| `create_user(username, password?, google_id?)` | Inserts a new user. Hashes the password if provided. Returns `True` on success, `False` on `IntegrityError`. |
| `verify_password(plain, hashed)` | Verifies a plaintext password against its hash using `passlib`. |
| `get_user_by_google_id(google_id)` | Looks up a user by their Google OAuth subject ID. |
| `update_score(username, points_add, new_stamp?)` | Increments the user's points and optionally appends a new unique stamp. Returns the updated `{points, stamps}`. |

### Key Design Decisions

- **Local-first**: SQLite is used for simplicity and zero-config deployment. The database file is created alongside the application.
- **Stamps as JSON**: The `stamps` column stores a JSON-serialized list of strings (e.g., `["Pongal Master", "Diwali Star"]`), deserialized with `json.loads()` on read.
- **Dual Auth Support**: The schema supports both traditional password-based accounts and Google OAuth accounts (via `google_id`).

---

## 7. Data Models (Pydantic)

**File**: `backend/models.py`

All request/response schemas are defined as Pydantic `BaseModel` classes for automatic validation and OpenAPI documentation.

### Request Models

| Model | Fields | Used By |
|-------|--------|---------|
| `LoginRequest` | `username: str`, `password: str` | `POST /login` |
| `SignupRequest` | `username: str`, `password: str` | `POST /signup` |
| `GoogleAuthRequest` | `id_token: str` | `POST /auth/google` |

### Response Models

| Model | Fields | Used By |
|-------|--------|---------|
| `LoginResponse` | `success: bool`, `message: str`, `token?: str`, `username?: str` | Auth endpoints |
| `VisionResponse` | `detected_text: str`, `feedback: str`, `is_correct: bool` | `POST /vision/analyze` |
| `VoiceResponse` | `feedback: str`, `transcription: str` | `POST /voice/analyze` |

Additionally, `culture.py` defines:

| Model | Fields | Used By |
|-------|--------|---------|
| `CultureResponse` | `response: str`, `points: int`, `stamps: List[str]` | `POST /culture/chat` |

---

## 8. API Router Modules

### 8.1 Auth Module (`api/auth.py`)

Handles user authentication with two strategies: **password-based** and **Google OAuth 2.0**.

#### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/auth/config` | Returns the Google Client ID for frontend OAuth setup | None |
| `POST` | `/login` | Traditional username/password login | None |
| `POST` | `/signup` | Create a new account with username/password | None |
| `GET` | `/auth/google/url` | Generates a Google OAuth authorization URL for redirect flow | None |
| `POST` | `/auth/google/exchange` | Exchanges an OAuth authorization code for user credentials | None |
| `POST` | `/auth/google` | Verifies a Google ID token directly (client-side popup flow) | None |

#### JWT Token Generation

```python
def create_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

- **Secret**: `JWT_SECRET` env var, default `"ammachi-secret-key-12345"`
- **Expiry**: 7 days
- **Algorithm**: HS256

#### Login Flow

1. Client sends `POST /login` with `{username, password}`.
2. Backend fetches user from SQLite via `database.get_user()`.
3. Password is verified with `database.verify_password()` (pbkdf2_sha256).
4. On success: returns a JWT token + welcome message.
5. On failure: returns HTTP 401.

#### Signup Flow

1. Client sends `POST /signup` with `{username, password}`.
2. Backend calls `database.create_user()` which hashes the password and inserts.
3. On duplicate username: returns HTTP 400.
4. On success: returns a JWT token + welcome message.

#### Google OAuth Flow (Authorization Code)

1. Frontend calls `GET /auth/google/url` → backend returns Google's authorization URL.
2. User is redirected to Google, authenticates, and is sent back to the Streamlit redirect URI with a `code` parameter.
3. Frontend detects the `code` in query params and calls `POST /auth/google/exchange` with it.
4. Backend exchanges the code for tokens via `google_auth_oauthlib`, verifies the ID token, extracts `sub` (Google ID), `email`, and `name`.
5. If the user doesn't exist: creates a new account with the Google ID.
6. Returns a JWT token.

#### Google OAuth Flow (ID Token — Popup)

1. Frontend renders a Google Sign-In button that produces an `id_token`.
2. Frontend sends `POST /auth/google` with `{id_token}`.
3. Backend verifies the token via `google.oauth2.id_token.verify_oauth2_token()`.
4. Creates or retrieves the user, returns a JWT token.

---

### 8.2 Vision Module (`api/vision.py`)

Handles handwriting analysis with two modes: **stroke tracing** and **general grammar checking**.

#### Endpoint

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/vision/analyze` | Analyzes uploaded image/video for handwriting |

**Parameters** (multipart form):
- `file` (UploadFile): Image (PNG/JPG) or video (MP4/MOV/AVI)
- `target_char` (str, optional): The Tamil character being practiced (for trace mode)
- `mode` (str): `"trace"` for stroke analysis, `"general"` for grammar/spelling

#### Processing Pipeline

##### Trace Mode (`mode="trace"`)

```
Upload (video) → MediaPipe Hands → Extract finger-tip path → 
Draw stroke on canvas → Encode as base64 → 
Send to Groq LLM (Llama-4 Scout multimodal) → Return feedback
```

1. **MediaPipe Hands** processes each video frame to track the index finger tip (landmark #8).
2. The fingertip coordinates are connected into a stroke path drawn on a black canvas.
3. The resulting stroke image is base64-encoded and sent to the **Groq multimodal LLM** with a prompt asking it to evaluate stroke order for the target Tamil character.
4. **Fallback**: If MediaPipe is unavailable, the first video frame is extracted instead.

##### General Mode (`mode="general"`)

```
Upload (image/video) → Extract middle frame (if video) → 
Tesseract OCR (Tamil+English) → Combine with image → 
Send to Groq LLM (Llama-4 Scout multimodal) → Return feedback
```

1. If a video is uploaded, the middle frame is extracted with OpenCV.
2. **Tesseract OCR** runs on the image with preprocessing (grayscale, 2× upscale, adaptive thresholding) to extract Tamil+English text.
3. Both the OCR text and the base64-encoded image are sent to the **Groq LLM** with an "Ammachi" persona prompt.
4. The LLM transcribes, corrects grammar/spelling, and provides warm feedback.

#### Key Components

| Component | Purpose |
|-----------|---------|
| `MediaPipe Hands` | Detects hand landmarks in video frames for stroke tracking |
| `OpenCV` | Video frame extraction, image preprocessing |
| `Tesseract OCR` | Optical character recognition for Tamil + English |
| `Groq LLM (Llama-4 Scout)` | Multimodal analysis — understands both text and images |

#### Cleanup

All temporary files (`*.mp4`, `*_stroke.png`, `*_frame.png`) are deleted in the `finally` block.

---

### 8.3 Voice Module (`api/voice.py`)

Handles speech analysis and text-to-speech generation.

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/voice/analyze` | Transcribes audio, cleans stutters, generates conversational reply |
| `POST` | `/voice/speak` | Converts text to speech audio |

#### Voice Analyze Pipeline (`POST /voice/analyze`)

```
Audio Upload (.wav) → Groq Whisper (STT) → Raw Transcription →
Patience Agent (LLM stutter cleaning) → Cleaned Text →
Ammachi Conversational Agent (LLM) → Feedback Response
```

**Step 1: Speech-to-Text**
- Uses **Groq's Whisper Large V3** model.
- Language hint set to Tamil (`ta`), but Whisper auto-detects mixed Tamil/English (Tanglish).

**Step 2: Patience Agent (Stutter Cleaning)**
- Uses **Groq LLM (Llama 3.3 70B Versatile)** to clean the raw transcription.
- Removes repeated words (stutters like "A... A... Amma").
- Removes filler words (um, uh).
- Fixes phonetic misinterpretations.
- This is a key accessibility feature for children with speech difficulties.

**Step 3: Conversational Reply**
- Uses the same **Groq LLM** with an "Ammachi" persona prompt.
- Replies relevantly to the child's cleaned message.
- Performs **recasting** — subtly corrects grammar by repeating the sentence correctly within the reply.
- Uses Tanglish and terms of endearment ("Kanna", "Chellam", "Sabash").

#### Text-to-Speech Pipeline (`POST /voice/speak`)

```
Text Input → Clean markdown/symbols → Detect language →
├─ Tamil detected → gTTS (Tamil) → Audio stream
└─ English/Tanglish → ElevenLabs API → Audio stream
                      └─ Fallback → gTTS (English) → Audio stream
```

**Text Cleaning** (`clean_text_for_speech()`):
- Strips markdown bold/italic (`**`, `__`)
- Replaces colons with periods
- Removes `#` and `-` characters

**Language Detection**:
- Checks if text contains Tamil Unicode characters (`\u0B80`–`\u0BFF`).
- Tamil → **gTTS** (Google Text-to-Speech) with `lang='ta'`.
- English/Tanglish → **ElevenLabs** with the "Dorothy" voice (`eleven_multilingual_v2` model).
- Fallback → **gTTS** in English if ElevenLabs fails.

**Response**: Returns a `StreamingResponse` with `audio/mpeg` content type.

---

### 8.4 Culture Module (`api/culture.py`)

The most complex module — implements a **LangGraph-based AI agent** for interactive cultural discovery.

#### Endpoint

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/culture/chat` | Multi-turn conversation with the Cultural Discovery Agent |

**Parameters** (multipart form):
- `message` (str): The user's latest message
- `history` (str): JSON-serialized conversation history
- `username` (str): Current user (default `"student"`)
- `language` (str): Selected language (Tamil, Hindi, Telugu, etc.)

#### LangGraph Agent Architecture

The culture module builds a **stateful agent graph** using LangGraph:

```
                    ┌─────────────┐
                    │  ENTRY      │
                    │  POINT      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
              ┌────►│   AGENT     │◄────┐
              │     │  (LLM Node) │     │
              │     └──────┬──────┘     │
              │            │            │
              │     ┌──────┴──────┐     │
              │     │  Has Tool   │     │
              │     │   Calls?    │     │
              │     └──┬──────┬───┘     │
              │    Yes │      │ No      │
              │        ▼      ▼         │
              │  ┌──────────┐  END      │
              └──│  ACTION  │           │
                 │(ToolNode)│───────────┘
                 └──────────┘
```

**Nodes**:
1. **Agent Node**: Invokes the LLM (Groq, `openai/gpt-oss-120b` model with tool bindings). The LLM decides whether to call a tool or respond directly.
2. **Action Node**: Executes the tool selected by the agent and returns results.

**Conditional Edge**: After the agent node, if the response contains `tool_calls`, route to the action node. Otherwise, route to `END`.

**Loop**: After the action node completes, control returns to the agent node to process tool results.

#### Agent Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_youtube` | Searches DuckDuckGo for kid-friendly videos about a topic | `query`, `language` |
| `search_image` | Searches DuckDuckGo for festival celebration images | `query`, `language` |
| `update_user_score` | Awards points and stamps to the user in SQLite | `username`, `points`, `stamp` |
| `get_festival_content` | Retrieves hardcoded educational content about Indian festivals | `festival_name` |
| `get_relevant_festival` | Returns festivals appropriate for a given language/culture | `language` |

**Festival Knowledge Base** (in `get_festival_content`):

| Festival | Language/Culture |
|----------|-----------------|
| Pongal, Deepavali, Puthandu, Thaipusam, Karthigai Deepam | Tamil |
| Diwali, Holi, Navratri, Ganesh Chaturthi, Durga Puja | Hindi |
| Onam, Vishu | Malayalam |
| Ugadi, Sankranti, Bonalu, Deepavali | Telugu |
| Dasara, Ugadi, Deepavali | Kannada |

#### Agent State

```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]  # Conversation history (append-only)
    username: str                                          # Current user
```

#### Dynamic System Prompt

The persona changes based on the selected language:

| Language | Persona | Style |
|----------|---------|-------|
| Tamil | Ammachi | Tanglish |
| Hindi | Dadi | Hinglish |
| Other | Grandma | English |

The system prompt instructs the agent to:
1. Greet the child.
2. List relevant festivals using the `get_relevant_festival` tool.
3. When a festival is picked, retrieve content, images, and videos.
4. Present a knowledge challenge.
5. Award points/stamps only for correct answers via `update_user_score`.

#### Technical Artifact Scrubbing

The `scrub_technical_bits()` function cleans LLM responses of leaked internal syntax:
- JSON tool-call blocks (`{"function": "..."}`).
- LangChain/OpenAI-style parameter blocks.
- XML-style `<function>` or `<tool>` tags.
- Dangling artifacts.

This ensures the child never sees raw tool invocations in the chat.

#### Chat Endpoint Flow

1. **Deserialize history**: Parse the JSON history string into `HumanMessage`/`AIMessage` objects.
2. **Build message list**: Prepend the dynamic system prompt + context, append the new user message.
3. **Invoke the LangGraph agent**: `app_graph.invoke(inputs)`.
4. **Extract response**: Take the last message from the final state.
5. **Scrub artifacts**: Clean any leaked technical syntax.
6. **Fetch user stats**: Read the latest points/stamps from the database.
7. **Return**: `CultureResponse` with the agent's reply, points, and stamps.

---

## 9. AI & ML Pipeline Details

### LLM Models Used

| Model | Provider | Used In | Purpose |
|-------|----------|---------|---------|
| `meta-llama/llama-4-scout-17b-16e-instruct` | Groq | Vision Module | Multimodal image+text analysis |
| `llama-3.3-70b-versatile` | Groq | Voice Module | Stutter cleaning + conversational reply |
| `openai/gpt-oss-120b` | Groq | Culture Module | Agent orchestration with tool calling |
| `whisper-large-v3` | Groq | Voice Module | Speech-to-text transcription |

### Computer Vision Pipeline

```
Video/Image → OpenCV (read/resize) → 
├─ MediaPipe Hands (landmark detection) → Stroke path extraction
└─ Adaptive Thresholding → Tesseract OCR (Tamil+English)
    → base64 encode → Groq multimodal LLM
```

### Speech Pipeline

```
Audio (.wav) → Groq Whisper STT → Raw text →
LLM Patience Agent (stutter/filler removal) → Cleaned text →
LLM Ammachi Agent (conversational reply) → Reply text →
├─ Tamil: gTTS → Audio
└─ English: ElevenLabs → Audio (fallback: gTTS)
```

---

## 10. LangGraph Agent Orchestration

The Cultural Discovery module uses **LangGraph** (from LangChain) to create a **ReAct-style agent** that can autonomously decide when to call tools.

### Graph Compilation

```python
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)       # LLM reasoning
workflow.add_node("action", tool_node)       # Tool execution
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)  # tool_calls → action, else → END
workflow.add_edge("action", "agent")         # tool results → back to LLM
app_graph = workflow.compile()
```

### Example Agent Execution Trace

```
User: "Tell me about Pongal"

→ Agent (LLM): Calls get_festival_content("Pongal")
  → Action: Returns "Pongal is a harvest festival..."
→ Agent (LLM): Calls search_image("Pongal")
  → Action: Returns "[IMAGE: https://...]"
→ Agent (LLM): Calls search_youtube("Pongal")
  → Action: Returns "[VIDEO: https://...]"
→ Agent (LLM): Generates response with story + challenge question
  → END: Returns to user

User: "It celebrates the Sun God"

→ Agent (LLM): Correct! Calls update_user_score("student", "10", "Pongal Master")
  → Action: Updates database, returns {"points": 10, "stamps": ["Pongal Master"]}
→ Agent (LLM): Congratulates child, asks next question
  → END: Returns to user
```

---

## 11. External Service Integrations

| Service | Purpose | SDK/Library | Config |
|---------|---------|-------------|--------|
| **Groq** | LLM inference (Llama, Whisper) | `groq`, `langchain-groq` | `GROQ_API_KEY` |
| **Google OAuth** | User authentication | `google-auth`, `google-auth-oauthlib` | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |
| **ElevenLabs** | High-quality English TTS | `elevenlabs` | `ELEVEN_LABS_API` or `ELEVENLABS_API_KEY` |
| **gTTS** | Tamil TTS (fallback English TTS) | `gTTS` | None (free) |
| **DuckDuckGo** | Video & image search | `duckduckgo-search` | None (free) |
| **Tesseract OCR** | Tamil/English text recognition | `pytesseract` | `TESSERACT_PATH` (optional) |
| **MediaPipe** | Hand landmark detection | `mediapipe` | None |

---

## 12. Frontend ↔ Backend Integration

The Streamlit frontend (`ammachi/`) communicates with the FastAPI backend via HTTP `requests`.

### API Call Map

| Frontend Module | Backend Endpoint | Data Format |
|-----------------|-----------------|-------------|
| `auth.py` → Login form | `POST /login` | JSON `{username, password}` |
| `auth.py` → Signup form | `POST /signup` | JSON `{username, password}` |
| `auth.py` → Google button | `GET /auth/google/url` | — |
| `auth.py` → Google callback | `POST /auth/google/exchange` | Form `{code}` |
| `modules/vision.py` → Trace mode | `POST /vision/analyze` | Multipart `{file, target_char, mode}` |
| `modules/vision.py` → Grammar mode | `POST /vision/analyze` | Multipart `{file, mode}` |
| `modules/vision.py` → Voice-over | `POST /voice/speak` | Form `{text}` |
| `modules/voice.py` → Record | `POST /voice/analyze` | Multipart `{file}` |
| `modules/voice.py` → Ammachi speaks | `POST /voice/speak` | Form `{text}` |
| `modules/culture.py` → Chat | `POST /culture/chat` | Form `{message, history, username, language}` |

### Configuration

The backend URL is configured in `ammachi/util.py`:
```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

---

## 13. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | **Yes** | — | API key for Groq LLM and Whisper services |
| `JWT_SECRET` | No | `"ammachi-secret-key-12345"` | Secret key for JWT token signing |
| `GOOGLE_CLIENT_ID` | No | `""` | Google OAuth 2.0 client ID |
| `GOOGLE_CLIENT_SECRET` | No | `""` | Google OAuth 2.0 client secret |
| `GOOGLE_REDIRECT_URI` | No | `"http://localhost:8501"` | OAuth redirect URI (Streamlit port) |
| `ELEVEN_LABS_API` / `ELEVENLABS_API_KEY` | No | — | ElevenLabs TTS API key |
| `ELEVENLABS_VOICE_ID` | No | `"ThT5KcBeYPX3keUQqHPh"` | ElevenLabs voice ID ("Dorothy") |
| `TESSERACT_PATH` | No | System default | Custom Tesseract binary path |
| `API_URL` | No | `"http://localhost:8000"` | Backend URL (used by Streamlit frontend) |

---

## 14. Dependencies

### Backend (`backend/requirements.txt`)

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `python-multipart` | Multipart form data parsing |
| `pydantic` | Data validation & serialization |
| `python-dotenv` | Environment variable loading |
| `groq` | Groq API client (Whisper STT) |
| `deepgram-sdk` | Deepgram STT (available but not actively used) |
| `langgraph` | Agent graph orchestration |
| `langchain` | LLM framework |
| `langchain-groq` | Groq LLM integration for LangChain |
| `langchain-google-genai` | Google GenAI integration (available) |
| `langchain-openai` | OpenAI-compatible integration |
| `duckduckgo-search` | Web/video/image search |
| `mediapipe` | Hand landmark detection |
| `opencv-python-headless` | Computer vision (video/image processing) |
| `transformers` | Hugging Face model support |
| `torch` / `torchvision` | PyTorch ML framework |
| `accelerate` | Hugging Face model acceleration |
| `qwen-vl-utils` | Qwen2-VL vision-language utilities |
| `decord` | Efficient video decoding |
| `elevenlabs` | ElevenLabs TTS |
| `gTTS` | Google Text-to-Speech (free) |

### Frontend (`ammachi/requirements.txt`)

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `Pillow` | Image processing |
| `requests` | HTTP client for backend API calls |

---

## 15. Data Flow Diagrams

### Authentication Flow

```
┌──────────┐     POST /login      ┌──────────┐     get_user()     ┌──────────┐
│  Client   │ ──────────────────► │  FastAPI  │ ─────────────────► │  SQLite  │
│(Streamlit)│     {user, pass}    │  Auth     │                    │          │
│           │ ◄────────────────── │  Router   │ ◄───────────────── │          │
│           │  {token, username}  │           │   user record      │          │
└──────────┘                      └──────────┘                     └──────────┘
```

### Vision Analysis Flow

```
┌──────────┐   POST /vision/analyze   ┌──────────┐
│  Client   │ ──── file + mode ─────► │  Vision   │
│(Streamlit)│                          │  Router   │
│           │ ◄── VisionResponse ──── │           │
└──────────┘                          └─────┬─────┘
                                            │
                   ┌────────────────────────┤
                   │                        │
           ┌───────▼────────┐       ┌───────▼────────┐
           │  mode="trace"  │       │ mode="general" │
           └───────┬────────┘       └───────┬────────┘
                   │                        │
           ┌───────▼────────┐       ┌───────▼────────┐
           │  MediaPipe     │       │  Tesseract     │
           │  Hands         │       │  OCR           │
           └───────┬────────┘       └───────┬────────┘
                   │                        │
                   └────────────┬───────────┘
                                │
                        ┌───────▼────────┐
                        │  Groq LLM      │
                        │  (Multimodal)  │
                        └───────┬────────┘
                                │
                        ┌───────▼────────┐
                        │   Feedback     │
                        │   Response     │
                        └────────────────┘
```

### Voice Analysis Flow

```
┌──────────┐   POST /voice/analyze    ┌──────────┐
│  Client   │ ──── audio (.wav) ────► │  Voice   │
│(Streamlit)│                          │  Router  │
│           │ ◄── VoiceResponse ───── │          │
└──────────┘                          └─────┬────┘
                                            │
                              ┌─────────────┼─────────────┐
                              ▼             ▼             ▼
                        ┌──────────┐ ┌───────────┐ ┌──────────────┐
                        │  Whisper │ │ Patience  │ │   Ammachi    │
                        │  (STT)  │→│  Agent    │→│ Conversation │
                        │         │ │(Stutter   │ │   Agent      │
                        │         │ │ Cleaning) │ │              │
                        └──────────┘ └───────────┘ └──────────────┘
```

### Cultural Discovery Agent Flow

```
┌──────────┐   POST /culture/chat     ┌──────────┐
│  Client   │ ── msg + history ─────► │ Culture  │
│(Streamlit)│                          │ Router   │
│           │ ◄── CultureResponse ─── │          │
└──────────┘                          └─────┬────┘
                                            │
                                    ┌───────▼────────┐
                                    │  Build Message │
                                    │  List + System │
                                    │  Prompt        │
                                    └───────┬────────┘
                                            │
                                    ┌───────▼────────┐
                                    │  LangGraph     │
                                    │  Agent Loop    │◄─────────┐
                                    │                │          │
                                    └───────┬────────┘          │
                                            │                   │
                                     ┌──────┴──────┐            │
                                     │ Tool Calls? │            │
                                     └──┬──────┬───┘            │
                                    Yes │      │ No             │
                                        ▼      ▼               │
                                 ┌──────────┐  END              │
                                 │  Execute  │                  │
                                 │  Tools:   │──────────────────┘
                                 │• youtube  │
                                 │• image    │
                                 │• festival │
                                 │• score    │
                                 └──────────┘
```

---

## 16. Error Handling Strategy

The backend uses a consistent error-handling pattern across all modules:

1. **HTTP Exceptions** for client-facing errors:
   ```python
   raise HTTPException(status_code=401, detail="Invalid credentials")
   ```

2. **Try/Except with Traceback** for internal errors:
   ```python
   except Exception as e:
       traceback.print_exc()
       return VisionResponse(
           detected_text="Error",
           feedback=f"Aiyayo! My eyes are a bit blurry: {str(e)}",
           is_correct=False
       )
   ```

3. **Graceful Degradation**:
   - MediaPipe unavailable → falls back to first-frame extraction.
   - ElevenLabs fails → falls back to gTTS.
   - Tool errors in agent → error message included in response, agent continues.

4. **Ammachi Persona in Errors**: Error messages use the grandmother persona ("Aiyayo!", "My ears are not working properly") to maintain the experience even during failures.

---

## 17. Security Considerations

| Area | Implementation | Notes |
|------|---------------|-------|
| **Password Storage** | pbkdf2_sha256 via `passlib` | Industry-standard hashing |
| **Authentication** | JWT tokens (HS256, 7-day expiry) | Tokens returned to client on login |
| **OAuth** | Google OAuth 2.0 with authorization code flow | ID tokens verified server-side |
| **CORS** | `allow_origins=["*"]` | Wide-open for development; should be restricted in production |
| **Input Validation** | Pydantic models for all request bodies | Automatic type checking and serialization |
| **File Uploads** | Temp files with `finally` cleanup | Prevents file system pollution |
| **SQL Injection** | Parameterized queries (`?` placeholders) | SQLite operations use safe parameter binding |

---

## 18. How to Run

### Prerequisites

- Python 3.8+
- Tesseract OCR installed (for vision module)
- API keys for Groq (required), ElevenLabs (optional), Google OAuth (optional)

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_key
JWT_SECRET=your_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
ELEVENLABS_API_KEY=your_elevenlabs_key
EOF

# Start the server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd ammachi

# Install dependencies
pip install -r requirements.txt

# Start Streamlit
streamlit run app.py --server.port 8501
```

### Verify

- Backend health check: `http://localhost:8000/`
- API documentation: `http://localhost:8000/docs` (Swagger UI)
- Frontend: `http://localhost:8501`

---

> **Document Version**: 1.0
> **Generated**: April 2026
> **Repository**: [Abishek0070/nri-Agent](https://github.com/Abishek0070/nri-Agent)
