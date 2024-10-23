from typing import List, Union
from pydantic import BaseModel
from datetime import datetime


class Status(BaseModel):
    sts: bool = False
    err: Union[str, None] = "Operation failed"
    war: Union[str, None] = None
    msg: Union[str, None] = None



class Bug(BaseModel):
    id: Union[int, None] = None
    product: Union[str, None] = None
    environment: Union[str, None] = None
    scenario: Union[str, None] = None
    testing_medium: Union[str, None] = None
    description: Union[str, None] = None
    user_data: Union[str, None] = None
    priority: Union[str, None] = None
    reported_by: Union[str, None] = None
    reported_at: Union[datetime, None] = None
    assignee: Union[str, None] = None
    root_cause_location: Union[str, None] = None
    root_cause: Union[str, None] = None
    resolution: Union[str, None] = None
    status: Union[str, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class BugsListResponse(BaseModel):
    status: Status
    bugs: list | None = None
