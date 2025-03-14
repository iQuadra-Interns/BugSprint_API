from datetime import datetime
from pydantic import BaseModel
from common.classes.generic import Status, UserId


class PersonalDetails(BaseModel):
    id: int | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    jobrole: str | None = None
    isd: str | None = None
    mobile_number: str | None = None
    created_at: datetime | None = None
    last_updated: datetime | None = None


class SignInRs(BaseModel):
    status: Status | None = Status(status=False, error="Operation failed", message="")
    usr: UserId | None = None
    developer_details: PersonalDetails | None = None
    tester_details: PersonalDetails | None = None
    admin_details: PersonalDetails | None = None
