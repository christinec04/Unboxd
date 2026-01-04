import os
from enum import Enum

file_abs_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class Path(str, Enum):
    DATA_FOLDER = os.path.join(file_abs_path, "..", "data")
    MOVIE_DATASET_FOLDER = os.path.join(DATA_FOLDER, "movie_dataset")
    MOVIES_FOLDER = os.path.join(DATA_FOLDER, "movies")
    PREPROCESSED_MOVIES_FOLDER = os.path.join(DATA_FOLDER, "preprocessed_movies")
    REDUCED_PREPROCESSED_MOVIES_FOLDER = os.path.join(DATA_FOLDER, "reduced_preprocessed_movies")

    RATINGS_FOLDER = os.path.join(DATA_FOLDER, "ratings")
    MERGED_RATINGS_FOLDER = os.path.join(DATA_FOLDER, "merged_ratings")

    DATABASE = os.path.join(DATA_FOLDER, "sqlite3.db")
    PREPROCESSED_MOVIE_MODEL = os.path.join(file_abs_path, "preprocessed_movie_model.py")
