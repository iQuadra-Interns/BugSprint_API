"""
Authors: Generic/Common classes for various requests and responses
JIRA Tkt: NA
"""
import datetime
from typing import Union, List

from pydantic import BaseModel, EmailStr, Field


class Status(BaseModel):
    sts: bool = False
    err: Union[str, None] = "Operation failed"
    war: Union[str, None] = None
    msg: Union[str, None] = None


class UserId(BaseModel):
    user_id: Union[int, None] = None
    user_category: Union[str, None] = None
    user_cat_id: Union[int, None] = None
