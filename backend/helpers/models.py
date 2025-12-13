from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    STARTING = "Starting."
    VALIDATING_USERNAME = "Validating username."
    FAILED_INVALID_USERNAME = "Failed invalid username."
    WAITING_FOR_SCRAPER = "Waiting for scraper."
    SCRAPING_REVIEWS = "Scraping the user reviews."
    FAILED_NO_REVIEWS = "Failed no ratings and reviews to scrape for the user."
    FAILED_SCRAPING = "Failed error while scraping."
    PREPROCESSING_DATA = "Preprocessing data."
    FAILED_NO_DATA = "Failed no data available about the user rated and reviews movies."
    FINDING_RECOMMENDATION = "Finding recommendations."
    FAILED_NO_RECOMMENDATIONS = "Failed no trending movies not already reviewed are available for recommendation."
    FINISHED = "Finished."

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
