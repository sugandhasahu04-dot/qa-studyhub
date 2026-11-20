"""Database layer.

On Vercel: uses Postgres (Neon / Vercel Postgres) from the DATABASE_URL or POSTGRES_URL env var.
Locally (no env var): uses a SQLite file, so you can run the app without any setup.
Queries are written with "?" placeholders and converted for Postgres automatically.
"""
import os
import sqlite3
from contextlib import contextmanager

DB_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
IS_PG = bool(DB_URL and DB_URL.startswith(("postgres://", "postgresql://")))

SQLITE_PATH = os.environ.get(
    "SQLITE_PATH",
    "/tmp/studyhub.db" if os.environ.get("VERCEL") else os.path.join(os.path.dirname(__file__), "..", "local.db"),
)

if IS_PG:
    import psycopg2
    import psycopg2.extras

ID_COL = "SERIAL PRIMARY KEY" if IS_PG else "INTEGER PRIMARY KEY AUTOINCREMENT"
NOW = "CURRENT_TIMESTAMP"

SCHEMA = [
    f"""CREATE TABLE IF NOT EXISTS notes (
        id {ID_COL},
        topic TEXT NOT NULL DEFAULT 'general',
        title TEXT NOT NULL,
        body TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMP DEFAULT {NOW},
        updated_at TIMESTAMP DEFAULT {NOW}
    )""",
    f"""CREATE TABLE IF NOT EXISTS resources (
        id {ID_COL},
        topic TEXT NOT NULL,
        kind TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT {NOW}
    )""",
    f"""CREATE TABLE IF NOT EXISTS quiz_attempts (
        id {ID_COL},
        topic TEXT NOT NULL,
        quiz_type TEXT NOT NULL,
        level TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT {NOW}
    )""",
    f"""CREATE TABLE IF NOT EXISTS lesson_progress (
        topic TEXT PRIMARY KEY,
        completed_at TIMESTAMP DEFAULT {NOW}
    )""",
    # Spaced-repetition flashcards (SM-2). key is unique so built-in / mistake cards aren't duplicated.
    f"""CREATE TABLE IF NOT EXISTS cards (
        id {ID_COL},
        key TEXT UNIQUE NOT NULL,
        topic TEXT NOT NULL,
        front TEXT NOT NULL,
        back TEXT NOT NULL,
        source TEXT NOT NULL DEFAULT 'builtin',
        ease REAL NOT NULL DEFAULT 2.5,
        interval_days INTEGER NOT NULL DEFAULT 0,
        reps INTEGER NOT NULL DEFAULT 0,
        lapses INTEGER NOT NULL DEFAULT 0,
        due TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT {NOW}
    )""",
    f"""CREATE TABLE IF NOT EXISTS reviews (
        id {ID_COL},
        card_id INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        day TEXT NOT NULL,
        reviewed_at TIMESTAMP DEFAULT {NOW}
    )""",
    """CREATE TABLE IF NOT EXISTS activity (
        day TEXT PRIMARY KEY
    )""",
    # Where you are inside a guided lesson, so you can stop and resume on any device.
    f"""CREATE TABLE IF NOT EXISTS learn_state (
        topic TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT {NOW}
    )""",
]

_initialized = False


def _connect():
    if IS_PG:
        url = DB_URL
        if "sslmode" not in url:
            url += ("&" if "?" in url else "?") + "sslmode=require"
        return psycopg2.connect(url)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_conn():
    global _initialized
    conn = _connect()
    try:
        if not _initialized:
            cur = conn.cursor()
            for stmt in SCHEMA:
                cur.execute(stmt)
            conn.commit()
            _initialized = True
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _sql(q):
    return q.replace("?", "%s") if IS_PG else q


def query(q, params=(), one=False):
    with get_conn() as conn:
        if IS_PG:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = conn.cursor()
        cur.execute(_sql(q), params)
        rows = [dict(r) for r in cur.fetchall()]
    return (rows[0] if rows else None) if one else rows


def execute(q, params=()):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(_sql(q), params)
        return cur.rowcount
