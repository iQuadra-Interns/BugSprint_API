from typing import Union

from pydantic import BaseModel

from common.classes.generic import Status, UserId

class personal_details(BaseModel):
    id : int
    first_name : str
    last_name : str
    role_of_the_user : str


class SignInRs(BaseModel):
    status: Status | None = Status(sts=False, err="Operation failed", msg="")
    usr: Union[UserId, None] = None
    person_details : personal_details

