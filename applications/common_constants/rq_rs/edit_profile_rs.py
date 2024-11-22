from pydantic import BaseModel
from common.classes.generic import Status

class EditProfileResponse(BaseModel):
    status: Status = Status(status=False, error="Operation failed")
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    mobile_number: str | None = None

