from src.ratings import get_user_rating
from src.database import get_connection
from src.watch_history import get_watch_history
from collections import Counter


def get_seen_movie_ids(user_id):
    rated = [row["movie_id"] for row in get_user_rating(user_id)]
    watched = [row["movie_id"] for row in get_watch_history(user_id)]
    return set(rated + watched)


def content_based_filter(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT movies.genre_ids, ratings.rating FROM ratings JOIN movies ON ratings.movie_id = movies.id WHERE ratings.user_id = ? AND ratings.rating >= 4", (user_id,))
        result = cursor.fetchall()

        liked_genres = []
        for row in result:
            genres = [int(g) for g in row["genre_ids"].split(",") if g.strip()]
            liked_genres.extend(genres)
        genre_counts = Counter(liked_genres)

        # Top genres watched by user.
        top_genres = set(g for g, count in genre_counts.most_common(3))

        # ELIMINATE: Movies the user has rated
        cursor.execute(
            "SELECT movie_id FROM ratings WHERE user_id = ?", (user_id,))
        rated = [row["movie_id"] for row in cursor.fetchall()]

        # ELIMINATE: Movies the user has watched
        cursor.execute(
            "SELECT movie_id FROM watch_history WHERE user_id = ?", (user_id,))
        watched = [row["movie_id"] for row in cursor.fetchall()]

        # Find movies from databse with genres in top genres but never rated or watched
        cursor.execute("SELECT * FROM movies")
        all_movies = cursor.fetchall()
        seen_ids = set(rated + watched)
        candidates = []

        for movie in all_movies:
            if movie["id"] in seen_ids:
                continue

            movie_genres = set(int(g)
                               for g in movie["genre_ids"].split(",") if g.strip())
            overlap = movie_genres & top_genres

            if overlap:
                candidates.append({
                    "movie": movie,
                    "score": len(overlap)
                })

        # Give top ten movies
        sorted_movies = sorted(
            candidates, key=lambda x: x["score"], reverse=True)
        return [item["movie"] for item in sorted_movies[:10]]
    finally:
        conn.close()
