import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ammachi.main")

from database.connection import init_db
from api import auth, voice, culture, user, challenge, handwriting

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    logger.info("Initializing Ammachi Backend and Database...")
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize database on startup: %s", e)
    yield
    # Shutdown
    logger.info("Shutting down Ammachi Backend.")

app = FastAPI(
    title="Ammachi AI – Native Language Learning Platform API",
    description="AI-powered multimodal native language tutor backend with PaddleOCR, Gemini, Deepgram, and LangGraph.",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
cors_origins_env = os.getenv("CORS_ORIGINS")

if cors_origins_env:
    origins = [orig.strip() for orig in cors_origins_env.split(",") if orig.strip()]
else:
    origins = [
        frontend_url,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8501", # Legacy Streamlit port
    ]

# Remove duplicates
origins = list(set(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads/profiles", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled Exception at %s: %s", request.url.path, exc, exc_info=True)
    # 500s bypass CORSMiddleware, so add the header here; otherwise browsers report them as CORS errors
    headers = {}
    origin = request.headers.get("origin")
    if origin in origins:
        headers = {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true", "Vary": "Origin"}
    return JSONResponse(
        status_code=500,
        content={"detail": "Aiyayo! An unexpected error occurred. Please try again."},
        headers=headers
    )

# Include Routers
app.include_router(auth.router, tags=["Authentication"])

app.include_router(voice.router, prefix="/voice", tags=["Voice / Pronunciation Agent"])
app.include_router(challenge.router, prefix="/challenges", tags=["Friend vs Friend Challenge"])
app.include_router(culture.router, prefix="/culture", tags=["Culture / Discovery Agent"])
app.include_router(user.router, prefix="/user", tags=["User Profile & Progress"])
app.include_router(handwriting.router, prefix="/handwriting", tags=["Handwriting Assessment"])

@app.get("/")
def read_root():
    return {
        "app": "Ammachi AI Native Language Tutor",
        "status": "online",
        "version": "2.0.0",
        "modules": ["Voice Agent (Deepgram + ElevenLabs)", "Cultural Discovery (LangGraph)"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ocr", tags=["Handwriting Assessment"])
async def ocr_image(file: UploadFile = File(...), language: str = Form("Tamil")):
    """Run Bodhan IndicOCR on an uploaded image and return the recognized text."""
    from services.bodhan_ocr import BodhanOCRService
    from services.handwriting_preprocessor import HandwritingPreprocessor

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large. Maximum size is 5MB.")

    try:
        image_bytes = HandwritingPreprocessor().preprocess_light(contents)
    except Exception:
        image_bytes = contents

    ocr_service = BodhanOCRService()
    provider = "bodhan" if ocr_service.api_key and ocr_service.endpoint else "groq"
    try:
        text, confidence = ocr_service.recognize_character(image_bytes, language)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "success": text is not None,
        "text": text,
        "confidence": confidence,
        "language": language,
        "provider": provider,
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
