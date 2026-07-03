from src.ratings import get_user_rating
from src.database import get_connection


def content_based_filter(user_id):
    user_ratings = get_user_rating(user_id)
    for rating in user_ratings:
        if rating["rating"] == 4 or rating["rating"] == 5:
