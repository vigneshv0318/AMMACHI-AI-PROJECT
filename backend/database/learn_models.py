from datetime import datetime

try:
    from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
    from sqlalchemy.orm import relationship
    from database.connection import Base

    if Base is not None:
        class UserStats(Base):
            """Duolingo-style gamification stats per user (XP, gems, hearts, streak)."""
            __tablename__ = "user_stats"

            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
            xp = Column(Integer, default=0)                     # lifetime XP (= points earned via lessons)
            gems = Column(Integer, default=0)                   # soft currency
            hearts = Column(Integer, default=5)                 # lesson lives (max 5)
            hearts_max = Column(Integer, default=5)
            streak = Column(Integer, default=0)                 # consecutive days with activity
            longest_streak = Column(Integer, default=0)
            daily_goal = Column(Integer, default=20)            # daily XP goal
            streak_freezes = Column(Integer, default=0)         # items owned
            last_active_date = Column(String(10), nullable=True)   # 'YYYY-MM-DD'
            hearts_refill_at = Column(DateTime, nullable=True)     # pending heart regen timestamp
            weekly_xp = Column(Integer, default=0)              # XP earned this league week
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        class LearnUnit(Base):
            """A section-level unit on the learning path ('Introduce yourself')."""
            __tablename__ = "learn_units"

            id = Column(Integer, primary_key=True, index=True)
            language = Column(String(50), nullable=False, index=True)
            order = Column(Integer, default=0)
            title = Column(String(150), nullable=False)
            description = Column(String(300), nullable=True)
            color = Column(String(30), default="blue")

            nodes = relationship("LearnNode", back_populates="unit", cascade="all, delete-orphan")

        class LearnNode(Base):
            """A single interactive node on the path: lesson / story / practice / chest / unit_review."""
            __tablename__ = "learn_nodes"

            id = Column(Integer, primary_key=True, index=True)
            unit_id = Column(Integer, ForeignKey("learn_units.id", ondelete="CASCADE"), nullable=False)
            order = Column(Integer, default=0)
            node_type = Column(String(30), default="lesson")  # lesson, story, practice, chest, unit_review
            title = Column(String(150), nullable=True)        # optional label (e.g., 'Personalized practice')
            topic = Column(String(150), nullable=True)        # content topic hint used by generators

            unit = relationship("LearnUnit", back_populates="nodes")

        class NodeProgress(Base):
            """Per-user completion state for each path node."""
            __tablename__ = "node_progress"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            node_id = Column(Integer, ForeignKey("learn_nodes.id", ondelete="CASCADE"), nullable=False)
            completed = Column(Boolean, default=False)
            stars = Column(Integer, default=0)               # 1..3 based on hearts remaining
            best_score = Column(Integer, default=0)          # percent
            attempts = Column(Integer, default=0)
            last_completed_at = Column(DateTime, nullable=True)

        class LessonAttempt(Base):
            """One run through a node's exercises (Duolingo-style lesson player)."""
            __tablename__ = "lesson_attempts"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            node_id = Column(Integer, ForeignKey("learn_nodes.id", ondelete="CASCADE"), nullable=True)
            status = Column(String(20), default="ACTIVE")    # ACTIVE, COMPLETED, ABANDONED
            exercises = Column(JSON, nullable=True)          # ordered exercise list
            results = Column(JSON, nullable=True)            # [{exercise_id, correct, tries}]
            current_index = Column(Integer, default=0)
            correct_count = Column(Integer, default=0)
            wrong_count = Column(Integer, default=0)
            combo_max = Column(Integer, default=0)
            combo_current = Column(Integer, default=0)
            hearts_lost = Column(Integer, default=0)
            xp_awarded = Column(Integer, default=0)
            language = Column(String(50), default="Tamil")
            created_at = Column(DateTime, default=datetime.utcnow)
            completed_at = Column(DateTime, nullable=True)

        class QuestProgress(Base):
            """Daily quest progress (resets every day): earn XP, finish lessons, answer correctly."""
            __tablename__ = "quest_progress"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            date = Column(String(10), nullable=False)        # 'YYYY-MM-DD'
            quest_type = Column(String(40), nullable=False)  # earn_xp, finish_lessons, correct_answers
            progress = Column(Integer, default=0)
            target = Column(Integer, default=10)
            claimed = Column(Boolean, default=False)

        class WeeklyXp(Base):
            """XP earned per ISO week – powers the league leaderboard."""
            __tablename__ = "weekly_xp"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            week = Column(String(12), nullable=False, index=True)  # e.g. '2026-W42'
            xp = Column(Integer, default=0)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    else:
        UserStats = None
        LearnUnit = None
        LearnNode = None
        NodeProgress = None
        LessonAttempt = None
        QuestProgress = None
        WeeklyXp = None

except Exception:
    UserStats = None
    LearnUnit = None
    LearnNode = None
    NodeProgress = None
    LessonAttempt = None
    QuestProgress = None
    WeeklyXp = None
