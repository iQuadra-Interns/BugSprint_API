from pydantic import BaseModel
from typing import List

class BugsList(BaseModel):
    bug_id: str
    bug: str
    scenario: str
    status: str
    assignee: str

class BugsListResponse(BaseModel):
    data: List[BugsList]
