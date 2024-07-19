from pydantic import BaseModel
from common.classes.generic import Status

class AddBugResponse(BaseModel):
    status: Status
    bug_id: int

class UpdateBugResponse(BaseModel):
    status: Status