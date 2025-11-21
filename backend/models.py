from pydantic import BaseModel

class Status(BaseModel):
    status: bool # True if successful, False otherwise
    message: str # Error or success message
    
class UsernameRequest(BaseModel):
    username: str
    
class Movie(BaseModel):
    name: str
    year: str
    description: str
    posterURL: str
    
class MovieList(BaseModel):
    movies: list[Movie]