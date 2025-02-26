from pydantic import BaseModel
from typing import Optional
from common.classes.generic import Status



class AddUserResponse(BaseModel):
    status: Status
    category_id: Optional[int] = None