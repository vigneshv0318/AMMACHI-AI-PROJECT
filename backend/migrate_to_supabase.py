"""
Copy every table from the local SQLite database (ammachi.db) into PostgreSQL / Supabase.

Usage (from the backend/ folder, with the venv active):
    python migrate_to_supabase.py                      # uses DATABASE_URL from .env
    python migrate_to_supabase.py "postgresql://..."   # or pass the Supabase URL directly
    python migrate_to_supabase.py --force              # wipe target tables first, then copy

Row IDs are preserved so all relationships stay intact, and ID sequences are reset afterwards.
"""
import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Parents before children, so foreign keys always resolve
TABLE_ORDER = [
    "users",
    "letters",
    "challenges",
    "learning_progress",
    "cultural_stamps",
    "learning_sessions",
    "handwriting_attempts",
    "challenge_participants",
    "challenge_questions",
    "challenge_answers",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Migrate ammachi.db (SQLite) to PostgreSQL / Supabase")
    parser.add_argument("database_url", nargs="?", default=os.getenv("DATABASE_URL"),
                        help="Target PostgreSQL URL (defaults to DATABASE_URL in .env)")
    parser.add_argument("--sqlite", default=os.getenv("DB_FILE", "ammachi.db"), help="Source SQLite file")
    parser.add_argument("--force", action="store_true", help="Delete existing rows in the target tables first")
    return parser.parse_args()


def to_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    text = str(value).strip().replace("T", " ").rstrip("Z")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return datetime.strptime(text[:19], "%Y-%m-%d %H:%M:%S")


def to_json(value):
    if value is None or not isinstance(value, (str, bytes)):
        return value
    try:
        return json.loads(value)
    except ValueError:
        return value


def convert_row(row, table):
    from sqlalchemy import Boolean, DateTime, JSON, String

    out = {}
    for col in table.columns:
        if col.name not in row.keys():
            continue
        value = row[col.name]
        if value is not None:
            if isinstance(col.type, DateTime):
                value = to_datetime(value)
            elif isinstance(col.type, Boolean):
                value = bool(value)
            elif isinstance(col.type, JSON):
                value = to_json(value)
            elif isinstance(col.type, String) and col.type.length and len(str(value)) > col.type.length:
                print(f"   ! {table.name}.{col.name} id={row['id']}: value longer than {col.type.length} chars, truncated")
                value = str(value)[: col.type.length]
        out[col.name] = value
    return out


def main():
    args = parse_args()
    if not args.database_url or args.database_url.startswith("sqlite"):
        sys.exit("Set DATABASE_URL in backend/.env to your Supabase PostgreSQL URL (or pass it as an argument).")
    if not os.path.exists(args.sqlite):
        sys.exit(f"SQLite source not found: {args.sqlite}")

    # database.connection builds its engine from DATABASE_URL at import time
    os.environ["DATABASE_URL"] = args.database_url
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sqlalchemy import text
    from database.connection import Base, engine, IS_SQLITE
    from database import models, handwriting_models  # noqa: F401  (registers all tables on Base)

    if IS_SQLITE:
        sys.exit("Target URL resolved to SQLite; expected PostgreSQL.")

    print(f"Source : {os.path.abspath(args.sqlite)}")
    print(f"Target : {engine.url.render_as_string(hide_password=True)}\n")

    src = sqlite3.connect(args.sqlite)
    src.row_factory = sqlite3.Row
    src_tables = {r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table'")}

    Base.metadata.create_all(bind=engine)
    tables = [Base.metadata.tables[name] for name in TABLE_ORDER]

    with engine.begin() as conn:
        existing = {t.name: conn.execute(text(f'SELECT COUNT(*) FROM "{t.name}"')).scalar() for t in tables}
        if any(existing.values()):
            if not args.force:
                filled = ", ".join(f"{k}={v}" for k, v in existing.items() if v)
                sys.exit(f"Target already has data ({filled}). Re-run with --force to replace it.")
            names = ", ".join(f'"{t.name}"' for t in tables)
            conn.execute(text(f"TRUNCATE {names} RESTART IDENTITY CASCADE"))
            print("Cleared existing target data (--force).\n")

        copied_ids = {}
        summary = []
        for table in tables:
            if table.name not in src_tables:
                summary.append((table.name, 0, 0, 0))
                continue

            rows = src.execute(f'SELECT * FROM "{table.name}" ORDER BY 1').fetchall()
            batch, skipped = [], 0
            for row in rows:
                record = convert_row(row, table)
                # Skip rows whose parent row does not exist (SQLite never enforced these links)
                orphan = False
                for fk in table.foreign_keys:
                    parent = fk.column.table.name
                    value = record.get(fk.parent.name)
                    if value is not None and parent in copied_ids and value not in copied_ids[parent]:
                        orphan = True
                        break
                if orphan:
                    skipped += 1
                    continue
                batch.append(record)

            if batch:
                conn.execute(table.insert(), batch)
            copied_ids[table.name] = {r["id"] for r in batch}
            summary.append((table.name, len(rows), len(batch), skipped))

        # Make new rows continue after the highest copied ID
        for table in tables:
            pk = table.primary_key.columns.values()[0]
            if pk.type.python_type is int:
                conn.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('\"{table.name}\"', '{pk.name}'), "
                    f"COALESCE(MAX(\"{pk.name}\"), 1), MAX(\"{pk.name}\") IS NOT NULL) FROM \"{table.name}\""
                ))

        print(f"{'table':26} {'sqlite':>7} {'copied':>7} {'skipped':>8} {'in target':>10}")
        ok = True
        for name, n_src, n_copied, n_skipped in summary:
            n_target = conn.execute(text(f'SELECT COUNT(*) FROM "{name}"')).scalar()
            ok &= n_target == n_copied
            print(f"{name:26} {n_src:>7} {n_copied:>7} {n_skipped:>8} {n_target:>10}")

    src.close()
    print("\nMigration complete." if ok else "\nWARNING: row counts do not match, check the output above.")


if __name__ == "__main__":
    main()
