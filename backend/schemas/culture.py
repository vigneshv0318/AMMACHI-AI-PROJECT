from pydantic import BaseModel
from typing import List, Optional

class CultureChatRequest(BaseModel):
    message: str
    history: Optional[str] = "[]"
    language: Optional[str] = "Tamil"

class MediaItem(BaseModel):
    type: str  # 'image' or 'video'
    url: str
    caption: Optional[str] = None

class YouTubeVideoItem(BaseModel):
    video_id: str
    title: str
    description: Optional[str] = ""
    thumbnail: Optional[str] = ""
    embed_url: str
    channel_title: Optional[str] = ""

class QuizQuestionItem(BaseModel):
    id: str
    question: str
    options: List[str]
    answer_index: int
    explanation: str

class QuizSubmitRequest(BaseModel):
    festival: str
    question_id: str
    selected_index: int
    language: Optional[str] = "Tamil"

class QuizSubmitResponse(BaseModel):
    is_correct: bool
    correct_index: int
    explanation: str
    feedback: str
    points_awarded: int
    total_points: int
    new_stamp_earned: bool = False
    stamp_name: Optional[str] = None
    stamps: List[str] = []

class FestivalInfo(BaseModel):
    id: str
    name: str
    native_name: str
    language: str
    summary: str
    significance: str
    icon: str
    image_url: Optional[str] = None
    videos: Optional[List[YouTubeVideoItem]] = []
    quiz_count: Optional[int] = 10

class CultureChatResponse(BaseModel):
    response: str
    points: int
    stamps: List[str]
    new_stamp_earned: Optional[bool] = False
    media: Optional[List[MediaItem]] = None
    videos: Optional[List[YouTubeVideoItem]] = []
