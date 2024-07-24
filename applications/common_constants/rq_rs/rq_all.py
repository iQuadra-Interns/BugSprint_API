
from pydantic import BaseModel

class DatabaseNameRequest(BaseModel):
    database: str
