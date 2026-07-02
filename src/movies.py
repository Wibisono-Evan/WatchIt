import requests
import os
import sqlite3
from dotenv import load_dotenv
from src.database import get_connection

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """Search for a movie by title, returns list of results."""
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    movies = data["results"]
    for movie in movies:
        save_movie(movie)
    return movies


def get_movie_details(movie_id):
    """Get full details of a movie by its TMDB ID."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    return response.json()


def get_popular_movies():
    """Fetch current popular movies from TMDB."""
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    movies = data["results"]
    for movie in movies:
        save_movie(movie)
    return movies


def save_movie(movie_item, source="tmdb"):
    conn = get_connection()
    cursor = conn.cursor()

    genre_ids = ",".join(str(g) for g in movie_item["genre_ids"])

    try:
        cursor.execute(
            """INSERT INTO movies 
               (source, source_id, title, overview, release_date, 
                popularity, vote_average, vote_count, genre_ids) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                source,
                movie_item["id"],
                movie_item["title"],
                movie_item["overview"],
                movie_item["release_date"],
                movie_item["popularity"],
                movie_item["vote_average"],
                movie_item["vote_count"],
                genre_ids
            )
        )
        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        cursor.execute(
            "SELECT id FROM movies WHERE source = ? AND source_id = ?",
            (source, movie_item["id"])
        )
        existing = cursor.fetchone()
        return existing["id"]

    finally:
        conn.close()
