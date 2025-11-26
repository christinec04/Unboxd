from enum import Enum
from pydantic import BaseModel
from typing import List

class UsernameRequest(BaseModel):
    username: str

class Status(str, Enum):
    starting = 'starting'
    scraping_reviews = 'scraping reviews'
    preprocessing_data = 'preprocessing data'
    finding_representative = 'finding representative'
    finding_recommendation = 'finding recommendations'
    finished = 'finished'

class StatusResponse(BaseModel):
    status: Status
    
class Movie(BaseModel):
    movieId: str
    name: str
    year: str
    genre: List[str]
    description: str
    posterURL: str
    letterboxdURL: str
    trailerID: str
    similarityScore: float