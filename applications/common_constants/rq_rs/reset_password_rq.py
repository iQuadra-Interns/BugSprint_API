from pydantic import BaseModel, Field, EmailStr
from common.classes.generic import UserId

class ResetPasswordRq(BaseModel):
    userid: UserId | None = None
    email: EmailStr | None = None
    old_password: str | None = Field(default=...)
    new_password: str | None = Field(default=...)
