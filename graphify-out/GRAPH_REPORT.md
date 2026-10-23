# Graph Report - AMMACHI-AI-PROJECT  (2026-10-23)

## Corpus Check
- 141 files · ~321,841 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 3, .example 1, .ico 1)

## Summary
- 861 nodes · 2198 edges · 49 communities (31 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- App Shell & Routing
- Learn API (Duolingo Pack)
- Streamlit Legacy App
- Handwriting API
- Challenge API
- Frontend Build & Deps
- Auth API
- Database & CRUD
- Culture API
- Shared Auth Dependency
- Culture Agent Graph (LangGraph)
- AI SDK Dependencies
- LangGraph Messaging Types
- Learn Content Seed
- Ammachi Brand Assets
- Avatar Storage
- DB Connection & Init
- PWA Install Flow
- Patience & Gemini Services
- Culture Service
- Vision Stack
- Culture Image Themes
- Backend Docs & Persona
- Diagnostics & Migration
- Backend Architecture Concepts
- Auth Schemas
- Voice Pipeline
- Direct DB Session
- Festival Imagery
- Core Python Deps
- Legacy Stack Map
- Security Config
- Gamification Economy
- Exception Handling
- Pillow Deps
- Streamlit Deps
- Password Hashing Deps
- Google Auth Deps
- Postgres Deps
- Vercel Config
- Deepgram STT
- ElevenLabs TTS
- gTTS
- NumPy
- OpenCV Dep
- dotenv

## God Nodes (most connected - your core abstractions)
1. `react` - 33 edges
2. `lucide-react` - 26 edges
3. `AmmachiMascot()` - 26 edges
4. `useAuth()` - 23 edges
5. `useLanguage()` - 23 edges
6. `evaluate_handwriting()` - 20 edges
7. `App()` - 19 edges
8. `react-router-dom` - 18 edges
9. `HandwritingPreprocessor` - 16 edges
10. `run_culture_chat()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Microservices Architecture` --semantically_similar_to--> `FastAPI Backend (RESTful API)`  [AMBIGUOUS] [semantically similar]
  BACKEND_ARCHITECTURE.md → BACKEND_SYSTEM.md
- `User Service` --semantically_similar_to--> `backend/api/auth.py (Auth Router)`  [AMBIGUOUS] [semantically similar]
  BACKEND_ARCHITECTURE.md → BACKEND_SYSTEM.md
- `API Gateway` --semantically_similar_to--> `FastAPI Backend (RESTful API)`  [AMBIGUOUS] [semantically similar]
  BACKEND_ARCHITECTURE.md → BACKEND_SYSTEM.md
- `Requests (HTTP client)` --conceptually_related_to--> `FastAPI 0.142.2`  [INFERRED]
  ammachi/requirements.txt → backend/requirements.txt
- `Ammachi AI Backend System Document` --references--> `Deepgram Nova-2 STT`  [AMBIGUOUS]
  BACKEND_SYSTEM.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Voice Analysis & TTS Pipeline (STT -> Stutter Cleaning -> Conversational Reply -> TTS)** — backend_system_api_voice_py, backend_system_groq_whisper_large_v3, backend_system_patience_agent, backend_system_groq_llama_3_3_70b, readme_elevenlabs_tts, backend_system_gtts [EXTRACTED 1.00]
- **Vision Handwriting Analysis Pipeline (CV Preprocessing -> OCR/Stroke Tracking -> Multimodal LLM Feedback)** — backend_system_api_vision_py, backend_system_mediapipe_hands, backend_system_opencv, backend_system_tesseract_ocr, backend_system_groq_llama_4_scout [EXTRACTED 1.00]
- **Cultural Discovery ReAct Agent Flow (Chat -> LangGraph Loop -> Tools -> Festival Content & Score Updates)** — backend_system_api_culture_py, backend_system_langgraph_react_agent, backend_system_agent_node, backend_system_action_node, backend_system_festival_knowledge_base, backend_system_gamification [EXTRACTED 1.00]
- **LLM & agent orchestration stack (Gemini, Groq, LangChain/LangGraph)** — backend_requirements_google_gemini, backend_requirements_google_generativeai, backend_requirements_langchain, backend_requirements_langchain_core, backend_requirements_langchain_google_genai, backend_requirements_langchain_groq, backend_requirements_langgraph, backend_requirements_groq [INFERRED 0.85]
- **Speech & voice services stack (STT/TTS)** — backend_requirements_deepgram_sdk, backend_requirements_elevenlabs, backend_requirements_gtts [INFERRED 0.85]
- **Image processing stack (OpenCV, Pillow, NumPy)** — backend_requirements_opencv_python_headless, backend_requirements_pillow, backend_requirements_numpy [INFERRED 0.85]
- **South Indian Festival Imagery Family** — frontend_public_images_culture_bonalu_festival_bonalu_festival_pot_procession, frontend_public_images_culture_pongal_pot_pongal_harvest_pot_boiling_over, frontend_public_images_culture_ugadi_pachadi_ugadi_pachadi_ritual_dish_with_ghee_lamp, frontend_public_images_culture_onam_pookalam_onam_pookalam_floral_carpet, frontend_public_images_culture_thaipusam_kavadi_thaipusam_kavadi_procession, frontend_public_images_culture_sankranti_kites_riverside_pilgrimage_crowd_at_dusk [INFERRED 0.75]
- **Sacred Lamp and Light Imagery Family** — frontend_public_images_culture_deepam_diya_diya_oil_lamps_on_rangoli, frontend_public_images_culture_diwali_lights_diwali_rangoli_with_lit_oil_lamps, frontend_public_images_culture_karthigai_deepam_karthigai_deepam_lamps_on_floral_kolam, frontend_public_images_culture_ugadi_pachadi_ugadi_pachadi_ritual_dish_with_ghee_lamp [INFERRED 0.75]
- **Deity, Bronze and Temple Art Imagery Family** — frontend_public_images_culture_brihadeeswara_temple_brihadeeswara_temple_at_twilight, frontend_public_images_culture_mahabalipuram_shore_mahabalipuram_shore_temple_by_the_sea, frontend_public_images_culture_lord_shiva_nataraja_bronze_statue_of_lord_shiva, frontend_public_images_culture_rajaraja_chola_rajaraja_chola_bronze_bust, frontend_public_images_culture_lord_murugan_golden_murugan_statue_at_batu_caves, frontend_public_images_culture_lord_ganesha_lord_ganesha_riding_mooshak_print, frontend_public_images_culture_goddess_lakshmi_goddess_lakshmi_painting_on_lotus [INFERRED 0.75]
- **Ammachi App Icon Variant Family (Favicon, Apple Touch and PWA Sizes Rendered from the Same Mascot Asset)** — frontend_public_apple_touch_icon_ammachi_apple_touch_icon, frontend_public_favicon_48x48_ammachi_favicon_48, frontend_public_favicon_ammachi_favicon_face, frontend_public_pwa_192x192_ammachi_pwa_icon_192, frontend_public_pwa_512x512_ammachi_pwa_icon_512, frontend_public_pwa_maskable_512x512_ammachi_maskable_pwa_icon_512, concept_ammachi_app_icon [INFERRED 0.75]
- **Tamil Learning Module Icon Set (Challenge, Culture, Handwriting and Voice Tiles in the Same Rounded-Gradient Style)** — frontend_public_icons_challenge_challenge_module_icon, frontend_public_icons_culture_culture_module_icon, frontend_public_icons_handwriting_handwriting_module_icon, frontend_public_icons_voice_voice_speaking_module_icon, concept_warm_amber_child_friendly_theme [INFERRED 0.75]
- **Ammachi App Brand Identity (Mascot Logo Themed Across App Icons, Module Icons and UI Screens)** — frontend_public_logo_ammachi_ammachi_mascot_logo, concept_ammachi_grandmother_mascot_branding, concept_warm_amber_child_friendly_theme, frontend_public_screenshots_home_home_dashboard_screenshot, frontend_public_screenshots_culture_culture_module_screen_screenshot [INFERRED 0.75]

## Communities (49 total, 18 thin omitted)

### Community 0 - "App Shell & Routing"
Cohesion: 0.06
Nodes (73): App(), ProtectedRoute(), AmmachiMascot(), triggerCelebration(), LoadingScreen(), SpeechBubble(), BottomNav(), Layout() (+65 more)

### Community 1 - "Learn API (Duolingo Pack)"
Cohesion: 0.07
Nodes (62): check_answer(), claim_quest(), complete_attempt(), _correct_answer(), _ensure_seed_path(), _evaluate_answer(), get_hud(), get_leaderboard() (+54 more)

### Community 2 - "Streamlit Legacy App"
Cohesion: 0.05
Nodes (35): main(), login_page(), culture_node(), send_to_agent(), vision_node(), voice_node(), render_google_login(), amma_speak() (+27 more)

### Community 3 - "Handwriting API"
Cohesion: 0.06
Nodes (10): evaluate_handwriting_endpoint(), get_letters(), ocr_image(), BodhanOCRService, HandwritingPreprocessor, _create_result(), evaluate_handwriting(), is_valid_character() (+2 more)

### Community 4 - "Challenge API"
Cohesion: 0.12
Nodes (31): api_create_challenge(), api_get_challenge(), api_get_question(), api_get_results(), api_join_challenge(), api_start_challenge(), api_submit_answer(), build_challenge_response() (+23 more)

### Community 5 - "Frontend Build & Deps"
Cohesion: 0.05
Nodes (38): dependencies, axios, canvas-confetti, clsx, lucide-react, react, react-dom, react-router-dom (+30 more)

### Community 6 - "Auth API"
Cohesion: 0.16
Nodes (18): create_access_token(), decode_access_token(), get_auth_config(), get_google_client_id(), get_me(), get_secret_key(), google_auth(), login() (+10 more)

### Community 7 - "Database & CRUD"
Cohesion: 0.21
Nodes (17): create_user(), get_user_by_google_id(), get_user_by_username(), get_user_handwriting_stats(), get_user_progress_summary(), link_google_id_to_user(), log_learning_progress(), log_learning_session() (+9 more)

### Community 8 - "Culture API"
Cohesion: 0.18
Nodes (13): culture_chat(), get_festival_quiz(), get_festival_videos(), get_festivals(), submit_quiz_answer(), CultureChatRequest, CultureChatResponse, FestivalInfo (+5 more)

### Community 9 - "Shared Auth Dependency"
Cohesion: 0.13
Nodes (7): get_current_user(), get_stamps(), get_user_profile(), update_language(), health_check(), lifespan(), read_root()

### Community 10 - "Culture Agent Graph (LangGraph)"
Cohesion: 0.16
Nodes (17): Action Node (ToolNode Execution), Agent Node (LLM Reasoning + Tool Binding), backend/api/auth.py (Auth Router), backend/api/culture.py (Culture Router), backend/database.py (SQLite Database Layer), DuckDuckGo Search (Video & Image), Festival Knowledge Base (Indian Festivals), Gamification (Points & Cultural Stamps) (+9 more)

### Community 11 - "AI SDK Dependencies"
Cohesion: 0.12
Nodes (18): duckduckgo-search 8.1.1 (web search), Google Gemini (LLM API), google-generativeai 0.8.6 (Gemini client SDK), Groq 0.37.1 (LLM inference API), LangChain 1.4.3, langchain-core 1.6.7, langchain-google-genai 4.4.0, langchain-groq 1.1.3 (+10 more)

### Community 12 - "LangGraph Messaging Types"
Cohesion: 0.20
Nodes (8): AIMessage, BaseMessage, HumanMessage, run_culture_chat(), scrub_response_text(), SystemMessage, invoke_direct_llm(), is_current_affairs_query()

### Community 13 - "Learn Content Seed"
Cohesion: 0.35
Nodes (10): build_seed_exercises(), _corpus_for(), _default_units(), _exercise_listen(), _exercise_match(), _exercise_multiple_choice(), _exercise_speak(), _exercise_translate() (+2 more)

### Community 14 - "Ammachi Brand Assets"
Cohesion: 0.21
Nodes (16): Ammachi App Icon (Canonical Brand App Icon Asset), Ammachi Grandmother Mascot Branding, Warm Amber Child-Friendly Theme, Ammachi Apple Touch App Icon (Grandmother Mascot on Amber Circle), Ammachi 48x48 Favicon (Small Grandmother Mascot Icon), Ammachi Vector Favicon (Simplified Grandmother Face with Spectacles, Bindi and Saree Motif), Challenge Module Icon (Trophy with Star on Amber Gradient Tile), Culture Module Icon (Flame Diya Lamp over Dished Plate on Magenta Gradient Tile) (+8 more)

### Community 15 - "Avatar Storage"
Cohesion: 0.23
Nodes (7): upload_avatar(), _config(), delete_file(), _ensure_bucket(), _headers(), is_supabase_storage_enabled(), upload_file()

### Community 16 - "DB Connection & Init"
Cohesion: 0.26
Nodes (6): init_db(), _init_postgres(), hash_password(), HandwritingAttempt, Letter, seed()

### Community 17 - "PWA Install Flow"
Cohesion: 0.29
Nodes (13): InstallPrompt(), InstructionsSheet(), readDismissed(), Steps(), useInstallState(), canPromptInstall(), captureInstallPrompt(), getPlatform() (+5 more)

### Community 18 - "Patience & Gemini Services"
Cohesion: 0.20
Nodes (4): process_child_speech_and_respond(), evaluate_handwriting_with_gemini(), get_llm_client(), get_cultural_images_for_query()

### Community 19 - "Culture Service"
Cohesion: 0.21
Nodes (5): get_festival_by_id(), get_festival_quiz(), get_festivals_for_language(), get_festival_youtube_videos(), search_youtube_api()

### Community 20 - "Vision Stack"
Cohesion: 0.18
Nodes (12): backend/api/vision.py (Vision Router), Groq Llama-4 Scout (Multimodal LLM), MediaPipe Hands (Hand Landmark Detection), OpenCV, Tesseract OCR (Tamil + English), Vision Node (Handwriting Analysis & Stroke-Order Tutoring), AI Handwriting Tutor (Bodhan IndicOCR + CV), backend/api/handwriting.py (Handwriting Router) (+4 more)

### Community 21 - "Culture Image Themes"
Cohesion: 0.22
Nodes (14): Chola Bronze Casting Tradition, Devotional Festival Procession, Hindu Deity Iconography, South Indian Heritage Temple Architecture, Bonalu Festival Pot Procession Photo, Brihadeeswara Temple at Twilight, Goddess Lakshmi on Lotus Painting, Lord Ganesha Riding Mooshak Vintage Print (+6 more)

### Community 22 - "Backend Docs & Persona"
Cohesion: 0.22
Nodes (11): Ammachi AI Backend System Document, Cultural Discovery Module (Festival-Based Gamified Learning), Ammachi AI Language Learning Platform, Ammachi Grandmother Persona, backend/api/challenge.py (Challenge Router: WebSocket + REST), Challenge-a-Friend (10-Question Gamified Match), backend/services/challenge_ai.py (Gemini Challenge Generation), backend/services/gemini_service.py (Gemini Multimodal Vision & LLM) (+3 more)

### Community 23 - "Diagnostics & Migration"
Cohesion: 0.27
Nodes (5): convert_row(), main(), parse_args(), to_datetime(), to_json()

### Community 24 - "Backend Architecture Concepts"
Cohesion: 0.27
Nodes (11): AI Models, API Gateway, Backend Architecture Document (Ammachi AI), Data Processing Service, Docker, End-to-End Backend Data Flow, Express.js, Flask (+3 more)

### Community 25 - "Auth Schemas"
Cohesion: 0.25
Nodes (6): GoogleAuthRequest, LoginRequest, LoginResponse, SignupRequest, VoiceResponse, HandwritingEvaluationResponse

### Community 26 - "Voice Pipeline"
Cohesion: 0.36
Nodes (9): backend/api/voice.py (Voice Router), Groq Whisper Large V3 (STT), gTTS (Google Text-to-Speech), Patience Agent (LLM Stutter Cleaning), Voice Node (Pronunciation Practice & Conversational Fluency), AI Voice Agent (STT + Patience Denoising + TTS), Deepgram Nova-2 STT, ElevenLabs TTS (Emotive Grandmother Voice, Dorothy) (+1 more)

### Community 28 - "Festival Imagery"
Cohesion: 0.47
Nodes (9): Festival Floor Art Rangoli Kolam Pookalam, Festival Ritual Food Offering, Lamp Flame Symbolism, Diya Oil Lamps on Rangoli, Diwali Rangoli with Lit Oil Lamps, Karthigai Deepam Lamps on Floral Kolam, Onam Pookalam Floral Carpet, Pongal Harvest Pot Boiling Over (+1 more)

### Community 29 - "Core Python Deps"
Cohesion: 0.29
Nodes (7): Requests (HTTP client), FastAPI 0.142.2, Pydantic 2.13.5, PyJWT 2.15.1 (JSON Web Tokens), python-multipart 0.0.32, Requests 2.34.2 (HTTP client), Uvicorn 0.54.0 (ASGI server)

### Community 30 - "Legacy Stack Map"
Cohesion: 0.38
Nodes (6): ammachi/app.py (Streamlit Main App), ammachi/util.py (Frontend Helpers & API_URL Config), FastAPI Backend (RESTful API), Streamlit Frontend, backend/database/connection.py (SQLAlchemy Engine & SQLite Fallback), PostgreSQL + SQLAlchemy 2.0 + Psycopg 3 (SQLite Fallback)

### Community 32 - "Gamification Economy"
Cohesion: 0.38
Nodes (7): Groq Llama 3.3 70B Versatile, backend/api/learn.py (Learning Path Router: XP/Hearts/Streaks/Quests/Leagues/Shop), backend/api/user.py (User Progress Router), backend/services/gamification.py (XP/Gems/Hearts/Streak/Quest/League Economy), Google Gemini (gemini-1.5-flash / gemini-2.0-flash), backend/services/learn_content.py (Seed Corpus + AI Exercise Generation), Duolingo-Style Learning Path & Gamification

## Ambiguous Edges - Review These
- `Microservices Architecture` → `FastAPI Backend (RESTful API)`  [AMBIGUOUS]
  BACKEND_ARCHITECTURE.md · relation: semantically_similar_to
- `User Service` → `backend/api/auth.py (Auth Router)`  [AMBIGUOUS]
  BACKEND_ARCHITECTURE.md · relation: semantically_similar_to
- `API Gateway` → `FastAPI Backend (RESTful API)`  [AMBIGUOUS]
  BACKEND_ARCHITECTURE.md · relation: semantically_similar_to
- `Ammachi AI Backend System Document` → `Deepgram Nova-2 STT`  [AMBIGUOUS]
  BACKEND_SYSTEM.md · relation: references
- `Streamlit` → `streamlit-audio-recorder (commented note)`  [AMBIGUOUS]
  ammachi/requirements.txt · relation: conceptually_related_to
- `Bonalu Festival Pot Procession Photo` → `Riverside Pilgrimage Crowd at Dusk (file named Sankranti Kites, no kites visible)`  [AMBIGUOUS]
  frontend/public/images/culture/sankranti_kites.jpg · relation: conceptually_related_to
- `Riverside Pilgrimage Crowd at Dusk (file named Sankranti Kites, no kites visible)` → `Devotional Festival Procession`  [AMBIGUOUS]
  frontend/public/images/culture/sankranti_kites.jpg · relation: conceptually_related_to

## Knowledge Gaps
- **47 isolated node(s):** `clsx`, `tailwind-merge`, `@types/react`, `@types/react-dom`, `autoprefixer` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 214 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HandwritingPreprocessor` connect `Handwriting API` to `Shared Auth Dependency`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **What connects `clsx`, `tailwind-merge`, `@types/react` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `App Shell & Routing` be split into smaller, more focused modules?**
  _Cohesion score 0.06081754735792622 - nodes in this community are weakly interconnected._
- **Why does `evaluate_handwriting()` connect `Handwriting API` to `DB Connection & Init`, `Shared Auth Dependency`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Should `Learn API (Duolingo Pack)` be split into smaller, more focused modules?**
  _Cohesion score 0.06730506155950752 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Microservices Architecture` and `FastAPI Backend (RESTful API)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `User Service` and `backend/api/auth.py (Auth Router)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._