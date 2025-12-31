import os
import sys
import re
import pandas as pd

def merge_ratings_dataset(movies: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the IMDb ids and user ratings of the movies from `ratings`, the result of 
    scraping Letterboxd for user ratings, that were successfully merged with `movies`
    """
    clean_title = lambda s: "" if pd.isna(s) else " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    years_and_ratings = ratings[["release_year", "user_rating"]].itertuples()
    clean_titles = ratings["original_title"].apply(clean_title).to_list()
    title2info = { title:info for title, info in zip(clean_titles, years_and_ratings) }
    rows = []
    for movie in movies.itertuples():
        clean_title = movie.clean_title
        release_year = movie.release_year
        if clean_title in title2info and float(title2info[clean_title].release_year) == release_year:
            rows.append([movie.imdb_id, movie.original_title, title2info[clean_title].user_rating])
            title2info.pop(clean_title)
    result = pd.DataFrame(rows, columns=["imdb_id", "original_title", "user_rating"])
    return result

def obtain_ids_and_weights(movies: pd.DataFrame, ratings: pd.DataFrame) -> tuple[set[str], list[float]]:
    """
    Returns the IMDB ids and user ratings, with missing values imputed via mean, of the 
    movies resulting from merging `ratings` with `movies`
    """
    merged_ratings = merge_ratings_dataset(movies, ratings)
    movie_ids = set(merged_ratings["imdb_id"].values)
    weights = merged_ratings["user_rating"].fillna(merged_ratings["user_rating"].mean()).to_list()
    return (movie_ids, weights)

if __name__ == "__main__":
    from paths import Path
    username = sys.argv[1]
    movies = pd.read_csv(os.path.join(Path.MOVIES), index_col=False)
    ratings = pd.read_csv(os.path.join(Path.RATINGS_FOLDER, f"{username}.csv"), index_col=False)
    merged_ratings = merge_ratings_dataset(movies, ratings)
    os.makedirs(Path.MERGED_RATINGS_FOLDER, exist_ok=True)
    merged_ratings.to_csv(os.path.join(Path.MERGED_RATINGS_FOLDER, f"{username}.csv"), index=False)
