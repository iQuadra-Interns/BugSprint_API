from pydantic import BaseModel
from typing import List
from common.classes.generic import Status

class BugsList(BaseModel):
    bug_id: str
    bug: str
    scenario: str
    status: str
    assignee: str

class BugsListResponse(BaseModel):
    status: Status
    data: List[BugsList]
