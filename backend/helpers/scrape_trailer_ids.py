from selenium.webdriver.common.by import By
import pandas as pd
from initialize_datasets import merged_trending_movies_path
from scrape_reviews import init_headless_chrome_webdriver
import os
import time
import requests
import json
from tqdm import tqdm

trailer_ids_path = os.path.join(os.getcwd(), "..", "data", "trending_movie_trailer_ids.csv")

def get_trailer_search_url(movie_name: str, release_year: str):
    """Returns the url for searching for `movie_name`'s trailer on YouTube"""
    search_query = "+".join(movie_name.split() + [release_year, "trailer"])
    return f"https://www.youtube.com/results?search_query={search_query}"

def scrape_trailer_ids_with_driver(movie_names: list[str], release_years) -> list[str]:
    """Returns the scraped YouTube video ids for the trailers of the movies specified by `movie_names` and `release_years` with a Chrome webdriver"""
    print("starting scraping...")
    driver = init_headless_chrome_webdriver()
    trailer_ids = []
    for movie_name, release_year in zip(tqdm(movie_names), release_years):
        video_id = ""
        try:
            driver.get(get_trailer_search_url(movie_name, release_year))
            time.sleep(1)
            video_titles = driver.find_elements(By.ID, "video-title")
            channel_names = [e.text for e in driver.find_elements(By.ID, "channel-info")]
            for video_title, channel_name in zip(video_titles, channel_names):
                # skip content from YouTube Movies & TV bc they only show trailers for non-rated R content w/out signing in 
                if channel_name == "Youtube Movies & TV":
                    continue
                video_url = video_title.get_attribute("href")
                if video_url is None:
                    continue
                url_prefix = "https://www.youtube.com/watch?v="
                video_id_end = video_url.find("&")
                video_id = video_url[len(url_prefix):video_id_end]
                break
        except Exception as e:
            tqdm.write(f"error, failed to scrape for {movie_name}: {e}")
        trailer_ids.append(video_id)
    driver.quit()
    return trailer_ids

def scrape_trailer_ids(movie_names: list[str], release_years: list[str]) -> list[str]:
    """Returns the scraped YouTube video ids for the trailers of the movies specified by `movie_names` and `release_years`"""
    print("starting scraping...")
    decoder = json.JSONDecoder()
    trailer_ids = []
    for movie_name, release_year in zip(tqdm(movie_names), release_years):
        video_id = ""
        try:
            response = requests.get(get_trailer_search_url(movie_name, release_year))
            time.sleep(1)
            html = response.text
            info_prefix = "var ytInitialData = "
            info_start = html.find(info_prefix) + len(info_prefix)
            info_end = html.find(";", info_start)
            info = decoder.decode(html[info_start:info_end])
            contents = info["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"] \
                    ["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
            for content in reversed(contents):
                # skip content from YouTube Movies & TV bc they only show trailers for non-rated R content w/out signing in 
                if "videoRenderer" not in content:
                    continue
                video_id = content["videoRenderer"]["videoId"]
        except Exception as e:
            tqdm.write(f"error, failed to scrape for {movie_name}: {e}")
        trailer_ids.append(video_id)
    return trailer_ids

if __name__ == "__main__":
    merged_trending_movies = pd.read_csv(merged_trending_movies_path)
    strings = lambda xs: [str(x) if x else "" for x in xs]
    release_years = strings(merged_trending_movies["release_year"].values)
    movie_names = strings(merged_trending_movies["original_title"].values)
    # slower but less error prone than the other scraping method
    trailer_ids = scrape_trailer_ids_with_driver(movie_names, release_years) 
    # trailer_ids = scrape_trailer_ids(movie_names, release_years) 
    result = pd.DataFrame()
    result["imdb_id"] = merged_trending_movies["imdb_id"]
    result["trailer id"] = trailer_ids
    result.to_csv(trailer_ids_path)

