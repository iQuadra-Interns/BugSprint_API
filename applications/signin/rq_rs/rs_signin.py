from typing import Union

from pydantic import BaseModel

from common.classes.generic import Status, UserId


class PersonalDetails(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email_id: str | None = None
    mobile_no: str | None = None


class SignInRs(BaseModel):
    status: Status | None = Status(sts=False, err="Operation failed", msg="")
    usr: UserId | None = None
    developer_details: PersonalDetails | None = None
    tester_details: PersonalDetails | None = None
    admin_details: PersonalDetails | None = None
