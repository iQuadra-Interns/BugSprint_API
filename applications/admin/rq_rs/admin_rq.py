from pydantic import BaseModel
from typing import Optional, Union

class UserInput(BaseModel):
    first_name: str
    last_name: str
    password:str
    phone_no: str
    email: str
    role: str