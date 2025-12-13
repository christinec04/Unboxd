import os
import sys
import re
import pandas as pd


def merge_sentiment_reviews_dataset(movies: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    """Merges the features of `movies` with `reviews`: the result of sentiment analysis"""
    clean_title = lambda s: "" if pd.isna(s) else " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    information = reviews[["year", "compound", "user_rating"]].itertuples()
    clean_titles = reviews["name"].apply(clean_title).to_list()
    title2info = {title:info for title, info in zip(clean_titles, information)}
    rows = []
    for movie in movies.itertuples():
        clean_title = movie.clean_title
        release_year = movie.release_year
        if clean_title in title2info and float(title2info[clean_title].year) == release_year:
            rows.append([
                    movie.imdb_id,
                    title2info[clean_title].compound,
                    title2info[clean_title].user_rating
            ])
            title2info.pop(clean_title)
    result = pd.DataFrame(rows, columns=["imdb_id", "compound", "user_rating"])
    return result

if __name__ == "__main__":
    from paths import Path
    username = sys.argv[1]
    movies = pd.read_csv(os.path.join(Path.MOVIES))
    sentiment_reviews = pd.read_csv(os.path.join(Path.SENTIMENT_REVIEWS_FOLDER, f"{username}.csv"))
    merged_reviews = merge_sentiment_reviews_dataset(movies, sentiment_reviews)
    merged_reviews.to_csv(os.path.join(Path.MERGED_REVIEWS_FOLDER, f"{username}.csv"))
