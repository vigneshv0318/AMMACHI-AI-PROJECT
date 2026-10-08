# Compatibility proxy for backend/database package
from database.connection import init_db, get_db, Base, engine, SessionLocal
from database.crud import (
    get_user_by_username as get_user,
    get_user_by_google_id,
    create_user,
    verify_password,
    update_user_points_and_stamp as update_score,
    log_learning_progress,
    get_user_progress_summary,
)
