import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scrape_reviews import scrape_reviews
from models import reviewRequest

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scrapeReviews")
def scrape_user_reviews(request: reviewRequest):
    scrape_reviews(request.username)
    return {"message": f"Scraping reviews for user {request.username} initiated."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)