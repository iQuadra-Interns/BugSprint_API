# applications/bugs_list/rq_rs/rs_bugs_list.py

from typing import List, Union
from pydantic import BaseModel

class Status(BaseModel):
    sts: bool = False
    err: Union[str, None] = "Operation failed"
    war: Union[str, None] = None
    msg: Union[str, None] = None

class BugsList(BaseModel):
    bug_id: str
    bug: str
    scenario: str
    status: str
    assignee: str

class BugsListResponse(BaseModel):
    status: Status
    data: List[BugsList]
