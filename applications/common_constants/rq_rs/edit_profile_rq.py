from pydantic import BaseModel

class EditProfileRequest(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    mobile_number: str | None = None
