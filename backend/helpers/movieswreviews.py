import os
import sys
import pandas as pd
import re

def merge_sentiment_reviews_dataset(movies: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    """Merges the features of `movies` with `reviews`, the result of sentiment analysis"""
    movie_choices = set(movies["clean_title"].tolist())
    clean_title = lambda s: "" if pd.isna(s) else re.sub(r"\s+[^a-z0-9]", " ", s.lower()).strip()
    best_match = lambda x: x if x in movie_choices else None
    reviews["other_clean_title"] = reviews["name"].apply(clean_title)
    reviews["matched_title"] = reviews["other_clean_title"].apply(best_match)
    merged = reviews.merge(
        movies,
        left_on="matched_title",
        right_on="clean_title",
        how="left"
    )
    merged = merged.query("release_year == year")
    result = merged[[
        "original_title",
        "clean_title",
        "release_year",
        "imdb_id",
        "runtime_seconds",
        "certificate_rating",
        "genres",
        "directors",
        "writers",
        "actors",
        "companies",
        "poster_url",
        "plot",
        "compound",
        "user_rating",
        "user_review",
        ]].reset_index(drop=True)
    return result

if __name__ == "__main__":
    username = sys.argv[1]
    movies = pd.read_csv(os.path.join(os.getcwd(), "..", "data", "movies.csv"))
    reviews = pd.read_csv(os.path.join(os.getcwd(), "..", "data", "sentiment_reviews", f"{username}.csv"))
    merged_reviews = merge_sentiment_reviews_dataset(movies, reviews)
    merged_reviews.to_csv(os.path.join(os.getcwd(), "..", "data", "merged_reviews", f"{username}.csv"))
