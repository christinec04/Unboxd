from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    starting = "Starting."
    validating_username = "Validating Letterboxd username."
    failed_invalid_username = "Failed: invalid Letterboxd username."
    waiting_for_scraper = "Waiting for scraper."
    scraping_reviews = "Scraping the user's reviews."
    failed_no_reviews = "Failed: no ratings and reviews to scrape for the user."
    failed_scraping = "Failed: error while scraping."
    preprocessing_data = "Preprocessing data."
    failed_no_data = "Failed: no data available about the user's rated and reviews movies."
    finding_recommendation = "Finding recommendations."
    failed_no_recommendations = "Failed: no trending movies, unrated and unreviewd by the user, are available for recommendation."
    finished = "Finished."

class Movie(BaseModel):
    movieId: str
    name: str
    year: int
    genre: list[str]
    description: str
    posterURL: str
    letterboxdURL: str
    trailerID: str
    similarityScore: float
