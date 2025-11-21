import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scrape_reviews import scrape_reviews
from models import Status, UsernameRequest, MovieList

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

# Dummy data
dummyData = [{"name": "Barbie", "year": "2023", "description": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.", "posterURL": "https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71"},]

# Send username to backend
@app.post("/username", response_model=Status)
def scrape_user_reviews(request: UsernameRequest):
    status, message = scrape_reviews(request.username)
    return Status(status=status, message=message)

# Get movie recommendations from backend
@app.get("/recommendations", response_model=MovieList)
def get_recommendations():
    # Do classification stuff here
    return MovieList(movies=dummyData)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)