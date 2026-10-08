import os
import sqlite3
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("ammachi.database")

DATABASE_URL = os.getenv("DATABASE_URL")
DB_FILE = os.getenv("DB_FILE", "ammachi.db")

# Try to import SQLAlchemy
HAS_SQLALCHEMY = False
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker
    
    if not DATABASE_URL:
        DATABASE_URL = f"sqlite:///./{DB_FILE}"
    else:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+psycopg://"):
            DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)
    else:
        connect_args = {
            # Supabase's transaction pooler (PgBouncer, port 6543) does not support prepared statements
            "prepare_threshold": None,
        }
        if "supabase" in DATABASE_URL and "sslmode=" not in DATABASE_URL:
            connect_args["sslmode"] = "require"
        engine = create_engine(
            DATABASE_URL,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=5,
            pool_recycle=300,
        )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    HAS_SQLALCHEMY = True
    logger.info("SQLAlchemy initialized with: %s", engine.url.render_as_string(hide_password=True))
except Exception as e:
    logger.warning("SQLAlchemy init note: %s. Using direct DB adapter.", e)
    Base = None
    engine = None
    SessionLocal = None

# True when the app runs on the local SQLite file; False for PostgreSQL / Supabase
IS_SQLITE = engine is None or engine.url.get_backend_name() == "sqlite"

class DirectDBSession:
    """Standard database session adapter supporting direct transactions."""
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, params=()):
        c = self.conn.cursor()
        c.execute(query, params)
        return c

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

def get_db():
    """FastAPI dependency for database session."""
    if HAS_SQLALCHEMY and SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        session = DirectDBSession()
        try:
            yield session
        finally:
            session.close()

def init_db():
    """Initializes and migrates tables for User, LearningProgress, CulturalStamps, and Sessions."""
    if not IS_SQLITE:
        _init_postgres()
        return

    if HAS_SQLALCHEMY and Base and engine:
        try:
            from database import models, handwriting_models
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            logger.warning("Base metadata create_all warning: %s", e)

    # Ensure SQLite tables and perform migration if table exists from prototype
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Check existing users table columns
    c.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in c.fetchall()}

    if cols and "id" not in cols:
        # Table exists from legacy prototype without id column -> perform migration
        logger.info("Migrating legacy users table to new production schema...")
        c.execute("ALTER TABLE users RENAME TO users_old")
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            google_id TEXT UNIQUE,
            points INTEGER DEFAULT 0,
            current_language TEXT DEFAULT 'Tamil',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''INSERT INTO users (username, password_hash, google_id, points)
                     SELECT username, password_hash, google_id, points FROM users_old''')
        c.execute("DROP TABLE users_old")
        conn.commit()
    elif not cols:
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            google_id TEXT UNIQUE,
            points INTEGER DEFAULT 0,
            current_language TEXT DEFAULT 'Tamil',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

    c.execute('''CREATE TABLE IF NOT EXISTS learning_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        module TEXT NOT NULL,
        activity TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        language TEXT DEFAULT 'Tamil',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS cultural_stamps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stamp_name TEXT NOT NULL,
        badge_icon TEXT DEFAULT '🪔',
        earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS learning_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        module TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        session_metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Bootstrap default student user if not exists or has no password
    c.execute("SELECT id, password_hash FROM users WHERE username='student'")
    row = c.fetchone()
    from database.crud import hash_password
    hashed = hash_password("password123")
    if not row:
        c.execute("INSERT INTO users (username, password_hash, points, current_language) VALUES (?, ?, ?, ?)",
                  ("student", hashed, 0, "Tamil"))
        conn.commit()
    elif row[1] is None:
        c.execute("UPDATE users SET password_hash=? WHERE username='student'", (hashed,))
        conn.commit()

    conn.close()
    logger.info("Database tables initialized and verified.")

def _init_postgres():
    """Create all tables on PostgreSQL (e.g. Supabase) and bootstrap the default student user."""
    from database import models, handwriting_models
    from database.crud import hash_password

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        student = db.query(models.User).filter(models.User.username == "student").first()
        if not student:
            db.add(models.User(username="student", password_hash=hash_password("password123"),
                               points=0, current_language="Tamil"))
            db.commit()
        elif student.password_hash is None:
            student.password_hash = hash_password("password123")
            db.commit()
    finally:
        db.close()
    logger.info("PostgreSQL tables initialized and verified.")
