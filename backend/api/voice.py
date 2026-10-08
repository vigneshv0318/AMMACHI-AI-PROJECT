import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException

from database.connection import get_db
from database import crud
from api.auth import get_current_user
from schemas.voice import (
    VoiceTranslateRequest,
    VoiceTranslateResponse,
    VoiceAnalyzeResponse,
    TextToSpeechRequest
)
from services.voice_service import (
    translate_english_to_native,
    transcribe_audio_detailed,
    determine_recognition_status,
    generate_tutor_feedback,
    generate_tts_stream
)

logger = logging.getLogger("ammachi.voice_api")

router = APIRouter()

@router.post("/translate", response_model=VoiceTranslateResponse)
def translate_text(request: VoiceTranslateRequest):
    """
    Translates an English sentence into the selected native language (Tamil, Telugu, Hindi)
    and returns a child-friendly English phonetic pronunciation guide.
    """
    if not request.english_text or not request.english_text.strip():
        raise HTTPException(status_code=400, detail="English text cannot be empty.")

    res = translate_english_to_native(request.english_text, request.language or "Tamil")
    return VoiceTranslateResponse(**res)

@router.post("/analyze", response_model=VoiceAnalyzeResponse)
def analyze_voice(
    file: UploadFile = File(...),
    expected_text: str = Form(""),
    pronunciation_guide: str = Form(""),
    original_english: str = Form(""),
    language: str = Form("Tamil"),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Analyzes the child's recorded native speech against the expected translated text:
    1. Transcribes audio via Deepgram STT (nova-3/general) / Groq Whisper
    2. Multi-script matcher classifies state: CORRECT (90-100), NEEDS_PRACTICE, or UNCERTAIN
    3. Prompts Gemini to generate warm, child-friendly feedback matching the status
    4. Logs learning progress and awards points in database
    """
    suffix = ".wav" if not file.filename or not file.filename.endswith(".webm") else ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        audio_path = tmp.name

    try:
        # 1. Detailed STT Transcription
        detected_text, confidence, words_data = transcribe_audio_detailed(audio_path, language=language)

        # 2. Multi-script & Phonetic Transliteration State Classification
        status, score, mistake_explanation, needs_retry = determine_recognition_status(
            expected_native=expected_text,
            pronunciation_guide=pronunciation_guide,
            original_english=original_english,
            detected_text=detected_text,
            confidence=confidence
        )

        # 3. Gemini Feedback Generation matching backend status
        feedback = generate_tutor_feedback(
            status=status,
            expected_text=expected_text,
            detected_text=detected_text,
            mistake_explanation=mistake_explanation,
            language=language
        )

        # 4. Award Points & Log in DB
        points_to_award = 10 if status == "CORRECT" else (5 if status == "NEEDS_PRACTICE" else 0)
        crud.log_learning_progress(
            db=db,
            user_id=current_user.id,
            module="voice",
            activity=f"Pronounced ({status}): '{expected_text[:25]}'",
            score=score,
            language=language
        )
        updated = crud.update_user_points_and_stamp(db, current_user.username, points_to_add=points_to_award)

        return VoiceAnalyzeResponse(
            expected_text=expected_text,
            detected_text=detected_text,
            recognition_status=status,
            score=score,
            confidence=round(confidence, 2),
            feedback=feedback,
            mistake_explanation=mistake_explanation,
            needs_retry=needs_retry,
            points_awarded=points_to_award,
            total_points=updated.get("points", current_user.points or 0),
            transcription=detected_text,
            cleaned_text=detected_text,
            is_correct=(status == "CORRECT")
        )

    except Exception as e:
        logger.error("Voice analysis endpoint error: %s", e)
        return VoiceAnalyzeResponse(
            expected_text=expected_text,
            detected_text="Audio received",
            recognition_status="UNCERTAIN",
            score=30,
            confidence=0.0,
            feedback=f"Aiyayo Kanna! My ears are having trouble hearing right now. Please press the mic and try again in a quiet room!",
            mistake_explanation="Audio connection check required.",
            needs_retry=True,
            points_awarded=0,
            total_points=current_user.points or 0,
            transcription="Audio received",
            cleaned_text="Audio received",
            is_correct=False
        )
    finally:
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception:
                pass

@router.post("/speak")
def speak_text(request: TextToSpeechRequest):
    """
    Streams audio synthesizing native text using ElevenLabs TTS (eleven_multilingual_v2).
    """
    return generate_tts_stream(request.text, language=request.language or "Tamil")

@router.get("/speak-get")
def speak_text_get(text: str, language: str = "Tamil"):
    """
    HTTP GET endpoint for playing native audio in browser <audio> tags or AudioContext.
    """
    return generate_tts_stream(text, language=language)