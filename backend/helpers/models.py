from enum import Enum
from pydantic import BaseModel

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    STARTING = "starting"
    SCRAPING_REVIEWS = "scraping reviews"
    PREPROCESSING_DATA = "preprocessing data"
    FINDING_RECOMMENDATION = "finding recommendations"
    FINISHED = "finished"

class StatusResponse(BaseModel):
    status: Status
    
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
