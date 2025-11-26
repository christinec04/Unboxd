from os import name
import uvicorn
import numpy as np
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from models import UsernameRequest, Status, StatusResponse, Movie
from scrape_reviews import scrape_reviews 
from sentiment import sentiment_analysis
from scrape_reviews import scrape_reviews
from dummy_data import dummyData
from recommender import recommend_movies

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

status: dict[str, Status] = dict()
recommendations: dict[str, list[Movie]] = dict()

def get_movie_metadata(recs):
    """
    Converts (movie_id, score) tuples from the recommender 
    into full Movie objects using dummy data for metadata lookup
    """
    # Create a mapping of movie_id to the full Movie object from your dummy data
    id_to_movie = {m.movieId: m for m in dummyData}
    
    final_recs = []
    for movie_id, score in recs:
        if movie_id in id_to_movie:
            # Create a copy and update the similarity score field
            movie = id_to_movie[movie_id].model_copy(update={'similarity_score': score})
            final_recs.append(movie)
    return final_recs

def create_mock_data():
    """
    Creates sample data structures needed by recommender.py for testing
    """
    # Ensure all feature vectors are NumPy arrays for compatibility with recommender.py
    user_movies = [
        [np.array([0.9, 0.1]), np.array([0.7])],  # Movie A
        [np.array([0.1, 0.9]), np.array([0.2])],  # Movie B
    ]
    weights = [0.8, 0.4]
    watched_ids = {"1000001", "1000002"} # Mock watched movies (IDs must match dummyData)

    # All Movies map (ID -> Feature Vector)
    all_movies = {
        "1000001": [np.array([0.9, 0.1]), np.array([0.7])],
        "1000002": [np.array([0.1, 0.9]), np.array([0.2])],
        "1000003": [np.array([0.85, 0.15]), np.array([0.8])], 
        "1000004": [np.array([0.2, 0.8]), np.array([0.3])],   
        "1000005": [np.array([0.5, 0.5]), np.array([0.5])],   
        "1000006": [np.array([0.9, 0.1]), np.array([0.9])],  
    }
    return user_movies, weights, watched_ids, all_movies

def system(username): 
    # TODO add more steps
    status[username] = Status.scraping_reviews
    df = scrape_reviews(username)
    status[username] = Status.preprocessing_data
    new_df = sentiment_analysis(df)

    status[username] = Status.finding_representative
    user_movies_mock, weights_mock, watched_ids_mock, all_movies_mock = create_mock_data()
    status[username] = Status.finding_recommendation
    recs = recommend_movies(
        user_movies=user_movies_mock,
        weights=weights_mock,
        watched_ids=watched_ids_mock,
        all_movies=all_movies_mock,
        k=5
    )
    recommendations[username] = get_movie_metadata(recs)

    status[username] = Status.finished

@app.post("/usernames/", status_code=HTTPStatus.ACCEPTED)
def init_system(request: UsernameRequest, background_tasks: BackgroundTasks):
    # should check if username exists in database, throw error if so
    # should check if scraped data is empty, throw error if so
    status[request.username] = Status.starting
    background_tasks.add_task(system, request.username)
    # uncomment here to test displaying the movies on the frontend
    # recommendations[request.username] = dummyData
    return

@app.get("/status/", response_model=StatusResponse)
def check_status(username: str):
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.get("/movies/", response_model=list[Movie])
def get_recommend_movies(username):
    if username not in recommendations:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return recommendations[username]

def test_recommender_module():
    """
    Runs a test of the recommender logic before server startup
    """
    print("--- Starting Recommender Test ---")
    
    user_movies, weights, watched_ids, all_movies = create_mock_data()
    k = 3
    
    try:
        recs = recommend_movies(
            user_movies=user_movies, 
            weights=weights, 
            watched_ids=watched_ids, 
            all_movies=all_movies, 
            k=k
        )
        final_recs = get_movie_metadata(recs)

        print(f"Successfully generated {len(final_recs)} recommendations:")
        for movie in final_recs:
            print(f"- {movie.name} ({movie.movieId}), Score: {movie.similarity_score:.4f}")

    except Exception as e:
        print(f"Recommender Test Failed with an error: {e}")
    
    print("--- Recommender Test Finished ---")
    
if __name__ == "__main__":
    test_recommender_module()

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000)
