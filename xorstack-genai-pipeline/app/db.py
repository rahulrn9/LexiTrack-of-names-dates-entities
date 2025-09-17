import sqlite3
from pathlib import Path
from typing import Iterable, Dict

DB_PATH = Path(__file__).resolve().parents[1] / "outputs" / "results.db"

DDL = """
CREATE TABLE IF NOT EXISTS extractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    entity_type TEXT,
    entity_text TEXT,
    normalized TEXT,
    start_char INTEGER,
    end_char INTEGER,
    processed_at TEXT
);
"""

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(DDL)
    return conn

def insert_rows(rows: Iterable[Dict]):
    conn = get_conn()
    with conn:
        conn.executemany(
            """
            INSERT INTO extractions (filename, entity_type, entity_text, normalized, start_char, end_char, processed_at)
            VALUES (:filename, :entity_type, :entity_text, :normalized, :start_char, :end_char, :processed_at)
            """,
            list(rows)
        )
    conn.close()
