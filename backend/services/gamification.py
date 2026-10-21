"""
Ammachi gamification engine (Duolingo-style economy):
XP, gems, hearts, daily streak with freezes, daily quests, weekly league.
"""
import logging
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("ammachi.gamification")

HEARTS_DEFAULT_MAX = 5
HEART_REFILL_MINUTES = 30  # one free heart back every 30 min
COMBO_BONUS_XP = 3         # bonus XP for a 5-in-a-row "combo"
QUEST_TEMPLATES = [
    {"type": "earn_xp", "target_key": "daily_goal", "reward_gems": 15},
    {"type": "finish_lessons", "target": 2, "reward_gems": 10},
    {"type": "correct_answers", "target": 8, "reward_gems": 10},
]

LEAGUE_TIERS = ["Bronze", "Silver", "Gold", "Sapphire", "Ruby", "Diamond"]


def _today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def _yesterday_str() -> str:
    return (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")


def week_key() -> str:
    today = date.today()
    return f"{today.isocalendar().year}-W{today.isocalendar().week:02d}"


def ensure_stats(db, user):
    """Fetch or bootstrap the UserStats row for a user."""
    from database.learn_models import UserStats
    stats = db.query(UserStats).filter(UserStats.user_id == user.id).first()
    if not stats:
        stats = UserStats(
            user_id=user.id,
            xp=0, gems=0,
            hearts=HEARTS_DEFAULT_MAX, hearts_max=HEARTS_DEFAULT_MAX,
            streak=0, longest_streak=0, daily_goal=20,
            streak_freezes=0, last_active_date=None,
            weekly_xp=0,
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


def league_for_xp(xp: int) -> Tuple[str, Dict[str, Any]]:
    idx = min(len(LEAGUE_TIERS) - 1, xp // 500)
    return LEAGUE_TIERS[idx], {
        "tier": idx,
        "next_tier_xp": (idx + 1) * 500,
        "advances": 3,
        "demotes": (idx > 0),
    }


def register_daily_activity(db, stats) -> Dict[str, Any]:
    """Update streak when XP is earned today. Returns event info for the Streak UI."""
    today = _today_str()
    yesterday = _yesterday_str()
    state = "same-day"
    if stats.last_active_date != today:
        if stats.last_active_date == yesterday:
            stats.streak = (stats.streak or 0) + 1
            state = "extended"
        elif stats.last_active_date is None:
            stats.streak = 1
            state = "started"
        else:
            # Streak broken (no freeze consumed here for simplicity) – restart
            stats.streak = 1
            state = "reset"
        stats.last_active_date = today
    if stats.streak > (stats.longest_streak or 0):
        stats.longest_streak = stats.streak
    return {"state": state, "streak": stats.streak}


def register_weekly_xp(db, user, amount: int):
    from database.learn_models import WeeklyXp
    week = week_key()
    row = db.query(WeeklyXp).filter(WeeklyXp.user_id == user.id, WeeklyXp.week == week).first()
    if not row:
        row = WeeklyXp(user_id=user.id, week=week, xp=0)
        db.add(row)
        db.flush()
    row.xp = (row.xp or 0) + max(0, amount)


def quest_target(template: Dict[str, Any], stats) -> int:
    if template.get("target_key") == "daily_goal":
        return stats.daily_goal or 20
    return template.get("target", 1)


def bump_quest(db, user, stats, quest_type: str, amount: int = 1):
    from database.learn_models import QuestProgress
    today = _today_str()
    for t in QUEST_TEMPLATES:
        if t["type"] != quest_type:
            continue
        row = db.query(QuestProgress).filter(
            QuestProgress.user_id == user.id,
            QuestProgress.date == today,
            QuestProgress.quest_type == quest_type,
        ).first()
        if not row:
            row = QuestProgress(user_id=user.id, date=today, quest_type=quest_type,
                                progress=0, target=quest_target(t, stats))
            db.add(row)
            db.flush()
        row.progress = min(row.target, (row.progress or 0) + amount)
    db.commit()


def quest_snapshot(db, user, stats) -> list:
    from database.learn_models import QuestProgress
    today = _today_str()
    # reset stale rows implicitly by querying today only
    rows = {r.quest_type: r for r in db.query(QuestProgress).filter(
        QuestProgress.user_id == user.id, QuestProgress.date == today).all()}
    out = []
    for t in QUEST_TEMPLATES:
        row = rows.get(t["type"])
        out.append({
            "type": t["type"],
            "title": {
                "earn_xp": f"Earn {quest_target(t, stats)} XP today",
                "finish_lessons": "Finish 2 lessons",
                "correct_answers": "Get 8 answers right",
            }[t["type"]],
            "progress": row.progress if row else 0,
            "target": quest_target(t, stats),
            "claimed": bool(row.claimed) if row else False,
            "reward_gems": t["reward_gems"],
        })
    return out


def lose_heart(db, stats) -> Dict[str, Any]:
    stats.hearts = max(0, (stats.hearts or 0) - 1)
    if stats.hearts == 0:
        # Set the regen timer for the first free heart (naive UTC)
        stats.hearts_refill_at = datetime.utcnow() + timedelta(minutes=HEART_REFILL_MINUTES)
    db.commit()
    return {"hearts": stats.hearts, "hearts_max": stats.hearts_max or HEARTS_DEFAULT_MAX, "out_of_hearts": stats.hearts == 0}


def maybe_refill_heart(db, stats) -> bool:
    if stats.hearts >= (stats.hearts_max or HEARTS_DEFAULT_MAX):
        return False
    if stats.hearts_refill_at:
        now = datetime.utcnow()  # refill_at is stored as naive UTC
        if now >= stats.hearts_refill_at:
            gained = 1 + int((now - stats.hearts_refill_at).total_seconds() // (HEART_REFILL_MINUTES * 60))
            stats.hearts = min(stats.hearts_max or HEARTS_DEFAULT_MAX, stats.hearts + gained)
            if stats.hearts >= (stats.hearts_max or HEARTS_DEFAULT_MAX):
                stats.hearts_refill_at = None
            else:
                stats.hearts_refill_at = datetime.utcnow() + timedelta(minutes=HEART_REFILL_MINUTES)
            db.commit()
            return True
    return False


def hud_summary(db, user) -> Dict[str, Any]:
    stats = ensure_stats(db, user)
    maybe_refill_heart(db, stats)
    xp_today = _xp_today(db, user)
    league, meta = league_for_xp(stats.xp or 0)
    return {
        "xp": stats.xp or 0,
        "xp_today": xp_today,
        "daily_goal": stats.daily_goal or 20,
        "daily_goal_met": xp_today >= (stats.daily_goal or 20),
        "gems": stats.gems or 0,
        "hearts": stats.hearts or 0,
        "hearts_max": stats.hearts_max or HEARTS_DEFAULT_MAX,
        "streak": stats.streak or 0,
        "longest_streak": stats.longest_streak or 0,
        "streak_freezes": stats.streak_freezes or 0,
        "league": league,
        "league_meta": meta,
        "quests": quest_snapshot(db, user, stats),
    }


def _xp_today(db, user) -> int:
    from database.models import LearningProgress
    today = date.today()
    try:
        rows = db.query(LearningProgress).filter(
            LearningProgress.user_id == user.id,
            LearningProgress.module == "learn",
        ).all()
        return sum(r.score or 0 for r in rows if r.created_at and r.created_at.date() == today)
    except Exception:
        return 0


def award_lesson_completion(db, user, stats, *, correct: int, total: int, hearts_remaining: int, combo_max: int) -> Dict[str, Any]:
    """Award XP/gems, best-earn stamps analog: stars based on hearts remaining."""
    base_xp = 10
    combo_bonus = COMBO_BONUS_XP if combo_max >= 5 else 0
    perfect_bonus = 5 if (total > 0 and correct == total) else 0
    xp_total = base_xp + combo_bonus + perfect_bonus

    stats.xp = (stats.xp or 0) + xp_total
    stats.gems = (stats.gems or 0) + (5 if correct == total else 2)
    streak_event = register_daily_activity(db, stats)
    register_weekly_xp(db, user, xp_total)

    # LearningProgress lives on: reuse existing module conventions ('learn')
    from database import crud
    crud.log_learning_progress(
        db=db,
        user_id=user.id,
        module="learn",
        activity=f"Lesson complete ({correct}/{total} correct)",
        score=xp_total,
        language=getattr(user, "current_language", None) or "Tamil",
    )
    bump_quest(db, user, stats, "earn_xp", xp_total)
    bump_quest(db, user, stats, "finish_lessons", 1)
    db.commit()
    return {
        "xp_total": xp_total,
        "base_xp": base_xp,
        "combo_bonus": combo_bonus,
        "perfect_bonus": perfect_bonus,
        "stars": max(1, min(3, hearts_remaining + 1)),
        "streak": stats.streak,
        "streak_state": streak_event.get("state", "same-day"),
        "gems": stats.gems,
    }
