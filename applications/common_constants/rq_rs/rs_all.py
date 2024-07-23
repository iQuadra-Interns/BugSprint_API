from pydantic import BaseModel
from typing import Dict, Any

class AllTablesDataResponse(BaseModel):
    data: Dict[str, Any]
