import requests
import os
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
    return data["results"]


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
    return data["results"]


def save_movie():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("")
