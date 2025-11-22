import uvicorn
from typing import Dict, List
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from models import Status, StatusResponse, RecommendationResponse
from scrape_reviews import scrape_reviews 
from sent import sentiment_analysis

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

status: Dict[str, Status] = dict()
recommendations: Dict[str, List[str]] = dict()

def system(username): 
    status[username] = Status.scraping_reviews
    df = scrape_reviews(username)
    status[username] = Status.preprocessing_data
    new_df = sentiment_analysis(df)
    status[username] = Status.finished
    # TODO add more tasks

@app.post("/usernames/", status_code=HTTPStatus.ACCEPTED)
def init_system(username: str, background_tasks: BackgroundTasks):
    status[username] = Status.starting
    background_tasks.add_task(system, username)
    return

@app.get("/status/")
def check_status(username: str) -> StatusResponse:
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.get("/recommendations/")
def recommend_movies(username: str) -> RecommendationResponse:
    if username not in recommendations:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return RecommendationResponse(movies=recommendations[username])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
