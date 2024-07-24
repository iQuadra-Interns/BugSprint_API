from pydantic import BaseModel
from typing import Dict, Any
from common.classes.generic import Status

class AllTablesDataResponse(BaseModel):
    data: Dict[str, Any]
