from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4)

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4)
    language: Optional[str] = "Tamil"

class GoogleAuthRequest(BaseModel):
    id_token: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    username: Optional[str] = None
    points: Optional[int] = 0
    language: Optional[str] = "Tamil"

class AuthConfigResponse(BaseModel):
    google_client_id: str
