import uvicorn
import pandas as pd
import numpy as np
from ast import literal_eval
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from helpers.paths import Path
from helpers.models import UsernameRequest, Status, StatusResponse, Movie
from helpers.scrape_reviews import scrape_reviews 
from helpers.sentiment import sentiment_analysis
from helpers.recommender import recommend_movies
from helpers.movieswreviews import merge_sentiment_reviews_dataset
from helpers.retrieve_preprocessed import retrieve_data, retrieve_preprocessed_data

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
uvicorn.run(app, host="0.0.0.0", port=8000)

def get_movies(recs: dict[str, float]) -> list[Movie]:
    """
    Converts the (movie id: score) tuples from the recommender 
    into full Movie objects 
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
    status[username] = Status.SCRAPING_REVIEWS
    reviews = scrape_reviews(username)
  
    status[username] = Status.PREPROCESSING_DATA
    sentiment_reviews = sentiment_analysis(reviews)
    merged_reviews = merge_sentiment_reviews_dataset(movies, sentiment_reviews)
    weights = [a + b for a, b in merged_reviews[["user_rating", "compound"]].values]
    user_movie_ids = set(merged_reviews["imdb_id"].to_list())
    complete_preprocessed_user_movies = retrieve_preprocessed_data(user_movie_ids.copy())
    preprocessed_user_movies = complete_preprocessed_user_movies.drop(columns=["imdb_id"]).to_numpy()

    status[username] = Status.FINDING_RECOMMENDATION
    recs = recommend_movies(
        user_movies=preprocessed_user_movies,
        weights=weights,
        user_movie_ids=user_movie_ids,
        all_movies=preprocessed_trending_movies,
        all_movie_ids=preprocessed_trending_movies_ids,
        k=10
    )
    recommendations[username] = get_movies(recs)

    status[username] = Status.FINISHED

@app.post("/usernames/", status_code=HTTPStatus.ACCEPTED)
def init_system(request: UsernameRequest, background_tasks: BackgroundTasks):
    status[request.username] = Status.STARTING
    background_tasks.add_task(recommendation_system, request.username)
    return

@app.get("/status/", response_model=StatusResponse)
def check_status(username: str):
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.get("/movies/", response_model=list[Movie])
def get_recommend_movies(username: str):
    if username not in recommendations:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return recommendations[username]