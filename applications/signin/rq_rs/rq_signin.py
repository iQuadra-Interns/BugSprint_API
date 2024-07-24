from pydantic import BaseModel, EmailStr, Field
from typing import Union


class SignInRq(BaseModel):
    email: EmailStr = Field(default=...)
    password: str = Field(default=...)