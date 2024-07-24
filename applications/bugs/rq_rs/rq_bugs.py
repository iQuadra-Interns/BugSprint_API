from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AddBugRq(BaseModel):
    reported_date: datetime
    reporter: str
    assignee: Optional[str] = None
    product_name: Optional[str] = None
    environment: Optional[str] = None
    testing_medium: Optional[str] = None
    scenario: Optional[str] = None
    description: Optional[str] = None
    user_data: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    root_cause_location: Optional[str] = None
    root_cause: Optional[str] = None
    solution: Optional[str] = None
    comments: Optional[str] = None

class UpdateBugRq(BaseModel):
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