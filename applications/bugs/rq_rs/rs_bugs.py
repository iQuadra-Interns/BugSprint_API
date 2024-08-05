from pydantic import BaseModel
from common.classes.generic import Status
from typing import Optional
from datetime import datetime

class AddBugResponse(BaseModel):
    status: Status
    bug_id: int

class UpdateBugResponse(BaseModel):
    status: Status

class Status(BaseModel):
    sts: bool
    err: str
    msg: str

class FindBugResponse(BaseModel):
    status: Status
    bug_id: int
    reported_date: datetime  # Now recognized as datetime is imported
    reporter: str
    assignee: str
    product_name: str
    environment: str
    testing_medium: str
    scenario: str
    description: str
    user_data: str
    priority: str
    status: str
    root_cause_location: str
    root_cause: str
    solution: str
    comments: str

   