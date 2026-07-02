from src.movies import get_popular_movies

movies = get_popular_movies()
for index, movie in enumerate(movies):
    print(movie['title'])
