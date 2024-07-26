# applications/common_constants/rq_rs/rs_all.py

from typing import Dict, List, Union, Any
from pydantic import BaseModel

class Status(BaseModel):
    sts: bool = False
    err: Union[str, None] = "Operation failed"
    war: Union[str, None] = None
    msg: Union[str, None] = None

class AllTablesDataResponse(BaseModel):
    status: Status
    data: Dict[str, Union[List[Dict[str, Any]], str]]
