import os
import pandas as pd
from tqdm import tqdm
from typing import NamedTuple

def retrieve_rows(ids: set[str], data: pd.DataFrame) -> list[NamedTuple]:
    """Retrieves the rows associated with `ids` in `data`, which must contain `imdb_id`s"""
    rows = []
    for movie in data.itertuples():
        if movie.imdb_id in ids:
            rows.append(movie[1:])
            ids.remove(movie.imdb_id)
    return rows

def retrieve_data(ids: set[str], movies: pd.DataFrame) -> pd.DataFrame: 
    """Retrieves the movie data associated with ids in `data`, which must contain `imdb_id`s"""
    rows = retrieve_rows(ids, movies)
    return pd.DataFrame(rows, columns=movies.columns)

def retrieve_preprocessed_data(ids: set[str], print_status: bool = False) -> pd.DataFrame: 
    """Retrieves the preprocessed movie data associated with ids in `data`, which must contain `imdb_id`s"""
    if print_status: print("retrieving preprocessed data...")
    columns, rows = None, []
    files = os.listdir(Path.PREPROCESSED_MOVIES_FOLDER)
    files = tqdm(files) if print_status else files
    for file in files:
        if len(ids) == 0:
            break
        preprocessed_data = pd.read_csv(os.path.join(Path.PREPROCESSED_MOVIES_FOLDER, file))
        if columns is None: 
            columns = preprocessed_data.columns
        rows += retrieve_rows(ids, preprocessed_data)
    result = pd.DataFrame(rows, columns=columns)
    if print_status: print("done!")
    return result

if __name__ == "__main__":
    from paths import Path
    trending_movies = pd.read_csv(Path.MERGED_TRENDING_MOVIES)
    preprocessed_trending_movies = retrieve_preprocessed_data(
            set(trending_movies["imdb_id"].to_list()),
            print_status=True
    )
    preprocessed_trending_movies.to_csv(Path.PREPROCESSED_TRENDING_MOVIES)
else:
    from .paths import Path
