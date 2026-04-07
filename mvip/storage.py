from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(SCHEMA)
        conn.commit()


def create_project(name: str, payload: dict) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects(name, payload) VALUES (?, ?)",
            (name, json.dumps(payload, ensure_ascii=False)),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_projects() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT id, name, created_at FROM projects ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def get_project(project_id: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT id, name, payload FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "payload": json.loads(row[2])}


def update_project(project_id: int, name: str, payload: dict) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "UPDATE projects SET name = ?, payload = ? WHERE id = ?",
            (name, json.dumps(payload, ensure_ascii=False), project_id),
        )
        conn.commit()
        return cur.rowcount > 0


def delete_project(project_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cur.rowcount > 0
