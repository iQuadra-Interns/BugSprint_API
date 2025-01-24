from pydantic import BaseModel, EmailStr, Field


class SignInRq(BaseModel):
    email: EmailStr = Field(default=...)
    password: str = Field(default=...)