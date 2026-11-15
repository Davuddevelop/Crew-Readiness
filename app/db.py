"""SQLite connection handling (one connection per request, closed on teardown)."""
from __future__ import annotations

import sqlite3

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Drop and recreate every table. Destroys data — used by reset/seed only."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))
    db.commit()


def is_initialized() -> bool:
    row = get_db().execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'profiles'"
    ).fetchone()
    return row is not None


def init_app(app) -> None:
    app.teardown_appcontext(close_db)


def ensure_columns() -> None:
    """Add columns introduced after a database was created (the prototype has no migrations)."""
    db = get_db()
    have = {r["name"] for r in db.execute("PRAGMA table_info(sessions)")}
    if "accepted_at" not in have:
        db.execute("ALTER TABLE sessions ADD COLUMN accepted_at TEXT")
        db.commit()
    have_att = {r["name"] for r in db.execute("PRAGMA table_info(attention_results)")}
    if have_att and "lapse_count" not in have_att:
        db.execute("ALTER TABLE attention_results ADD COLUMN lapse_count INTEGER NOT NULL DEFAULT 0")
        db.commit()
