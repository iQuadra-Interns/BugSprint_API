from pydantic import BaseModel
from typing import Optional
from common.classes.generic import Status

class EditProfileResponse(BaseModel):
    status: Status
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
