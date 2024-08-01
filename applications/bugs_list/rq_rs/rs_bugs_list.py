from typing import List, Union
from pydantic import BaseModel
from datetime import datetime

class Status(BaseModel):
    sts: bool = False
    err: Union[str, None] = "Operation failed"
    war: Union[str, None] = None
    msg: Union[str, None] = None

class BugsList(BaseModel):
    ID: Union[float,None]
    Redirected_from: Union[float, None]
    Redirected_to: Union[float, None]
    Date: Union[datetime, None]
    Bug_identified_Time: Union[str, None]
    Bug_Reported_Time: Union[datetime, None]
    Reported_By: Union[str, None]
    Product_Name: Union[str, None]
    Environment: Union[str, None]
    Testing_Medium: Union[str, None]
    Scenario: Union[str, None]
    Description: Union[str, None]
    User_Data: Union[str, None]
    Priority: Union[str, None]
    Status: Union[str, None]
    Assignee: Union[str, None]
    Root_Cause_Location: Union[str, None]
    Root_Cause: Union[str, None]
    Solution: Union[str, None]
    Developer_Comment: Union[str, None]
    Tester_Comments: Union[str, None]

class BugsListResponse(BaseModel):
    status: Status
    data: List[BugsList]
