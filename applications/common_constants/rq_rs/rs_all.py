from typing import Dict, List, Union, Any ,Optional
from pydantic import BaseModel
from common.classes.generic import Status



class GetTableDataResponse(BaseModel):
    status: Status
    data: Optional[Union[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]] = None


class UserDetailsResponse(BaseModel):
    user_id: int
    user_name: str

class GetUserDetailsResponse(BaseModel):
    status: Status
    users: list[UserDetailsResponse] = []
