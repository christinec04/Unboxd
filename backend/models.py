from enum import Enum
from typing import List
from pydantic import BaseModel

class Status(str, Enum):
    starting = 'starting'
    scraping_reviews = 'scraping reviews'
    preprocessing_data = 'preprocessing data'
    finding_representative = 'finding representative'
    finding_recommendation = 'finding recommendations'
    finished = 'finished'

class ReviewRequest(BaseModel):
    username: str

class StatusResponse(BaseModel):
    status: Status
    
class RecommendationResponse(BaseModel):
    movies: List[str]
