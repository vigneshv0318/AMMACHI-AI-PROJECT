import os
import io
import re
import json
import logging
import difflib
import requests
from typing import Dict, Any, Optional, Tuple, List
from fastapi.responses import Response

from services.gemini_service import invoke_direct_llm

logger = logging.getLogger("ammachi.voice")

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_LABS_API")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "ThT5KcBeYPX3keUQqHPh")

LANG_CODE_MAP = {
    "tamil": "ta",
    "telugu": "te",
    "hindi": "hi",
    "english": "en"
}

OFFLINE_TRANSLATION_FALLBACKS = {
    "tamil": {
        "hello": ("வணக்கம்", "Vanakkam"),
        "thank you": ("நன்றி", "Nandri"),
        "how are you": ("எப்படி இருக்கிறீர்கள்?", "Eppadi irukkireergal?"),
        "good morning": ("காலை வணக்கம்", "Kaalai Vanakkam"),
        "i love learning": ("நான் கற்றுக்கொள்வதை விரும்புகிறேன்", "Naan katrukolvadhai virumbugiren")
    },
    "telugu": {
        "hello": ("నమస్కారం", "Namaskaram"),
        "thank you": ("ధన్యవాదాలు", "Dhanyavadalu"),
        "how are you": ("మీరు ఎలా ఉన్నారు?", "Meeru ela unnaru?"),
        "good morning": ("శుభోదయం", "Subhodayam")
    },
    "hindi": {
        "hello": ("नमस्ते", "Namaste"),
        "thank you": ("धन्यवाद", "Dhanyavaad"),
        "how are you": ("आप कैसे हैं?", "Aap kaise hain?"),
        "good morning": ("सुप्रभात", "Suprabhat")
    }
}

def translate_english_to_native(english_text: str, language: str = "Tamil") -> Dict[str, Any]:
    """
    Translates English input into native script (Tamil, Telugu, Hindi)
    and generates a child-friendly English phonetic pronunciation guide.
    """
    lang_clean = (language or "Tamil").lower()
    target_code = LANG_CODE_MAP.get(lang_clean, "ta")
    text_clean = english_text.strip()

    system_prompt = (
        f"You are an expert native language tutor translating English for children learning {language}.\n"
        f"Translate the English text into native {language} script and provide an easy, child-friendly English phonetic pronunciation guide.\n"
        f"Return ONLY a raw JSON object with these exact keys:\n"
        f"{{\n"
        f'  "translated_text": "Native {language} script translation",\n'
        f'  "pronunciation_guide": "Easy English phonetic transliteration (e.g. Vanakkam Kanna)"\n'
        f"}}\n"
        f"Do NOT include markdown backticks or extra commentary."
    )

    user_prompt = f'Translate this text into {language}: "{text_clean}"'

    try:
        raw_res = invoke_direct_llm(system_prompt=system_prompt, user_message=user_prompt)
        if raw_res:
            json_str = raw_res.strip()
            if json_str.startswith("```"):
                json_str = re.sub(r"^```(?:json)?\n?", "", json_str)
                json_str = re.sub(r"\n?```$", "", json_str)
            
            data = json.loads(json_str)
            if data.get("translated_text") and data.get("pronunciation_guide"):
                return {
                    "original_text": text_clean,
                    "translated_text": data["translated_text"].strip(),
                    "pronunciation_guide": data["pronunciation_guide"].strip(),
                    "language": language,
                    "language_code": target_code
                }
    except Exception as e:
        logger.warning("LLM translation failed: %s. Checking offline fallbacks.", e)

    fallback_dict = OFFLINE_TRANSLATION_FALLBACKS.get(lang_clean, {})
    lowered = text_clean.lower()
    for key, (native, guide) in fallback_dict.items():
        if key in lowered:
            return {
                "original_text": text_clean,
                "translated_text": native,
                "pronunciation_guide": guide,
                "language": language,
                "language_code": target_code
            }

    return {
        "original_text": text_clean,
        "translated_text": text_clean,
        "pronunciation_guide": text_clean,
        "language": language,
        "language_code": target_code
    }


def transcribe_audio_detailed(audio_path: str, language: str = "Tamil") -> Tuple[str, float, List[Dict[str, Any]]]:
    """
    Transcribes audio via direct Deepgram HTTP REST API or Groq Whisper.
    Returns (raw_transcript, overall_confidence, list_of_words).
    """
    lang_clean = (language or "Tamil").lower()
    target_lang = LANG_CODE_MAP.get(lang_clean, "ta")

    # 1. Direct Deepgram HTTP REST API (Robust across all SDK versions)
    if DEEPGRAM_API_KEY and not DEEPGRAM_API_KEY.startswith("your_"):
        for model in ["nova-3", "general"]:
            try:
                url = f"https://api.deepgram.com/v1/listen?model={model}&language={target_lang}&smart_format=true&punctuate=true"
                headers = {
                    "Authorization": f"Token {DEEPGRAM_API_KEY}",
                    "Content-Type": "audio/wav"
                }
                with open(audio_path, "rb") as f:
                    audio_data = f.read()

                res = requests.post(url, headers=headers, data=audio_data, timeout=12)
                if res.status_code == 200:
                    dg_json = res.json()
                    channels = dg_json.get("results", {}).get("channels", [])
                    if channels:
                        alt = channels[0].get("alternatives", [{}])[0]
                        transcript = alt.get("transcript", "").strip()
                        confidence = float(alt.get("confidence", 0.88) or 0.88)
                        words_data = alt.get("words", [])
                        if transcript:
                            logger.info("Deepgram REST transcribed [%s/%s, conf=%.2f]: %s", model, target_lang, confidence, transcript)
                            return transcript, confidence, words_data
            except Exception as dg_err:
                logger.warning("Deepgram REST call (%s/%s) error: %s", model, target_lang, dg_err)

    # 2. Groq Whisper REST / SDK Fallback
    if GROQ_API_KEY and not GROQ_API_KEY.startswith("your_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            with open(audio_path, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    file=(audio_path, f.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )
            raw_text = str(transcription).strip()
            if raw_text:
                logger.info("Groq Whisper transcribed: %s", raw_text)
                return raw_text, 0.85, []
        except Exception as groq_err:
            logger.warning("Groq Whisper fallback failed: %s", groq_err)

    return "", 0.0, []


def determine_recognition_status(
    expected_native: str,
    pronunciation_guide: str,
    original_english: str,
    detected_text: str,
    confidence: float = 0.85
) -> Tuple[str, int, str, bool]:
    """
    MULTI-SCRIPT & PHONETIC RECOGNITION MATCHING ENGINE:
    Evaluates detected speech against:
    1. Native script (e.g. "வணக்கம்")
    2. English Phonetic Guide (e.g. "Vanakkam")
    3. Original English phrase (e.g. "Hello")

    Returns (recognition_status, score, mistake_explanation, needs_retry).
    States: CORRECT, NEEDS_PRACTICE, UNCERTAIN.
    """
    def clean(s: str) -> str:
        if not s: return ""
        s = re.sub(r'[^\w\s]', '', s.lower())
        return " ".join(s.split()).strip()

    det_clean = clean(detected_text)

    # 1. Unclear / Empty Audio -> UNCERTAIN
    if not det_clean or len(det_clean) < 1 or (confidence > 0.0 and confidence < 0.35):
        return (
            "UNCERTAIN",
            30,
            "Speech was not clearly heard. Please record in a quiet room and speak close to the microphone.",
            True
        )

    targets = [
        clean(expected_native),
        clean(pronunciation_guide),
        clean(original_english)
    ]
    targets = [t for t in targets if t]

    best_score = 0.0
    best_target = targets[0] if targets else ""

    for target in targets:
        # String similarity ratio
        ratio = difflib.SequenceMatcher(None, target, det_clean).ratio() * 100.0
        
        # Word overlap ratio
        t_words = target.split()
        d_words = det_clean.split()
        matched = [w for w in t_words if w in d_words or any(difflib.SequenceMatcher(None, w, dw).ratio() > 0.75 for dw in d_words)]
        overlap = (len(matched) / max(len(t_words), 1)) * 100.0

        score = (ratio * 0.5) + (overlap * 0.5)
        if score > best_score:
            best_score = score
            best_target = target

    # Direct substring/exact match bonus
    for target in targets:
        if target in det_clean or det_clean in target:
            best_score = max(best_score, 88.0)

    # Decision Logic
    if best_score >= 68.0:
        final_score = min(100, max(90, int(best_score + 10)))
        return (
            "CORRECT",
            final_score,
            "Clear and accurate native pronunciation!",
            False
        )

    elif best_score >= 30.0:
        exp_words = best_target.split()
        det_words = det_clean.split()
        missing = [w for w in exp_words if w not in det_words]
        
        explanation = ""
        if missing:
            explanation = f"Try focusing on pronouncing the word: '{missing[0]}'"
        else:
            explanation = "Speak clearly and practice each syllable."

        final_score = max(55, min(86, int(best_score + 15)))
        return (
            "NEEDS_PRACTICE",
            final_score,
            explanation,
            False
        )

    else:
        return (
            "UNCERTAIN",
            35,
            "The speech sounded different from the target sentence. Try speaking slowly and clearly.",
            True
        )


def generate_tutor_feedback(
    status: str,
    expected_text: str,
    detected_text: str,
    mistake_explanation: str,
    language: str = "Tamil"
) -> str:
    """
    Generates warm, encouraging feedback using Gemini strictly bound to the determined backend status.
    Gemini is NOT allowed to change the status decision.
    """
    system_prompt = (
        f"You are a warm, encouraging native language tutor helping a child learn {language} pronunciation.\n"
        f"The backend speech analyzer has ALREADY determined the result: status={status}.\n"
        f"YOUR INSTRUCTIONS STRICTLY BASED ON STATUS:\n"
        f"- CORRECT: Praise the child enthusiastically! Praise their clear native pronunciation and invite them to keep speaking.\n"
        f"- NEEDS_PRACTICE: Provide gentle, loving guidance. Mention what to practice: '{mistake_explanation}'. Encourage them to listen again and try.\n"
        f"- UNCERTAIN: Do NOT tell the child they were wrong. Gently explain that the mic didn't catch their voice clearly, and invite them to try again in a quiet spot.\n"
        f"Keep the feedback warm, short (1-2 sentences), and encouraging. Use friendly emojis."
    )

    user_prompt = (
        f"Status: {status}\n"
        f"Expected Sentence: {expected_text}\n"
        f"Child Detected Speech: {detected_text}\n"
        f"Guidance: {mistake_explanation}"
    )

    try:
        feedback = invoke_direct_llm(system_prompt=system_prompt, user_message=user_prompt)
        if feedback and len(feedback.strip()) > 5:
            return feedback.strip()
    except Exception as e:
        logger.warning("Feedback LLM generation error: %s", e)

    if status == "CORRECT":
        return "Sabash Kanna! Fantastic job! Your pronunciation was super clear and accurate! 🌟"
    elif status == "NEEDS_PRACTICE":
        return f"Good effort! {mistake_explanation}. Listen to the audio again and give it another try! 💪"
    else:
        return "Aiyayo Kanna! I couldn't hear your sweet voice clearly. Please check your mic and speak again in a quiet room! 🎤"


def clean_text_for_tts(text: str) -> str:
    """Removes markdown symbols, brackets, emojis, and unwanted formatting artifacts."""
    text = re.sub(r'[\*_`#~]', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = text.replace(':', '. ').replace('--', ', ')
    return " ".join(text.split()).strip()


def is_indic_script(text: str) -> bool:
    """Checks if text contains native Indic script characters (Tamil, Telugu, Devanagari)."""
    for char in text:
        code = ord(char)
        if (0x0B80 <= code <= 0x0BFF) or (0x0C00 <= code <= 0x0C7F) or (0x0900 <= code <= 0x097F):
            return True
    return False


def generate_tts_stream(text: str, language: str = "Tamil") -> Response:
    """
    Generates audio for native text using ElevenLabs TTS (model: eleven_multilingual_v2).
    Dynamically loads ELEVENLABS_VOICE_ID and ELEVENLABS_API_KEY from environment variables.
    Falls back to gTTS if ElevenLabs key is missing or fails.
    """
    cleaned_text = clean_text_for_tts(text)
    if not cleaned_text:
        cleaned_text = "Sabash Kanna, well done!"

    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_LABS_API") or ELEVENLABS_API_KEY
    voice_id = os.getenv("ELEVENLABS_VOICE_ID") or ELEVENLABS_VOICE_ID or "EXAVITQu4vr4xnSDxMaL"

    if elevenlabs_key and not elevenlabs_key.startswith("your_"):
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=elevenlabs_key)

            if hasattr(client, "text_to_speech"):
                audio_stream = client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=cleaned_text,
                    model_id="eleven_multilingual_v2"
                )
            else:
                audio_stream = client.generate(
                    text=cleaned_text,
                    voice=voice_id,
                    model="eleven_multilingual_v2"
                )

            audio_bytes = b"".join(audio_stream)
            if audio_bytes and len(audio_bytes) > 500:
                logger.info("ElevenLabs TTS generated (%s bytes) with voice_id: %s", len(audio_bytes), voice_id)
                return Response(content=audio_bytes, media_type="audio/mpeg")
        except Exception as el_err:
            logger.warning("ElevenLabs TTS note: %s. Falling back to gTTS.", el_err)

    try:
        from gtts import gTTS
        lang_code = LANG_CODE_MAP.get((language or "Tamil").lower(), "ta")
        tts = gTTS(text=cleaned_text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return Response(content=fp.getvalue(), media_type="audio/mpeg")
    except Exception as gtts_err:
        logger.error("Final gTTS fallback error: %s", gtts_err)

    return Response(content=b"", media_type="audio/mpeg")
