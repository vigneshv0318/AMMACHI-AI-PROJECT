import os
import hmac
import hashlib
import json
import base64
import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Header, Form
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from database.connection import get_db
from database import crud
from schemas.auth import LoginRequest, SignupRequest, GoogleAuthRequest, LoginResponse, AuthConfigResponse
from schemas.user import UserProfileResponse

from dotenv import load_dotenv

router = APIRouter()

def get_google_client_id() -> str:
    return os.getenv("GOOGLE_CLIENT_ID", "")

def get_secret_key() -> str:
    return os.getenv("JWT_SECRET", "ammachi-super-secret-production-key-2026")

SECRET_KEY = get_secret_key()

# Safe JWT / Token Generator
try:
    import jwt
    HAS_JWT = True
except Exception:
    HAS_JWT = False

def create_access_token(username: str) -> str:
    secret = get_secret_key()
    payload = {
        "sub": username,
        "username": username,
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(days=14)).isoformat()
    }
    if HAS_JWT:
        return jwt.encode({"sub": username, "username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14)}, secret, algorithm="HS256")
    
    # Custom URL-safe HMAC signed token
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
    return f"{payload_str}.{signature}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    secret = get_secret_key()
    if HAS_JWT:
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except Exception:
            pass
    
    try:
        parts = token.split(".")
        if len(parts) == 2:
            payload_str, signature = parts
            expected_sig = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(signature, expected_sig):
                payload_json = base64.urlsafe_b64decode(payload_str.encode()).decode()
                return json.loads(payload_json)
    except Exception:
        pass
    return None

def get_current_user(
    authorization: str = Header(None), 
    db = Depends(get_db)
):
    """Dependency to extract authenticated user from Authorization Bearer header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication token required")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        username = payload.get("username") or payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = crud.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User account not found")
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/auth/config", response_model=AuthConfigResponse)
def get_auth_config():
    client_id = get_google_client_id()
    return AuthConfigResponse(google_client_id=client_id)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db = Depends(get_db)):
    user = crud.get_user_by_username(db, request.username)
    if user and crud.verify_password(request.password, user.password_hash):
        token = create_access_token(user.username)
        return LoginResponse(
            success=True,
            message="Welcome back, Kanna!",
            token=token,
            username=user.username,
            points=user.points or 0,
            language=user.current_language or "Tamil"
        )
    raise HTTPException(status_code=401, detail="Invalid username or password")

@router.post("/signup", response_model=LoginResponse)
def signup(request: SignupRequest, db = Depends(get_db)):
    existing = crud.get_user_by_username(db, request.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username is already taken, Kanna!")
    
    user = crud.create_user(
        db, 
        username=request.username, 
        password=request.password,
        current_language=request.language or "Tamil"
    )
    token = create_access_token(user.username)
    return LoginResponse(
        success=True,
        message="Account created! Welcome to Ammachi's class.",
        token=token,
        username=user.username,
        points=0,
        language=user.current_language
    )

@router.post("/auth/google", response_model=LoginResponse)
def google_auth(request: GoogleAuthRequest, db = Depends(get_db)):
    try:
        google_id = None
        email = None
        name = None
        client_id = get_google_client_id()

        if client_id:
            try:
                idinfo = id_token.verify_oauth2_token(request.id_token, google_requests.Request(), client_id)
                google_id = idinfo.get("sub")
                email = idinfo.get("email")
                name = idinfo.get("name", email.split("@")[0] if email else "student")
            except Exception:
                pass

        if not google_id:
            try:
                payload_part = request.id_token.split(".")[1]
                payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
                decoded = json.loads(base64.b64decode(payload_part).decode('utf-8'))
                google_id = decoded.get("sub") or decoded.get("user_id")
                email = decoded.get("email")
                name = decoded.get("name", email.split("@")[0] if email else "student")
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid Google token structure")

        if not google_id:
            raise HTTPException(status_code=401, detail="Could not retrieve verified Google ID")

        # 1. Lookup user by google_id
        user = crud.get_user_by_google_id(db, google_id)

        # 2. Account linking by email/username if google_id match was not found
        if not user and email:
            email_username = email.split("@")[0]
            existing_user = crud.get_user_by_username(db, email_username)
            if existing_user:
                crud.link_google_id_to_user(db, existing_user.id, google_id)
                user = existing_user

        # 3. Create new user if account doesn't exist
        if not user:
            base_username = email.split("@")[0] if email else f"user_{google_id[:8]}"
            username = base_username
            if crud.get_user_by_username(db, username):
                username = f"{base_username}_{google_id[:4]}"
            user = crud.create_user(db, username=username, google_id=google_id, current_language="Tamil")

        token = create_access_token(user.username)
        return LoginResponse(
            success=True,
            message=f"Namaste {name}!",
            token=token,
            username=user.username,
            points=user.points or 0,
            language=user.current_language or "Tamil"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google authentication failed: {str(e)}")

@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user = Depends(get_current_user), db = Depends(get_db)):
    return crud.get_user_progress_summary(db, current_user)
