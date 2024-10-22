from pydantic import BaseModel
from typing import Optional, Union

class UserInput(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    email: str
    jobrole: str
    isd: str
    mobile_number: str