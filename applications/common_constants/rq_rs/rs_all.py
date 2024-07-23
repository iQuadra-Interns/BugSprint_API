from pydantic import BaseModel
from typing import Dict, Any
from common.classes.generic import Status

class AllTablesDataResponse(BaseModel):
    status: Status
    data: Dict[str, Any]
