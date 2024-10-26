from pydantic import BaseModel, EmailStr
from common.classes.generic import UserId, Status


class ForgotPasswordRs(BaseModel):
    status: Status | None = Status(status=False, error="Operation failed")
    userid: UserId | None = None
    email: EmailStr | None = None


class UserLogin(BaseModel):
    userid: UserId | None = None
    email: EmailStr | None = None


class UserLoginRs(BaseModel):
    sts: Status | None = Status(status=False, error="Operation failed")
    det: UserLogin | None = None