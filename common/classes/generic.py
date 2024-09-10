"""
Authors: Generic/Common classes for various requests and responses
JIRA Tkt: NA
"""
import datetime
from typing import Union, List, Optional

from pydantic import BaseModel, EmailStr, Field


class Status(BaseModel):
    status: bool = False
    error: str | None = "Operation failed"
    warning: str | None = None
    message: str | None = None


class UserId(BaseModel):
    user_id: Union[int, None] = None
    user_category: Union[str, None] = None
    user_cat_id: Union[int, None] = None

