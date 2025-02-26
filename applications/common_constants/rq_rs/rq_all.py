from typing import Optional
from pydantic import BaseModel ,Field

class TableRequest(BaseModel):
    table_name: Optional[str] = Field(default=None, description="Name of the table to fetch data from. Leave empty to fetch from all tables.")

class GetUserDetailsRequest(BaseModel):
    pass
