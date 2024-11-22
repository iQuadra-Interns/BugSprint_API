from pydantic import BaseModel

class EditProfileRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    mobile_number: str
