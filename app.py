import argparse
import json
import os
from src.database import initialize_db
from src.auth import register_user, user_login
from src.movies import get_popular_movies, search_movie, save_movie
from src.ratings import rate_movie
from src.watch_history import add_to_watch_history
from src.recommender import content_based_filter
from src.database import get_connection


def save_session(user_id):
    with open(".session", "w") as f:
        json.dump({"user_id": user_id}, f)


def load_session():
    try:
        with open(".session") as f:
            return json.load(f)["user_id"]
    except FileNotFoundError:
        return None


def main():
    # Initialize database on every run
    initialize_db()

    parser = argparse.ArgumentParser(description="WatchIt - Movie Recommender")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("register")
    subparsers.add_parser("login")
    subparsers.add_parser("recommend")
    subparsers.add_parser("history")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("title", help="Movie title to search for")

    rate_parser = subparsers.add_parser("rate")
    rate_parser.add_argument("title", help="Movie title to rate")
    rate_parser.add_argument("rating", type=int, help="Rating 1-5")

    args = parser.parse_args()

    # Route to correct function
    if args.command == "register":
        register_user()

    elif args.command == "login":
        user_id = user_login()
        if user_id:
            save_session(user_id)

    elif args.command == "search":
        results = search_movie(args.title)
        if not results:
            print("No movies found.")
        for i, movie in enumerate(results[:5]):
            print(f"{i+1}. {movie['title']} ({movie['release_date'][:4]})")

    elif args.command == "rate":
        user_id = load_session()
        if not user_id:
            print("Please login first.")
            return
        results = search_movie(args.title)
        if not results:
            print("Movie not found.")
            return
        movie = results[0]
        save_movie(movie)
        # Get internal id
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM movies WHERE source_id = ?", (movie["id"],))
        movie_db = cursor.fetchone()
        conn.close()
        rate_movie(user_id, movie_db["id"], args.rating)
        add_to_watch_history(user_id, movie_db["id"])
        print(f"Rated {movie['title']} {args.rating}/5!")

    elif args.command == "recommend":
        user_id = load_session()
        if not user_id:
            print("Please login first.")
            return
        recs = content_based_filter(user_id)
        if not recs:
            print("Rate some movies first to get recommendations!")
            return
        print("\nYour Movie Recommendations:\n")
        for i, movie in enumerate(recs):
            print(f"{i+1}. {movie['title']}")

    elif args.command == "history":
        user_id = load_session()
        if not user_id:
            print("Please login first.")
            return
        from src.watch_history import get_watch_history
        from src.movies import get_movie_by_id
        history = get_watch_history(user_id)
        if not history:
            print("No watch history yet.")
            return
        print("\n📽️  Watch History:\n")
        for row in history:
            movie = get_movie_by_id(row["movie_id"])
            if movie:
                print(f"- {movie['title']} ({row['watched_at']})")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
