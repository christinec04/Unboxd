import os
import json
import pandas as pd
import re
from pandas.core.internals.managers import create_block_manager_from_column_arrays
from tqdm import tqdm
import ast
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

trending_movies_path = os.path.join(os.getcwd(), "data", "trending_movies.csv")
movies_folder_path = os.path.join(os.getcwd(), "data", "movie_dataset")
movies_path = os.path.join(os.getcwd(), "data", "movies.csv")
merged_trending_movies_path = os.path.join(os.getcwd(), "data", "merged_trending_movies.csv")

def safe_get(d, keys, default=None):
    """Safely navigate nested dictionaries/lists."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

def initialize_movies_dataset() -> None: 
    """Extracts the data from all the json files of the movies dataset into a single csv"""
    print("preparing dataset...")
    clean_title = lambda s: "" if pd.isna(s) else re.sub(r"\s+[^a-z0-9]", " ", s.lower()).strip()
    movie_rows = []
    for file in tqdm(os.listdir(movies_folder_path)):
        if not (file.startswith("movies_batch_") and file.endswith(".json")):
            continue
        path = os.path.join(movies_folder_path, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for movie in data:
            title = safe_get(movie, ["titleText", "text"], "")
            original_title = safe_get(movie, ["originalTitleText", "text"], title)
            release_year = safe_get(movie, ["releaseYear", "year"], "")
            imdb_id = safe_get(movie, ["id"], "")
            runtime_seconds = safe_get(movie, ["runtime", "seconds"], "")
            certificate_rating = safe_get(movie, ["certificate", "rating"], "")
            genres = [safe_get(g, ["text"], "") for g in safe_get(movie, ["genres", "genres"], [])]
            plot = safe_get(movie, ["plot", "plotText", "plainText"], "")
            directors, writers, actors = [], [], []
            principal_credits = safe_get(movie, ["principalCredits"], [])
            categories = { "Director": directors, "Writers": writers, "Stars": actors }
            for pc in principal_credits:
                category = safe_get(pc, ["category", "text"], "") 
                if category not in categories:
                    continue
                names = [safe_get(p, ["name", "nameText", "text"], "") for p in safe_get(pc, ["credits"], [])]
                categories[category].extend(names)
            company_credits = safe_get(movie, ["companyCredits", "edges"], [])
            companies = [safe_get(cc, ["node", "company", "companyText", "text"], "") for cc in company_credits]
            poster_url = safe_get(movie, ["primaryImage", "url"], "")
            movie_rows.append({
                "original_title": original_title,
                "clean_title": clean_title(original_title),
                "release_year": release_year,
                "imdb_id": imdb_id,
                "runtime_seconds": runtime_seconds,
                "certificate_rating": certificate_rating,
                "genres": genres,
                "plot": plot,
                "directors": directors,
                "writers": writers,
                "actors": actors,
                "companies": companies,
                "poster_url": poster_url,
            })
    print("saving dataset...")
    movies = pd.DataFrame(movie_rows)
    movies.to_csv(movies_path)
    print("done!")

def merge_trending_movies_dataset() -> None:
    """Merges the trending movies dataset with the features of the movies dataset"""
    print("merging trending movies dataset...")
    movies = pd.read_csv(movies_path)
    movie_choices = set(movies["clean_title"].tolist())
    trending_movies = pd.read_csv(trending_movies_path)
    clean_title = lambda s: "" if pd.isna(s) else re.sub(r"\s+[^a-z0-9]", " ", s.lower()).strip()
    date_year = lambda date: float(str(date)[:4]) if date else None
    best_match = lambda x: x if x in movie_choices else None
    trending_movies["year"] = trending_movies["release_date"].apply(date_year)
    trending_movies["other_clean_title"] = trending_movies["original_title"].apply(clean_title)
    # to avoid conflicting column names when merging datasets
    trending_movies = trending_movies.rename(columns={ "original_title": "og_title" })
    trending_movies["matched_title"] = trending_movies["other_clean_title"].apply(best_match)
    merged = trending_movies.merge(
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
        ]].reset_index(drop=True)
    result.to_csv(merged_trending_movies_path)
    print("done!")

if __name__ == "__main__":
    initialize_movies_dataset()
    merge_trending_movies_dataset()