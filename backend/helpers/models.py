from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    starting = "starting"
    validating_username = "validating Letterboxd username"
    failed_invalid_username = "failed, invalid Letterboxd username"
    waiting_for_scraper = "waiting for scraper"
    scraping_reviews = "scraping reviews"
    failed_no_reviews = "failed, no reviews to scrape"
    failed_scraping = "failed, error while scraping"
    preprocessing_data = "preprocessing data"
    finding_recommendation = "finding recommendations"
    finished = "finished"

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
