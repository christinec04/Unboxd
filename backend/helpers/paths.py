import os
from enum import Enum

class Path(str, Enum):
    data_folder = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "..", "data")
    movie_dataset_folder = os.path.join(data_folder, "movie_dataset")
    movies = os.path.join(data_folder, "movies.csv")
    preprocessed_movies_folder = os.path.join(data_folder, "preprocessed_movies")
    preprocessed_movies = os.path.join(data_folder, "preprocessed_movies.csv")

    trending_movies = os.path.join(data_folder, "trending_movies.csv")
    trending_movie_trailers = os.path.join(data_folder, "trending_movie_trailers.csv")
    merged_trending_movies = os.path.join(data_folder, "merged_trending_movies.csv")
    preprocessed_trending_movies = os.path.join(data_folder, "preprocessed_trending_movies.csv")

    reviews_folder = os.path.join(data_folder, "reviews")
    sentiment_reviews_folder = os.path.join(data_folder, "sentiment_reviews")
    merged_reviews_folder = os.path.join(data_folder, "merged_reviews")

