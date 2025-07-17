from pydantic import BaseModel

class RephraseRequest(BaseModel):
    description: str
