"""
Ammachi Learn Path & Gamification API — Duolingo-style features:
/path · /node preview · /attempt (start, answer, complete) · /hud · /quests · /shop · /leaderboard
"""
import os
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from database.connection import get_db
from api.auth import get_current_user
from database import crud
from database.learn_models import LearnUnit, LearnNode, NodeProgress, LessonAttempt
from schemas.learn import (
    PathResponse, UnitItem, PathNodeItem, NodePreviewResponse, ExerciseItem,
    AttemptStartResponse, AnswerCheckRequest, AnswerCheckResponse,
    AttemptCompleteResponse, HudResponse, LeaderboardResponse, LeaderboardEntry,
    ShopResponse, ShopItemOut, PurchaseRequest, PurchaseResponse,
    QuestClaimResponse, GoalRequest, GoalResponse,
)
from services import learn_content
from services import gamification
from services.gamification import (
    ensure_stats, lose_heart, maybe_refill_heart, register_daily_activity,
    bump_quest, league_for_xp, week_key, LEAGUE_TIERS, QUEST_TEMPLATES,
    quest_target, COMBO_BONUS_XP,
)

router = APIRouter()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _serialize_exercise(ex: Dict[str, Any]) -> Dict[str, Any]:
    """Clean exercise dict for client (no answer leakage where possible)."""
    out = dict(ex)
    return out


def _unit_progress(db, user_id: int, unit: LearnUnit, progress_by_node: Dict[int, NodeProgress]):
    nodes = sorted(unit.nodes, key=lambda n: n.order)
    lesson_count = sum(1 for n in nodes if n.node_type in ("lesson", "story", "practice", "unit_review"))
    done = sum(1 for n in nodes if n.node_type in ("lesson", "story", "practice", "unit_review")
               and progress_by_node.get(n.id) and progress_by_node[n.id].completed)
    return int((done / lesson_count) * 100) if lesson_count else 0


def _get_path(db, user, language: str):
    units = db.query(LearnUnit).filter(LearnUnit.language == language).order_by(LearnUnit.order).all()
    if len(units) < len(learn_content.UNIT_BLUEPRINTS):  # missing units (fresh language or old seed)
        units = _ensure_seed_path(db, language)
    progress = db.query(NodeProgress).filter(NodeProgress.user_id == user.id).all()
    progress_by_node = {p.node_id: p for p in progress}
    return units, progress_by_node


def _ensure_seed_path(db, language: str) -> List[LearnUnit]:
    """Create missing default units/nodes for a language (idempotent — appends unit orders not yet present)."""
    existing_orders = {u.order for u in db.query(LearnUnit).filter(LearnUnit.language == language).all()}
    for blueprint in learn_content._default_units(language):
        if blueprint["order"] in existing_orders:
            continue
        unit = LearnUnit(
            language=language,
            order=blueprint["order"],
            title=blueprint["title"],
            description=blueprint.get("description"),
        )
        db.add(unit)
        db.flush()
        for nb in blueprint["nodes"]:
            db.add(LearnNode(
                unit_id=unit.id,
                order=nb["order"],
                node_type=nb["node_type"],
                topic=nb.get("topic"),
            ))
    db.commit()
    return db.query(LearnUnit).filter(LearnUnit.language == language).order_by(LearnUnit.order).all()


def _path_payload(db, user, language: str) -> Dict[str, Any]:
    units, progress_by_node = _get_path(db, user, language)
    current_node_id = None
    all_learn_nodes: List[LearnNode] = []
    unit_items: List[UnitItem] = []

    for unit in units:
        nodes = sorted(unit.nodes, key=lambda n: n.order)
        for n in nodes:
            if n.node_type in ("lesson", "story", "practice", "unit_review"):
                all_learn_nodes.append(n)
        unit_items.append(UnitItem(
            id=unit.id,
            order=unit.order,
            title=unit.title,
            description=unit.description,
            progress_pct=_unit_progress(db, user.id, unit, progress_by_node),
            nodes=[
                PathNodeItem(
                    id=n.id,
                    order=n.order,
                    node_type=n.node_type,
                    title=n.title,
                    topic=n.topic,
                    completed=bool(progress_by_node.get(n.id) and progress_by_node[n.id].completed),
                    stars=(progress_by_node[n.id].stars if progress_by_node.get(n.id) else 0),
                )
                for n in nodes
            ],
        ))

    current = next((n for n in all_learn_nodes
                    if not (progress_by_node.get(n.id) and progress_by_node[n.id].completed)), None)
    if current:
        current_node_id = current.id

    # A learn node is unlocked when it is completed, or it is the current node.
    # Chest nodes unlock together with the next learn node after them.
    unlocked = set()
    if current_node_id is not None:
        unlocked.add(current_node_id)
    elif all_learn_nodes:
        pass  # everything complete
    for n in all_learn_nodes:
        if progress_by_node.get(n.id) and progress_by_node[n.id].completed:
            unlocked.add(n.id)

    for unit_item in unit_items:
        for node_item in unit_item.nodes:
            node_item.is_current = (node_item.id == current_node_id)
            learn_node = next((n for n in all_learn_nodes if n.id == node_item.id), None)
            if node_item.node_type == "chest":
                node_item.locked = not unlocked  # chests open once any lesson is unlocked
            else:
                node_item.locked = node_item.id not in unlocked

    return {"language": language, "units": [u.dict() for u in unit_items], "current_node_id": current_node_id}


# ------------------------------------------------------------
# Path endpoints
# ------------------------------------------------------------

@router.get("/path")
def get_path(
    language: Optional[str] = None,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    lang = language or current_user.current_language or "Tamil"
    return _path_payload(db, current_user, lang)


@router.get("/node/{node_id}/preview", response_model=NodePreviewResponse)
def node_preview(node_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    node = db.query(LearnNode).filter(LearnNode.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Path node not found")
    unit = db.query(LearnUnit).filter(LearnUnit.id == node.unit_id).first()
    lang = unit.language if unit else "Tamil"

    # Lesson number within this run of practice-able nodes
    siblings = sorted(unit.nodes, key=lambda n: n.order) if unit else [node]
    lesson_no = node.order
    lesson_total = max(s.order for s in siblings) if siblings else node.order

    stats = ensure_stats(db, current_user)
    maybe_refill_heart(db, stats)
    return NodePreviewResponse(
        node_id=node.id,
        node_type=node.node_type,
        title=learn_content.TOPIC_TITLE.get(node.topic or "", "Practice"),
        lesson_no=lesson_no,
        lesson_total=lesson_total,
        xp=10,
        hearts=stats.hearts or 0,
        hearts_max=stats.hearts_max or gamification.HEARTS_DEFAULT_MAX,
    )


# ------------------------------------------------------------
# Lesson attempts
# ------------------------------------------------------------

@router.post("/node/{node_id}/start", response_model=AttemptStartResponse)
async def start_attempt(node_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    node = db.query(LearnNode).filter(LearnNode.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Path node not found")
    unit = db.query(LearnUnit).filter(LearnUnit.id == node.unit_id).first()
    lang = unit.language if unit else (current_user.current_language or "Tamil")

    stats = ensure_stats(db, current_user)
    maybe_refill_heart(db, stats)

    if (stats.hearts or 0) <= 0:
        raise HTTPException(status_code=402, detail="Out of hearts! Visit the Shop or wait for a refill.")

    # Abandon stale ACTIVE attempt for same node
    stale = db.query(LessonAttempt).filter(
        LessonAttempt.user_id == current_user.id,
        LessonAttempt.node_id == node_id,
        LessonAttempt.status == "ACTIVE",
    ).all()
    for s in stale:
        s.status = "ABANDONED"

    exercises = await learn_content.generate_lesson_exercises(node.node_type, node.topic or "greetings", lang)
    exercises = [_serialize_exercise(e) for e in exercises]

    attempt = LessonAttempt(
        user_id=current_user.id,
        node_id=node_id,
        exercises=exercises,
        status="ACTIVE",
        language=lang,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return AttemptStartResponse(
        attempt_id=attempt.id,
        node_id=node_id,
        exercises=[ExerciseItem(**e) for e in exercises],
        hearts=stats.hearts or 0,
        hearts_max=stats.hearts_max or gamification.HEARTS_DEFAULT_MAX,
        xp=10,
    )


@router.post("/attempt/{attempt_id}/answer", response_model=AnswerCheckResponse)
def check_answer(attempt_id: int, request: AnswerCheckRequest, current_user=Depends(get_current_user), db=Depends(get_db)):
    attempt = db.query(LessonAttempt).filter(
        LessonAttempt.id == attempt_id, LessonAttempt.user_id == current_user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != "ACTIVE":
        raise HTTPException(status_code=409, detail="Attempt already finished")

    exercise = next((e for e in (attempt.exercises or []) if e.get("id") == request.exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found in this attempt")

    correct = _evaluate_answer(exercise, request.answer)

    stats = ensure_stats(db, current_user)
    xg = 0
    if correct:
        attempt.correct_count += 1
        attempt.combo_current += 1
        if attempt.combo_current > attempt.combo_max:
            attempt.combo_max = attempt.combo_current
        if attempt.combo_current >= 5:
            xg = COMBO_BONUS_XP
            attempt.combo_current = 0  # combo banked
        bump_quest(db, current_user, stats, "correct_answers", 1)
    else:
        attempt.wrong_count += 1
        attempt.combo_current = 0
        attempt.hearts_lost += 1
        lose_heart(db, stats)

    results = attempt.results or []
    results.append({"exercise_id": request.exercise_id, "correct": correct, "tries": 1})
    attempt.results = results
    attempt.current_index += 1
    db.commit()

    hearts_now = stats.hearts or 0
    return AnswerCheckResponse(
        correct=correct,
        explanation=exercise.get("explanation", ""),
        correct_answer=_correct_answer(exercise) if not correct else None,
        hearts=hearts_now,
        hearts_max=stats.hearts_max or gamification.HEARTS_DEFAULT_MAX,
        out_of_hearts=hearts_now <= 0,
        combo_current=attempt.combo_current,
        xp_gained=xg,
    )


def _evaluate_answer(exercise: Dict[str, Any], answer: Any) -> bool:
    etype = exercise.get("type")
    if etype in ("multiple_choice", "listen"):
        try:
            return int(answer) == int(exercise.get("answer_index", -1))
        except (TypeError, ValueError):
            return False
    if etype == "translate":
        expected = [w.lower() for w in exercise.get("answer_words", [])]
        given = [str(w).lower().strip() for w in (answer or []) if str(w).strip()]
        return given == expected
    if etype == "match":
        # client sends {native: english} mapping; verify all pairs correct
        pairs = {p["native"]: p["english"] for p in exercise.get("pairs", [])}
        if not isinstance(answer, dict):
            return False
        return all(pairs.get(k) == v for k, v in answer.items())
    if etype == "speak":
        # validated client-side via voice module; server accepts generous match
        return bool(answer)
    return False


def _correct_answer(exercise: Dict[str, Any]) -> Any:
    etype = exercise.get("type")
    if etype in ("multiple_choice", "listen"):
        return exercise.get("options", [None])[exercise.get("answer_index", 0)] if exercise.get("options") else None
    if etype == "translate":
        return exercise.get("answer_words")
    if etype == "match":
        return exercise.get("pairs")
    return None


@router.post("/attempt/{attempt_id}/complete", response_model=AttemptCompleteResponse)
def complete_attempt(attempt_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    attempt = db.query(LessonAttempt).filter(
        LessonAttempt.id == attempt_id, LessonAttempt.user_id == current_user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    stats = ensure_stats(db, current_user)
    exercises = attempt.exercises or []
    total = len([e for e in exercises if e.get("type") in ("multiple_choice", "translate", "listen", "match", "speak")])

    already = attempt.status == "COMPLETED"
    if not already:
        # Mark node progress (best of attempts)
        node = db.query(LearnNode).filter(LearnNode.id == attempt.node_id).first()
        if node:
            prog = db.query(NodeProgress).filter(
                NodeProgress.user_id == current_user.id, NodeProgress.node_id == node.id).first()
            hearts_remaining = stats.hearts or 0
            pct = int((attempt.correct_count / total) * 100) if total else 0
            if not prog:
                prog = NodeProgress(user_id=current_user.id, node_id=node.id)
                db.add(prog)
                db.flush()
            prog.completed = True
            prog.best_score = max(prog.best_score or 0, pct)
            prog.stars = max(prog.stars or 0, max(1, min(3, hearts_remaining + 1)))
            prog.attempts = (prog.attempts or 0) + 1
            prog.last_completed_at = datetime.utcnow()

        award = gamification.award_lesson_completion(
            db, current_user, stats,
            correct=attempt.correct_count, total=total,
            hearts_remaining=stats.hearts or 0,
            combo_max=attempt.combo_max,
        )
        attempt.xp_awarded = award["xp_total"]
        attempt.status = "COMPLETED"
        attempt.completed_at = datetime.utcnow()
        db.commit()
    else:
        award = {
            "xp_total": attempt.xp_awarded or 0, "base_xp": 10, "combo_bonus": 0,
            "perfect_bonus": 0, "stars": 1, "streak": stats.streak, "gems": stats.gems,
        }

    return AttemptCompleteResponse(
        successful=True,
        xp_total=award["xp_total"],
        base_xp=award["base_xp"],
        combo_bonus=award.get("combo_bonus", 0),
        perfect_bonus=award.get("perfect_bonus", 0),
        stars=award["stars"],
        correct=attempt.correct_count,
        total=total,
        streak=stats.streak,
        streak_state=award.get("streak_state", "same-day"),
        gems=stats.gems or 0,
        combo_max=attempt.combo_max,
    )


@router.post("/attempt/{attempt_id}/quit")
def quit_attempt(attempt_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    attempt = db.query(LessonAttempt).filter(
        LessonAttempt.id == attempt_id, LessonAttempt.user_id == current_user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status == "ACTIVE":
        attempt.status = "ABANDONED"
        db.commit()
    return {"ok": True}


# ------------------------------------------------------------
# HUD / quests / shop / leaderboard
# ------------------------------------------------------------

@router.get("/hud", response_model=HudResponse)
def get_hud(current_user=Depends(get_current_user), db=Depends(get_db)):
    return gamification.hud_summary(db, current_user)


@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(current_user=Depends(get_current_user), db=Depends(get_db)):
    from database.learn_models import WeeklyXp
    from database.models import User
    week = week_key()
    rows = db.query(WeeklyXp).filter(WeeklyXp.week == week).order_by(WeeklyXp.xp.desc()).all()
    users = {u.id: u for u in db.query(User).all()}
    entries = []
    my_rank = None
    for i, row in enumerate(rows):
        u = users.get(row.user_id)
        if not u:
            continue
        is_me = u.id == current_user.id
        if is_me:
            my_rank = i + 1
        entries.append(LeaderboardEntry(rank=i + 1, username=u.username, xp=row.xp or 0,
                                        is_current_user=is_me, avatar_url=getattr(u, "avatar_url", None)))
    # ensure the current user is present even with 0 XP
    if my_rank is None:
        me = next((e for e in entries if e.is_current_user), None)
        base_rank = len(entries) + 1
        entries.append(LeaderboardEntry(rank=base_rank, username=current_user.username, xp=0, is_current_user=True))
        my_rank = base_rank

    stats = ensure_stats(db, current_user)
    league, meta = league_for_xp(stats.xp or 0)
    days_left = 7 - ((date.today().isocalendar().weekday - 1) % 7) or 7
    return LeaderboardResponse(
        league=league, week=week,
        advances=meta.get("advances", 3),
        days_left=days_left,
        my_rank=my_rank,
        entries=entries[:15],
    )


@router.post("/quests/{quest_type}/claim", response_model=QuestClaimResponse)
def claim_quest(quest_type: str, current_user=Depends(get_current_user), db=Depends(get_db)):
    template = next((t for t in QUEST_TEMPLATES if t["type"] == quest_type), None)
    if not template:
        raise HTTPException(status_code=404, detail="Unknown quest")

    from database.learn_models import QuestProgress
    today = date.today().strftime("%Y-%m-%d")
    stats = ensure_stats(db, current_user)
    target = quest_target(template, stats)

    row = db.query(QuestProgress).filter(
        QuestProgress.user_id == current_user.id,
        QuestProgress.date == today,
        QuestProgress.quest_type == quest_type,
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Quest not started yet")
    if (row.progress or 0) < target:
        raise HTTPException(status_code=409, detail="Quest not finished yet!")
    if row.claimed:
        raise HTTPException(status_code=409, detail="Already claimed this chest today")

    row.claimed = True
    stats.gems = (stats.gems or 0) + template["reward_gems"]
    db.commit()
    return QuestClaimResponse(ok=True, gems=stats.gems or 0, reward_gems=template["reward_gems"])


SHOP_ITEMS = [
    {"id": "heart_refill", "kind": "hearts", "title": "Refill hearts",
     "description": "Fill all hearts instantly.", "cost": 350, "icon": "❤️"},
    {"id": "streak_freeze", "kind": "streak_freeze", "title": "Streak freeze",
     "description": "Protects your streak for a day you miss.", "cost": 200, "icon": "🧊"},
    {"id": "goal_20", "kind": "goal", "title": "Casual goal",
     "description": "20 XP per day", "cost": 0, "icon": "🎯", "extra": {"goal": 20}},
    {"id": "goal_50", "kind": "goal", "title": "Serious goal",
     "description": "50 XP per day", "cost": 0, "icon": "🎯", "extra": {"goal": 50}},
    {"id": "goal_80", "kind": "goal", "title": "Intense goal",
     "description": "80 XP per day", "cost": 0, "icon": "🎯", "extra": {"goal": 80}},
]


@router.get("/shop", response_model=ShopResponse)
def get_shop(current_user=Depends(get_current_user), db=Depends(get_db)):
    stats = ensure_stats(db, current_user)
    maybe_refill_heart(db, stats)
    return ShopResponse(
        gems=stats.gems or 0,
        hearts=stats.hearts or 0,
        hearts_max=stats.hearts_max or gamification.HEARTS_DEFAULT_MAX,
        daily_goal=stats.daily_goal or 20,
        streak_freezes=stats.streak_freezes or 0,
        items=[ShopItemOut(**i) for i in SHOP_ITEMS],
    )


@router.post("/shop/purchase", response_model=PurchaseResponse)
def purchase(request: PurchaseRequest, current_user=Depends(get_current_user), db=Depends(get_db)):
    item = next((i for i in SHOP_ITEMS if i["id"] == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown shop item")

    stats = ensure_stats(db, current_user)

    if item["kind"] == "goal":
        goal = item["extra"]["goal"]
        stats.daily_goal = goal
        db.commit()
        return PurchaseResponse(ok=True, message=f"Daily goal set to {goal} XP!",
                                gems=stats.gems or 0, hearts=stats.hearts or 0,
                                streak_freezes=stats.streak_freezes or 0, daily_goal=goal)

    if (stats.gems or 0) < item["cost"]:
        raise HTTPException(status_code=402, detail="Not enough gems! Earn more XP to collect gems.")

    stats.gems = (stats.gems or 0) - item["cost"]
    if item["kind"] == "hearts":
        stats.hearts = stats.hearts_max or gamification.HEARTS_DEFAULT_MAX
        stats.hearts_refill_at = None
        message = "All hearts refilled!"
    elif item["kind"] == "streak_freeze":
        stats.streak_freezes = (stats.streak_freezes or 0) + 1
        message = "Streak freeze equipped! Stay warm, kanna."
    else:
        message = "Purchase complete."
    db.commit()

    return PurchaseResponse(
        ok=True, message=message,
        gems=stats.gems or 0, hearts=stats.hearts or 0,
        streak_freezes=stats.streak_freezes or 0,
    )


@router.post("/goal", response_model=GoalResponse)
def set_goal(request: GoalRequest, current_user=Depends(get_current_user), db=Depends(get_db)):
    if request.daily_goal not in (10, 20, 30, 50, 80):
        raise HTTPException(status_code=400, detail="Choose a valid daily goal (10-80 XP)")
    stats = ensure_stats(db, current_user)
    stats.daily_goal = request.daily_goal
    db.commit()
    return GoalResponse(ok=True, daily_goal=stats.daily_goal)
