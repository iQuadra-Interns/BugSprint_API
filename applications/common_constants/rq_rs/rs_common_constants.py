from pydantic import BaseModel
from typing import List, Dict, Any

class TableDataResponse(BaseModel):
    data: List[Dict[str, Any]]
