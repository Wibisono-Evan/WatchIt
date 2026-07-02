import sqlite3
from src.database import get_connection


def rate_movie(user_id, movie_id, rating):
    # Validate rating range
    if rating < 1 or rating > 5:
        print("Rating must be between 1 and 5.")
        return None

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)",
            (user_id, movie_id, rating)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_user_rating(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM ratings WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()
