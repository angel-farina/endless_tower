import os
import sqlite3

def _db_path(db_path=None):
    if db_path is not None:
        return db_path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "scores.db")

def create_scores_table(db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)")

def save_score(name, score, db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(score), 0) FROM scores")
        current_highest = cursor.fetchone()[0]
        score = int(score)
        if score > current_highest:
            cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()

def check_if_table_exists(db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scores'")
        return cursor.fetchone() is not None

def get_highest_score(db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(score), 0) FROM scores")
        result = cursor.fetchone()
        return result[0] if result else 0

def get_highscore_name(db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM scores ORDER BY score DESC, rowid ASC LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else "N/A"

def get_top_scores(limit=5, db_path=None):
    db_path = _db_path(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, score FROM scores ORDER BY score DESC, rowid ASC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()
