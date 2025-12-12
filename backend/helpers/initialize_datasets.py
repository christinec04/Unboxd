import os
import json
import re
import pandas as pd
from tqdm import tqdm
from paths import Path

def safe_get(d, keys, default=None):
    """Safely navigate nested dictionaries/lists."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

def initialize_movies_dataset() -> None: 
    """
    Extracts the data from all the json files of the movies dataset into a single csv
    https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies
    """
    clean_title = lambda s: "" if pd.isna(s) else " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    print("preparing dataset...")
    movie_rows = []
    for file in tqdm(os.listdir(Path.MOVIE_DATASET_FOLDER)):
        if not (file.startswith("movies_batch_") and file.endswith(".json")):
            continue
        path = os.path.join(Path.MOVIE_DATASET_FOLDER, file)
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
    movies.to_csv(Path.MOVIES)
    print("done!")


def merge_trending_movies_dataset() -> None:
    """
    Merges the trending movies dataset with the features of the movies dataset
    https://www.kaggle.com/datasets/amitksingh2103/trending-movies-over-the-years
    """
    print("merging trending movies dataset...")
    movies = pd.read_csv(Path.MOVIES)
    trending_movies = pd.read_csv(Path.TRENDING_MOVIES)
    clean_title = lambda s: "" if pd.isna(s) else " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    date_year = lambda date: float(str(date)[:4]) if date else None
    release_years = trending_movies["release_date"].apply(date_year).to_list()
    clean_titles = trending_movies["original_title"].apply(clean_title).to_list()
    title2year = {title:year for title, year in zip(clean_titles, release_years)}
    rows = []
    for movie in movies.itertuples():
        if len(title2year) == 0: 
            break
        clean_title = movie.clean_title
        release_year = movie.release_year
        if clean_title in title2year and title2year[clean_title] == release_year:
            rows.append([
                    movie.original_title, movie.release_year, movie.imdb_id,
                    movie.genres, movie.plot, movie.poster_url
            ])
            title2year.pop(clean_title)
    result = pd.DataFrame(rows, columns=[
        "original_title", "release_year", "imdb_id",
        "genres", "plot", "poster_url"
        ])
    print("saving result...")
    result.to_csv(Path.MERGED_TRENDING_MOVIES)
    print("done!")

initialize_movies_dataset()
merge_trending_movies_dataset()
