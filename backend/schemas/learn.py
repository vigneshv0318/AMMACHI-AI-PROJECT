from pydantic import BaseModel
from typing import List, Optional, Dict, Any


# ---------- Path ----------

class PathNodeItem(BaseModel):
    id: int
    order: int
    node_type: str
    title: Optional[str] = None
    topic: Optional[str] = None
    completed: bool = False
    stars: int = 0
    is_current: bool = False
    locked: bool = False

class UnitItem(BaseModel):
    id: int
    order: int
    title: str
    description: Optional[str] = None
    progress_pct: float = 0
    nodes: List[PathNodeItem]

class PathResponse(BaseModel):
    language: str
    units: List[UnitItem]
    current_node_id: Optional[int] = None

class NodePreviewResponse(BaseModel):
    node_id: int
    node_type: str
    title: str
    lesson_no: int
    lesson_total: int
    xp: int = 10
    hearts: int
    hearts_max: int

# ---------- Lesson player ----------

class ExerciseItem(BaseModel):
    id: str
    type: str              # multiple_choice | translate | listen | match | speak
    prompt: str = ""
    native_text: Optional[str] = None
    transliteration: Optional[str] = None
    english: Optional[str] = None
    options: Optional[List[str]] = None
    answer_index: Optional[int] = None
    bank: Optional[List[str]] = None
    answer_words: Optional[List[str]] = None
    pairs: Optional[List[Dict[str, str]]] = None
    explanation: str = ""

class AttemptStartRequest(BaseModel):
    pass  # node id in path

class AttemptStartResponse(BaseModel):
    attempt_id: int
    node_id: Optional[int] = None
    exercises: List[ExerciseItem]
    hearts: int
    hearts_max: int
    xp: int = 10

class AnswerCheckRequest(BaseModel):
    exercise_id: str
    answer: Any = None     # index / list of words / dict for match etc.

class AnswerCheckResponse(BaseModel):
    correct: bool
    explanation: str = ""
    correct_answer: Optional[Any] = None
    hearts: int
    hearts_max: int
    out_of_hearts: bool = False
    combo_current: int = 0
    xp_gained: int = 0

class AttemptCompleteResponse(BaseModel):
    successful: bool
    xp_total: int
    base_xp: int
    combo_bonus: int = 0
    perfect_bonus: int = 0
    stars: int = 1
    correct: int = 0
    total: int = 0
    streak: int = 0
    streak_state: str = "same-day"
    gems: int = 0
    combo_max: int = 0

# ---------- HUD / quests / shop / leaderboard ----------

class QuestItem(BaseModel):
    type: str
    title: str
    progress: int
    target: int
    claimed: bool
    reward_gems: int

class QuestClaimResponse(BaseModel):
    ok: bool
    gems: int
    reward_gems: int = 0

class HudResponse(BaseModel):
    xp: int
    xp_today: int
    daily_goal: int
    daily_goal_met: bool
    gems: int
    hearts: int
    hearts_max: int
    streak: int
    longest_streak: int
    streak_freezes: int
    league: str
    league_meta: Dict[str, Any]
    quests: List[QuestItem]

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    xp: int
    is_current_user: bool = False
    avatar_url: Optional[str] = None

class LeaderboardResponse(BaseModel):
    league: str
    week: str
    advances: int
    days_left: int
    my_rank: Optional[int] = None
    entries: List[LeaderboardEntry]

class ShopItemOut(BaseModel):
    id: str
    title: str
    description: str
    cost: int
    icon: str
    kind: str  # hearts | streak_freeze | goal | gems
    extra: Optional[Dict[str, Any]] = None

class ShopResponse(BaseModel):
    gems: int
    hearts: int
    hearts_max: int
    daily_goal: int
    streak_freezes: int
    items: List[ShopItemOut]

class PurchaseRequest(BaseModel):
    item_id: str

class PurchaseResponse(BaseModel):
    ok: bool
    message: str
    gems: int
    hearts: int
    streak_freezes: int = 0
    daily_goal: Optional[int] = None

class GoalRequest(BaseModel):
    daily_goal: int

class GoalResponse(BaseModel):
    ok: bool
    daily_goal: int
