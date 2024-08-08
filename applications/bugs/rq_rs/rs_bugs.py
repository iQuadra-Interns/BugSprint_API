from pydantic import BaseModel
from common.classes.generic import Status
from datetime import datetime

class AddBugResponse(BaseModel):
    status: Status
    bug_id: int

class UpdateBugResponse(BaseModel):
    status: Status

class BugDetails(BaseModel):
    reported_date: datetime
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

class FindBugResponse(BaseModel):
    status: Status
    bug: BugDetails
