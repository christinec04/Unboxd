import os
import json
import pandas as pd
import re
from thefuzz import process, fuzz

def clean_title(s):
    if pd.isna(s):
        return ""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def safe_get(d, keys, default=None):
    """Safely navigate nested dictionaries/lists."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

movies_folder = r"C:\Users\zhang\School\B365\Project-ez2-ermili-cch8-dvchavan\movie_dataset\movie_dataset"

movie_rows = []

for file in os.listdir(movies_folder):
    if file.startswith("movies_batch_") and file.endswith(".json"):
        print("Loading:", file) 
        path = os.path.join(movies_folder, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for movie in data:
            title = safe_get(movie, ["titleText", "text"], "")
            original_title = safe_get(movie, ["originalTitleText", "text"], title)
            imdb_id = movie.get("id", "")

            genres = safe_get(movie, ["genres", "genres"], [])
            genres = ", ".join([g.get("text", "") for g in genres]) if isinstance(genres, list) else ""

            plot = safe_get(movie, ["plot", "plotText", "plainText"], "")

            directors = safe_get(movie, ["credits", "crewmembers"], [])
            if isinstance(directors, list):
                directors = [p.get("name", {}).get("nameText", {}).get("text", "") for p in directors if p.get("category") == "director"]
                directors = ", ".join([d for d in directors if d])
            else:
                directors = ""

            writers = safe_get(movie, ["credits", "crewmembers"], [])
            if isinstance(writers, list):
                writers = [p.get("name", {}).get("nameText", {}).get("text", "") for p in writers if p.get("category") == "writer"]
                writers = ", ".join([w for w in writers if w])
            else:
                writers = ""

            actors = safe_get(movie, ["credits", "cast"], [])
            if isinstance(actors, list):
                actors = [a.get("name", {}).get("nameText", {}).get("text", "") for a in actors]
                actors = ", ".join([a for a in actors if a])
            else:
                actors = ""

            companies = safe_get(movie, ["production", "companies"], [])
            if isinstance(companies, list):
                companies = ", ".join([c.get("company", {}).get("text", "") for c in companies])
            else:
                companies = ""

            movie_rows.append({
                "imdb_id": imdb_id,
                "title": title,
                "original_title": original_title,
                "clean_title": clean_title(original_title),
                "genres": genres,
                "plot": plot,
                "directors": directors,
                "writers": writers,
                "actors": actors,
                "companies": companies
            })


movies = pd.DataFrame(movie_rows)

reviews_path = r"C:\Users\zhang\School\B365\Project-ez2-ermili-cch8-dvchavan\processed_reviews\deathproof_sentiment.csv"
reviews = pd.read_csv(reviews_path)
reviews["clean_title"] = reviews["name"].apply(clean_title)

movie_choices = movies["clean_title"].tolist()

def best_match(x):
    if not x or x.strip() == "":
        return None
    match, score = process.extractOne(x, movie_choices, scorer=fuzz.WRatio)
    if score < 92:
        return None
    return match

reviews["matched_title"] = reviews["clean_title"].apply(best_match)

merged = reviews.merge(
    movies,
    left_on="matched_title",
    right_on="clean_title",
    how="left"
)

output_path = r"C:\Users\zhang\School\B365\Project-ez2-ermili-cch8-dvchavan\merged_reviews\deathproof_sentiment_merged.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged.to_csv(output_path, index=False)
