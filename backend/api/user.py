import os
import time
import logging
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from database.connection import get_db
from database import crud
from services import storage_service

logger = logging.getLogger("ammachi.user")
from api.auth import get_current_user
from schemas.user import UserProfileResponse, UpdateLanguageRequest

router = APIRouter()

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large. Maximum size is 5MB.")

    file_ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if file_ext not in {"jpg", "jpeg", "png", "webp", "gif"}:
        file_ext = "jpg"
    filename = f"profiles/user_{current_user.id}_{int(time.time())}.{file_ext}"

    old_avatar_url = getattr(current_user, "avatar_url", None)
    try:
        avatar_url = storage_service.upload_file(content, filename, file.content_type)
    except Exception as e:
        logger.error("Avatar upload failed: %s", e)
        raise HTTPException(status_code=502, detail="Could not save the photo. Please try again.")

    crud.update_user_avatar(db, current_user.id, avatar_url)
    if old_avatar_url and old_avatar_url != avatar_url:
        storage_service.delete_file(old_avatar_url)

    return {"success": True, "avatar_url": avatar_url}

@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    return crud.get_user_progress_summary(db, current_user)

@router.put("/language")
def update_language(
    request: UpdateLanguageRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    updated = crud.update_user_language(db, current_user.id, request.language)
    return {"success": True, "language": updated.current_language}

@router.get("/stamps")
def get_stamps(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    return [
        {
            "id": s.id,
            "stamp_name": s.stamp_name,
            "badge_icon": s.badge_icon,
            "earned_at": s.earned_at.isoformat() if hasattr(s.earned_at, "isoformat") else str(s.earned_at)
        }
        for s in current_user.stamps
    ]
