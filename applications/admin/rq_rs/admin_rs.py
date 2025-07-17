from pydantic import BaseModel
from typing import Optional
from common.classes.generic import Status
from typing import List, Dict, Any




class AddUserResponse(BaseModel):
    status: Status
    category_id: Optional[int] = None
class GenericResponse(BaseModel):
    status: Status
class ProductRS(BaseModel):
    status: Status
    products: Optional[List[Dict[str, Any]]] = None
class ScenarioRS(BaseModel):
    status: Status
    scenarios: Optional[List[Dict[str, Any]]] = None
