from pydantic import BaseModel

class AddBugResponse(BaseModel):
    message: str
