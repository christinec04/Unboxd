from enum import Enum
from pydantic import BaseModel

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
    name: str
    year: str
    description: str
    posterURL: str
    
class RecommendationResponse(BaseModel):
    movies: list[Movie]
