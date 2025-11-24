from os import name
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from models import UsernameRequest, Status, StatusResponse, Movie
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

dummyData = [
    Movie(name="Barbie", year="2023", genre=["Comedy", "Fantasy"], description="Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.", posterURL="https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71", letterboxdURL="https://letterboxd.com/film/barbie/", trailerID="Ml0bijl4IoA"),
    Movie(name="Oppenheimer", year="2023", genre=["Drama", "History"], description="The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.", posterURL="https://a.ltrbxd.com/resized/film-poster/7/8/4/3/2/8/784328-oppenheimer-0-230-0-345-crop.jpg?v=e3c6e7a32c", letterboxdURL="https://letterboxd.com/film/oppenheimer-2023/", trailerID="pXTvDfOjbh0"),]

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
    # recommendations[request.username] = dummyData
    return

@app.get("/status/", response_model=StatusResponse)
def check_status(username: str):
    if username not in status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return StatusResponse(status=status[username])

@app.get("/movies/", response_model=list[Movie])
def recommend_movies(username):
    # if username not in recommendations:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    # return MoviesResponse(movies=recommendations[username])

    # testing data returns 
    return dummyData
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000)
