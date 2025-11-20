import uvicorn
import sqlite3
from typing import Dict, List
from threading import Lock
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from scrape_reviews import scrape_reviews, save_data_to_csv
from models import ReviewRequest, Status, StatusResponse, RecommendationResponse

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

@app.post("/scrapeReviews")
def scrape_user_reviews(request: ReviewRequest):
    data = scrape_reviews(request.username)
    save_data_to_csv(request.username, data)
    return
    return {"message": f"Scraping reviews for user {request.username} initiated."}

# TODO possibly replace with sqlite db
lock = Lock()
status: Dict[str, Status] = dict()
recommendations: Dict[str, List[str]] = dict()

def system(username): 
    status[username] = Status.scraping_reviews
    data = scrape_reviews(username)
    # TODO add every task

@app.post("/usernames/{username}", status_code=HTTPStatus.ACCEPTED)
def init_system(username: str, background_tasks: BackgroundTasks):
    status[username] = Status.starting
    background_tasks.add_task(system, username)
    return

@app.post("/status/{username}")
def check_status(username: str) -> StatusResponse:
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.post("/recommendations/{username}")
async def recommend_movies(username: str) -> RecommendationResponse:
    if username not in recommendations:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return RecommendationResponse(movies=recommendations[username])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
