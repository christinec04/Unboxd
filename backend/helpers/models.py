from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    STARTING = "Starting"
    VALIDATING_USERNAME = "Validating username"
    FAILED_INVALID_USERNAME = "Failed. Invalid username"
    WAITING_FOR_SCRAPER = "Waiting for scraper"
    SCRAPING_REVIEWS = "Scraping the user reviews"
    FAILED_NO_REVIEWS = "Failed. No reviews to scrape for the user"
    FAILED_SCRAPING = "Failed. Error while scraping"
    PREPROCESSING_DATA = "Preprocessing data"
    FAILED_NO_DATA = "Failed. No data available about the user-reviewed movies"
    FINDING_RECOMMENDATION = "Finding recommendations"
    FAILED_NO_RECOMMENDATIONS = "Failed. No trending movies not already reviewed are available for recommendation"
    FINISHED = "Finished"

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
