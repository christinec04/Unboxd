import os
import shutil
import json
import pandas as pd
from paths import Path
import math
from typing import Iterable, Any
from pydantic import BaseModel
from multiprocessing import Pool


def folder_paths(folder: str) -> Iterable[str]:
    """Yields the absolute paths of every file in `folder`."""
    filenames = os.listdir(folder)
    for filename in filenames:
        yield os.path.join(folder, filename)


def reset_folder(folder: str) -> None:
    """Creates an empty directory at `folder`, discarding any previous contents."""
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def read_csv_to_df(path: str) -> pd.DataFrame:
    """Reads the csv file at `path`, and does not create an index."""
    return pd.read_csv(path, index_col=False)


def read_csvs_to_df(csv_dir: str) -> pd.DataFrame:
    """Reads the csv files in `splits_dir`."""
    print(f"Reading dataset splits...")
    with Pool(4) as p:
        return pd.concat(p.map(read_csv_to_df , folder_paths(csv_dir)))


def df_splits(df: pd.DataFrame, row_limit: int, splits_dir: str) -> Iterable[tuple[pd.DataFrame, str]]:
    """Yields splits of `df`, each of length `row_limit`, to be saved in `splits_dir`."""
    df_len = len(df)
    num_splits = math.ceil(df_len / float(row_limit))

    print(f"Saving dataset into {num_splits} splits...")
    for i in range(num_splits):
        start, end = i * row_limit, min(df_len, (i + 1) * row_limit)
        split = df.iloc[start:end]
        filename = os.path.join(splits_dir, f'split_{i + 1}.csv')
        yield (split, filename)


def write_split_to_csv(split: tuple[pd.DataFrame, str]) -> None:
    """Saves a `split` (`DataFrame`, filename) into a csv file."""
    df, filename = split
    df.to_csv(filename, index=False, chunksize=10000)


def write_df_to_csvs(df: pd.DataFrame, row_limit: int, splits_dir: str) -> None:
    """Saves `df` into smaller csv files with at most `row_limit` rows per split."""
    reset_folder(splits_dir)
    with Pool(4) as p:
        p.map(write_split_to_csv, df_splits(df, row_limit, splits_dir))


class Movie(BaseModel):
    """
    The data extracted for each movie from the international movies dataset.
    https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies
    """
    original_title: str
    release_year: int 
    imdb_id: str
    poster_url: str | None
    runtime_seconds: int | None
    certificate_rating: str | None
    genres: list[str]
    spoken_languages: list[str]
    plot: str | None
    keywords: list[str]
    directors: list[str]
    writers: list[str]
    actors: list[str]
    companies: list[str]


def safe_get(d, keys: list[str], default=None):
    """Safely navigate nested `dict`s."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d


def safe_get_list(d: dict, keys_to_list: list[str], list_keys: list[str]) -> list[Any]:
    """Safely navigates nested `dict`s to a `list` and extracts values from its nested `dict` entries."""
    return [safe_get(entry, list_keys) for entry in safe_get(d, keys_to_list, [])]


def strs(xs: list[Any]) -> list[str]:
    """Filters out non-`str` elements from a list."""
    return list(filter(lambda x: isinstance(x, str), xs))


def extract_movie_data(path: str) -> list[Movie]:
    """
    Extracts the data from a json batch of the international movies dataset at `path`.
    https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    movies: list[Movie] = []
    for movie in data:
        title = safe_get(movie, ["titleText", "text"])
        original_title = safe_get(movie, ["originalTitleText", "text"], title)
        if not original_title:
            continue

        release_year = safe_get(movie, ["releaseYear", "year"])
        if release_year is None:
            continue

        imdb_id = safe_get(movie, ["id"])
        if not imdb_id:
            continue

        poster_url = safe_get(movie, ["primaryImage", "url"])

        runtime_seconds = safe_get(movie, ["runtime", "seconds"])
        
        certificate_rating = safe_get(movie, ["certificate", "rating"])

        genres = safe_get_list(movie, ["genres", "genres"], ["text"])

        spoken_languages = safe_get_list(movie, ["spokenLanguages", "spokenLanguages"], ["text"])

        plot = safe_get(movie, ["plot", "plotText", "plainText"], None)

        keywords = safe_get_list(movie, ["keywords", "edges"], ["node", "text"])

        directors, writers, actors = [], [], []
        principal_credits = safe_get(movie, ["principalCredits"], [])
        categories = { "Director": directors, "Writers": writers, "Stars": actors }
        for pc in principal_credits:
            category = safe_get(pc, ["category", "text"]) 
            if category in categories:
                names = safe_get_list(pc, ["credits"], ["name", "nameText", "text"])
                categories[category].extend(names)

        companies = safe_get_list(movie, ["companyCredits", "edges"], ["node", "company", "companyText", "text"])

        movies.append(Movie(
                original_title=original_title,
                release_year=release_year,
                imdb_id=imdb_id,
                runtime_seconds=runtime_seconds,
                certificate_rating=certificate_rating,
                genres=strs(genres),
                spoken_languages=strs(spoken_languages),
                plot=plot,
                keywords=strs(keywords),
                directors=strs(directors),
                writers=strs(writers),
                actors=strs(actors),
                companies=strs(companies),
                poster_url=poster_url,
                ))
    return movies 


def filter_duplicate_movies(movies: list[Movie]) -> list[dict[str, str | list[str] | None]]:
    """Filters out movies with the same `original_title` and `release_year`."""
    title_year = set()
    filtered_movies = []
    for movie in movies:
        entry = (movie.original_title, movie.release_year)
        if entry not in title_year:
            title_year.add(entry)
            filtered_movies.append(dict(movie))
    return filtered_movies

    
def main() -> None: 
    """
    Extracts the data from all the json files of the international movies dataset.
    https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies
    """
    print("Initializing international movies dataset...")
    with Pool(4) as p:
        movies_batches = p.map(extract_movie_data, folder_paths(Path.MOVIE_DATASET_FOLDER))

    movies: list[Movie] = []
    for movies_batch in movies_batches:
        movies.extend([movie for movie in movies_batch])

    filtered_movies = filter_duplicate_movies(movies)
    df = pd.DataFrame(filtered_movies)
    df.info()
    print("Note: the empty list values of list features, like keywords, do not appear as null")

    write_df_to_csvs(df, 7500, Path.MOVIES_FOLDER)


if __name__ == "__main__":
    main()

