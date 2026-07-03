import sqlite3
from src.database import get_connection


def add_to_watch_history(user_id, movie_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO watch_history (user_id, movie_id) VALUES (?,?)",
                       (user_id, movie_id))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_watch_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM watch_history WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()
