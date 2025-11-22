import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from models import UsernameRequest, Status, StatusResponse, Movie, MoviesResponse
from scrape_reviews import scrape_reviews 
from sent import sentiment_analysis
from scrape_reviews import scrape_reviews

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

# dummyData = [{"name": "Barbie", "year": "2023", "description": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.", "posterURL": "https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71"},]
dummyData = [Movie(name="Barbie", year="2023", description="Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.", posterURL="https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71"),]

def system(username): 
    # TODO add more steps
    status[username] = Status.scraping_reviews
    df = scrape_reviews(username)
    status[username] = Status.preprocessing_data
    new_df = sentiment_analysis(df)
    # uncomment here to test whether the frontend waits for the system to finish before fetching the movies
    # recommendations[username] = dummyData
    status[username] = Status.finished

@app.post("/usernames/", status_code=HTTPStatus.ACCEPTED)
def init_system(request: UsernameRequest, background_tasks: BackgroundTasks):
    status[request.username] = Status.starting
    background_tasks.add_task(system, request.username)
    # uncomment here to test displaying the movies on the frontend
    # recommendations[username] = dummyData
    return

@app.get("/status/", response_model=StatusResponse)
def check_status(username: str):
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.get("/movies/", response_model=MoviesResponse)
def recommend_movies(username: str):
    if username not in recommendations:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return MoviesResponse(movies=recommendations[username])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000)
