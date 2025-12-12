import uvicorn
import pandas as pd
import numpy as np
import requests
from ast import literal_eval
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from threading import Lock
from helpers.paths import Path
from helpers.models import UsernameRequest, Status, Movie
from helpers.scrape_reviews import scrape_reviews 
from helpers.sentiment import sentiment_analysis
from helpers.scrape_reviews import scrape_reviews
from helpers.recommender import recommend_movies
from helpers.movieswreviews import merge_sentiment_reviews_dataset
from helpers.retrieve_preprocessed import retrieve_data, retrieve_preprocessed_data

scraper_lock = Lock()
status: dict[str, Status] = dict()
recommendations: dict[str, list[Movie]] = dict()

movies = pd.read_csv(Path.movies)
trending_movies = pd.read_csv(Path.merged_trending_movies)

complete_preprocessed_trending_movies = pd.read_csv(Path.preprocessed_trending_movies)
indexed_preprocessed_trending_movies = complete_preprocessed_trending_movies.drop(columns=["imdb_id"]).to_numpy()
preprocessed_trending_movies = np.delete(arr=indexed_preprocessed_trending_movies, obj=0, axis=1)
preprocessed_trending_movies_ids = complete_preprocessed_trending_movies["imdb_id"].to_list()

trailers = pd.read_csv(Path.trending_movie_trailers)
trailer_ids = {trailer.imdb_id:trailer.trailer_id for trailer in trailers.itertuples()}

app = FastAPI()
origins = [
        "http://localhost:3000",
        "http://192.168.11.1:3000"
]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

def get_movies(recs: dict[str, float]) -> list[Movie]:
    """
    Converts the (movie id : similarity score) mappings from the recommender 
    into full Movie objects using the trending movies dataset
    """
    result = []
    imdb_ids = set(recs.keys())
    for movie in retrieve_data(imdb_ids, trending_movies).itertuples():
        result.append(Movie(
            movieId=movie.imdb_id,
            name=movie.original_title,
            year=int(movie.release_year),
            genre=literal_eval(movie.genres),
            description=movie.plot,
            posterURL=movie.poster_url,
            letterboxdURL=f'https://www.letterboxd.com/imdb/{movie.imdb_id}',
            trailerID=trailer_ids[movie.imdb_id] if movie.imdb_id in trailer_ids else "",
            similarityScore=recs[movie.imdb_id]
        ))
    return result 

def recommendation_system(username: str): 
    """
    Completes the trending movie recommendation system for the Letterboxd user `username`, 
    updating the `status` of the system for `username` along the way, and storing the
    the result in `recommendations` for `username`
    """
    status[username] = Status.validating_username
    profile_response = requests.get(f"https://www.letterboxd.com/{username}/")
    if profile_response.status_code != 200:
        status[username] = Status.failed_invalid_username
        return

    status[username] = Status.waiting_for_scraper
    with scraper_lock:
        status[username] = Status.scraping_reviews
        try:
            reviews = scrape_reviews(username)
        except:
            status[username] = Status.failed_scraping
            return
    if len(reviews) == 0:
        status[username] = Status.failed_no_reviews
        return

    status[username] = Status.preprocessing_data
    sentiment_reviews = sentiment_analysis(reviews)
    merged_reviews = merge_sentiment_reviews_dataset(movies, sentiment_reviews)
    if len(merged_reviews) == 0:
        status[username] = Status.failed_no_data
        return
    weights = [a + b for a, b in merged_reviews[["user_rating", "compound"]].values]
    user_movie_ids = set(merged_reviews["imdb_id"].to_list())
    complete_preprocessed_user_movies = retrieve_preprocessed_data(user_movie_ids.copy())
    preprocessed_user_movies = complete_preprocessed_user_movies.drop(columns=["imdb_id"]).to_numpy()

    status[username] = Status.finding_recommendation
    recs = recommend_movies(
        user_movies=preprocessed_user_movies,
        weights=weights,
        user_movie_ids=user_movie_ids,
        all_movies=preprocessed_trending_movies,
        all_movie_ids=preprocessed_trending_movies_ids,
        k=10
    )
    if len(recs) == 0:
        status[username] = Status.failed_no_available_recommendations 
        return
    recommendations[username] = get_movies(recs)

    status[username] = Status.finished

@app.post("/usernames/", status_code=HTTPStatus.ACCEPTED)
def init_system(request: UsernameRequest, background_tasks: BackgroundTasks):
    status[request.username] = Status.starting
    background_tasks.add_task(recommendation_system, request.username)
    return

@app.get("/status/", response_model=Status)
def check_status(username: str):
    if username not in status:
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"the recommendation system has not run for {username}, \
                        post /usernames/ to start it."
        )
    username_status = status[username]
    if username_status in (Status.failed_invalid_username, Status.failed_no_reviews):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=username_status)
    elif username_status in (Status.failed_scraping, Status.failed_no_data, Status.failed_no_recommendations):
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=username_status)
    else:
        return username_status 

@app.get("/movies/", response_model=list[Movie])
def get_recommend_movies(username):
    if username not in recommendations:
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"The recommendation system is incomplete for {username}, \
                        get /status/ for more info."
        )
    else:
        return recommendations[username]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

