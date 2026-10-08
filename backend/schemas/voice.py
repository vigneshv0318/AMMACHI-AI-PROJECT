from pydantic import BaseModel
from typing import Optional, List

class VoiceTranslateRequest(BaseModel):
    english_text: str
    language: Optional[str] = "Tamil"

class VoiceTranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    pronunciation_guide: str
    language: str
    language_code: str = "ta"

class VoiceAnalyzeResponse(BaseModel):
    expected_text: str
    detected_text: str
    recognition_status: str  # CORRECT, NEEDS_PRACTICE, UNCERTAIN
    score: int
    confidence: float
    feedback: str
    mistake_explanation: Optional[str] = ""
    needs_retry: bool = False
    points_awarded: int = 0
    total_points: int = 0
    # Backward compatibility fields
    transcription: Optional[str] = ""
    cleaned_text: Optional[str] = ""
    is_correct: Optional[bool] = True

class TextToSpeechRequest(BaseModel):
    text: str
    language: Optional[str] = "Tamil"
    speed: Optional[float] = 1.0

