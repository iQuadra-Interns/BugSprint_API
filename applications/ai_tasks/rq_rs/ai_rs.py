from pydantic import BaseModel

class RephraseResponse(BaseModel):
    original: str
    rephrased: str
