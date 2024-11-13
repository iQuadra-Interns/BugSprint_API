from pydantic import BaseModel
from common.classes.generic import Status
from datetime import datetime


class AddBugResponse(BaseModel):
    status: Status
    bug_id: int


class UpdateBugResponse(BaseModel):
    status: Status


class BugDetails(BaseModel):
    bug_id: int
    title:str
    product_id: int
    environment_id: int
    scenario_id: int
    testing_medium: int
    description: str
    user_data: str | None = None
    priority_id: int
    reported_by: int
    reported_at: datetime | None = None
    assignee_id: int | None = None
    root_cause_location: int
    root_cause: str | None = None
    resolution: str | None = None
    status: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ViewBugDetails(BaseModel):
    bug_id: int
    title:str
    product: str
    environment: str
    scenario: str
    testing_medium: str
    description: str
    user_data: str | None = None
    priority: str
    reported_by: str
    reported_at: datetime | None = None
    assignee: str | None = None
    root_cause_location: str
    root_cause: str | None = None
    resolution: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class FindBugResponse(BaseModel):
    status: Status
    bug_details: ViewBugDetails | None = None
