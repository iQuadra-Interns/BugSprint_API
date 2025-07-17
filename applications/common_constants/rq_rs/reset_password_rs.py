from pydantic import BaseModel

from common.classes.generic import Status, UserId


class ResetPasswordRs(BaseModel):
    status: Status | None = Status(status=False, error="Operation failed")
    userid: UserId | None = None
