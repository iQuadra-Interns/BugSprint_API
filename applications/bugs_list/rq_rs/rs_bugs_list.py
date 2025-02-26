from typing import  Union
from pydantic import BaseModel
from datetime import datetime


class Status(BaseModel):
    sts: bool = False
    err: str | None = "Operation failed"
    war: str | None = None
    msg: str | None = None



class Bug(BaseModel):
    bug_id: int | None = None
    title: str | None = None
    product: str | None = None
    environment: str | None = None
    scenario: str | None = None
    testing_medium: str | None = None
    description: str | None = None
    bug_code : str | None = None
    user_data: str | None = None
    priority: str | None = None
    reported_by: str | None = None
    reported_at: datetime | None = None
    assignee: str | None = None
    root_cause_location: str | None = None
    root_cause: str | None = None
    resolution: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BugsListResponse(BaseModel):
    status: Status
    bugs: list | None = None
