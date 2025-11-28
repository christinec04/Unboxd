from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    starting = "starting"
    scraping_reviews = "scraping reviews"
    preprocessing_data = "preprocessing data"
    finding_recommendation = "finding recommendations"
    finished = "finished"

class StatusResponse(BaseModel):
    status: Status
    
class Movie(BaseModel):
    movieId: str
    name: str
    year: str
    genre: list[str]
    description: str
    posterURL: str
    letterboxdURL: str
    trailerID: str
    similarityScore: float
