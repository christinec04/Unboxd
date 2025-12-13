import os
from enum import Enum

class Path(str, Enum):
    DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "..", "data")
    MOVIE_DATASET_FOLDER = os.path.join(DATA_FOLDER, "movie_dataset")
    MOVIES = os.path.join(DATA_FOLDER, "movies.csv")
    PREPROCESSED_MOVIES_FOLDER = os.path.join(DATA_FOLDER, "preprocessed_movies")
    PREPROCESSED_MOVIES = os.path.join(DATA_FOLDER, "preprocessed_movies.csv")

    TRENDING_MOVIES = os.path.join(DATA_FOLDER, "trending_movies.csv")
    TRENDING_MOVIE_TRAILERS = os.path.join(DATA_FOLDER, "trending_movie_trailers.csv")
    MERGED_TRENDING_MOVIES = os.path.join(DATA_FOLDER, "merged_trending_movies.csv")
    PREPROCESSED_TRENDING_MOVIES = os.path.join(DATA_FOLDER, "preprocessed_trending_movies.csv")

    REVIEWS_FOLDER = os.path.join(DATA_FOLDER, "reviews")
    SENTIMENT_REVIEWS_FOLDER = os.path.join(DATA_FOLDER, "sentiment_reviews")
    MERGED_REVIEWS_FOLDER = os.path.join(DATA_FOLDER, "merged_reviews")
