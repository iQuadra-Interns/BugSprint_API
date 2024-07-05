from typing import Union

from pydantic import BaseModel

from common.classes.generic import Status, UserId


class SignInRs(BaseModel):
    status: Status | None = Status(sts=False, err="Operation failed", msg="")
    usr: Union[UserId, None] = None

