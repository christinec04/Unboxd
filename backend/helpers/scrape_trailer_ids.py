import time
import requests
from tqdm import tqdm
import pandas as pd

def get_trailer_search_url(movie_name: str, release_year: str) -> str:
    """Returns the url for searching for `movie_name`'s trailer on YouTube"""
    search_query = "+".join(movie_name.split() + ["(", release_year, ")", "trailer"])
    return f"https://www.youtube.com/results?search_query={search_query}"

def get_trailer_id(html: str) -> str:
    # skip content from YouTube Movies & TV bc they only show trailers for non-rated R content w/out signing in 
    id_prefix = "\"videoRenderer\":{\"videoId\":\""
    id_start = html.find(id_prefix) + len(id_prefix)
    id_end = html.find("\"", id_start)
    video_id = html[id_start:id_end]
    return video_id

def scrape_trailer_ids(
        movie_names: list[str], release_years: list[str], print_status: bool = False
        ) -> list[str]:
    """Returns the scraped YouTube video ids of the trailers of the movies specified by `movie_names` and `release_years`"""
    if print_status: print("starting scraping...")
    trailer_ids = []
    movie_data = zip(tqdm(movie_names), release_years) if print_status else zip(movie_names, release_years)
    for movie_name, release_year in movie_data:
        if print_status: tqdm.write(f"scraping for {movie_name}...")
        video_id = ""
        try:
            response = requests.get(get_trailer_search_url(movie_name, release_year))
            response.raise_for_status()
            html = response.text
            video_id = get_trailer_id(html)
        except Exception as e:
            if print_status: tqdm.write(f"error, failed to scrape for {movie_name}: {e}")
        trailer_ids.append(video_id)
        time.sleep(2)
    return trailer_ids

def main():
    from paths import Path
    merged_trending_movies = pd.read_csv(Path.MERGED_TRENDING_MOVIES)
    strings = lambda xs: [str(x) if x else "" for x in xs]
    movie_names = strings(merged_trending_movies["original_title"].values)
    release_years = strings(merged_trending_movies["release_year"].values)
    trailer_ids = scrape_trailer_ids(movie_names, release_years, print_status=True) 
    result = pd.DataFrame()
    result["imdb_id"] = merged_trending_movies["imdb_id"].to_list()
    result["trailer_id"] = trailer_ids
    result.to_csv(Path.TRENDING_MOVIE_TRAILERS)

if __name__ == "__main__":
    main()
    
