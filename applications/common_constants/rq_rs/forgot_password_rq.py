from pydantic import BaseModel, Field, EmailStr
from common.classes.generic import UserId



class ForgotPasswordRq(BaseModel):
    userid: UserId | None = None
    email: EmailStr | None = None
    new_password: str | None = Field(default=...)


class ForgotPasswordGenerateOTPRq(BaseModel):
    userid: UserId | None = None
    email: EmailStr | None = None


class ForgotPasswordVerifyEmailRq(BaseModel):
    userid: UserId | None = None
    email: EmailStr | None = None
    email_otp: str | None = Field(default=...)