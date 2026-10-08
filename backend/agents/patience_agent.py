import os
import logging
from typing import Tuple
from services.gemini_service import get_llm_client

logger = logging.getLogger("ammachi.patience")

def process_child_speech_and_respond(
    raw_transcript: str,
    language: str = "Tamil"
) -> Tuple[str, str, int]:
    """
    Patience Agent for NRI children:
    1. Denoises stutters, pauses, filler words ('A... A... Amma' -> 'Amma')
    2. Generates a warm, patient, loving Ammachi reply with subtle recastings.
    3. Calculates pronunciation/fluency score.
    Returns: (cleaned_transcript, ammachi_feedback, score)
    """
    if not raw_transcript or raw_transcript.strip() == "":
        return (
            "...",
            f"Ammachi couldn't hear clearly, Kanna. Please press the mic and speak once more!",
            50
        )

    llm = get_llm_client()
    
    if llm:
        try:
            prompt = f"""You are 'Ammachi', a loving and patient grandmother tutoring an NRI child in {language}.

Child's raw speech transcription: "{raw_transcript}"

Tasks:
1. Clean the text by removing repeated stutter syllables (e.g. "A... A... Appa" -> "Appa") and filler words (um, uh).
2. Formulate a short, warm, enthusiastic grandmother reply (1-2 sentences).
   - Use affectionate words like "Kanna", "Chellam", "Sabash".
   - If the child made a grammatical or pronunciation mistake, repeat their sentence correctly as part of your natural reply (recasting).
   - Mix simple {language} and English.
   - Do NOT use markdown asterisks or special formatting. Keep punctuation simple for audio speech.
3. Assign a fluency/effort score between 70 and 100.

Output strictly in this format:
CLEANED_TEXT: <the cleaned intended words>
FEEDBACK: <Ammachi's warm spoken response>
SCORE: <integer score>
"""
            response = llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)

            cleaned_text = raw_transcript
            feedback = f"Sabash Kanna! Ammachi is so happy to hear you speak in {language}."
            score = 90

            for line in content.splitlines():
                if line.startswith("CLEANED_TEXT:"):
                    cleaned_text = line.replace("CLEANED_TEXT:", "").strip()
                elif line.startswith("FEEDBACK:"):
                    feedback = line.replace("FEEDBACK:", "").strip()
                elif line.startswith("SCORE:"):
                    try:
                        score = int("".join(c for c in line if c.isdigit()))
                    except:
                        score = 85

            return cleaned_text, feedback, score

        except Exception as e:
            logger.error("Error in patience agent LLM: %s", e)

    # Simple rule-based fallback if LLM is offline
    cleaned = " ".join(dict.fromkeys(raw_transcript.split()))
    return (
        cleaned,
        f"Sabash Kanna! You said '{cleaned}'. You are speaking {language} very well, keep it up!",
        85
    )
