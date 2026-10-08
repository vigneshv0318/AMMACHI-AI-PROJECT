import json
from typing import List, Optional
from fastapi import APIRouter, Form, Depends, HTTPException, Query

from database.connection import get_db
from database import crud
from api.auth import get_current_user
from schemas.culture import (
    CultureChatRequest,
    CultureChatResponse,
    FestivalInfo,
    YouTubeVideoItem,
    QuizQuestionItem,
    QuizSubmitRequest,
    QuizSubmitResponse
)
from services.culture_service import get_festivals_for_language, get_festival_by_id, get_festival_quiz_questions
from services.youtube_service import get_festival_youtube_videos
from agents.langgraph_culture import run_culture_chat

router = APIRouter()

@router.get("/festivals", response_model=List[FestivalInfo])
def get_festivals(language: str = "Tamil"):
    data = get_festivals_for_language(language)
    for item in data:
        item["quiz_count"] = 10
    return [FestivalInfo(**item) for item in data]

@router.get("/videos", response_model=List[YouTubeVideoItem])
def get_festival_videos(
    festival: str = Query("pongal", description="Festival ID or name"),
    language: str = Query("Tamil", description="Native language")
):
    """
    Returns relevant YouTube video lessons and animated stories for the selected festival.
    Uses YouTube Data API v3 when configured with YOUTUBE_API_KEY.
    """
    videos = get_festival_youtube_videos(festival, festival, language)
    return [YouTubeVideoItem(**v) for v in videos]

@router.get("/quiz", response_model=List[QuizQuestionItem])
def get_festival_quiz(
    festival: str = Query("pongal", description="Festival ID or name"),
    language: str = Query("Tamil", description="Native language")
):
    """
    Returns 10 contextual quiz questions for the selected festival.
    """
    questions = get_festival_quiz_questions(festival, language)
    return [QuizQuestionItem(**q) for q in questions]

@router.post("/quiz/submit", response_model=QuizSubmitResponse)
def submit_quiz_answer(
    request: QuizSubmitRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Validates the child's quiz answer for the festival.
    Awards +10 points on correct answer, logs learning progress, and checks badge unlocks.
    """
    questions = get_festival_quiz_questions(request.festival, request.language or "Tamil")
    question = next((q for q in questions if q["id"] == request.question_id), None)
    
    if not question:
        raise HTTPException(status_code=404, detail="Quiz question not found")

    is_correct = (request.selected_index == question["answer_index"])
    points_to_award = 10 if is_correct else 2
    
    stamp_name = f"{request.festival.capitalize()} Cultural Master"
    badge_icon = "🪔"
    fest_l = request.festival.lower()
    if "pongal" in fest_l: badge_icon = "🌾"
    elif "diwali" in fest_l: badge_icon = "🪔"
    elif "ugadi" in fest_l: badge_icon = "🌿"
    elif "onam" in fest_l: badge_icon = "🌸"
    elif "karthigai" in fest_l: badge_icon = "🪔"
    elif "thaipusam" in fest_l: badge_icon = "🦚"
    elif "sankranti" in fest_l or "lohri" in fest_l: badge_icon = "🪁"
    elif "holi" in fest_l: badge_icon = "🎨"
    elif "dussehra" in fest_l: badge_icon = "🏹"
    elif "raksha" in fest_l or "rakhi" in fest_l: badge_icon = "🧵"
    elif "janmashtami" in fest_l or "krishna" in fest_l: badge_icon = "🦚"
    elif "navratri" in fest_l or "durga" in fest_l: badge_icon = "🌸"
    elif "ganesh" in fest_l or "vinayagar" in fest_l or "pillaiyar" in fest_l: badge_icon = "🐘"
    elif "ayudha" in fest_l or "saraswathi" in fest_l: badge_icon = "📚"
    elif "chhath" in fest_l: badge_icon = "🌅"
    elif "bonalu" in fest_l: badge_icon = "🏺"
    elif "puthandu" in fest_l: badge_icon = "🥭"

    # Log progress in DB
    crud.log_learning_progress(
        db=db,
        user_id=current_user.id,
        module="culture",
        activity=f"Quiz: {question['question'][:40]}",
        score=100 if is_correct else 40,
        language=request.language or "Tamil"
    )

    # Award points & unlock stamp on correct answer
    updated = crud.update_user_points_and_stamp(
        db=db,
        username=current_user.username,
        points_to_add=points_to_award,
        stamp_name=stamp_name if is_correct else None,
        badge_icon=badge_icon
    )

    feedback = (
        f"Sabash Kanna! Excellent answer! You earned +{points_to_award} points!"
        if is_correct
        else f"Good attempt, Kanna! Ammachi wants you to know: {question['explanation']}"
    )

    return QuizSubmitResponse(
        is_correct=is_correct,
        correct_index=question["answer_index"],
        explanation=question["explanation"],
        feedback=feedback,
        points_awarded=points_to_award,
        total_points=updated["points"],
        new_stamp_earned=updated.get("new_stamp_earned", False),
        stamp_name=stamp_name,
        stamps=updated.get("stamps", [])
    )

@router.post("/chat", response_model=CultureChatResponse)
def culture_chat(
    request: CultureChatRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        raw_history = json.loads(request.history) if request.history else []
    except Exception:
        raw_history = []

    result = run_culture_chat(
        message=request.message,
        raw_history=raw_history,
        username=current_user.username,
        language=request.language or current_user.current_language or "Tamil"
    )

    crud.log_learning_progress(
        db=db,
        user_id=current_user.id,
        module="culture",
        activity=f"Cultural Discovery: {request.language}",
        score=100 if result.get("stamps") else 85,
        language=request.language or "Tamil"
    )

    return CultureChatResponse(
        response=result["response"],
        points=result["points"],
        stamps=result["stamps"],
        new_stamp_earned=False,
        media=result.get("media", []),
        videos=result.get("videos", [])
    )
