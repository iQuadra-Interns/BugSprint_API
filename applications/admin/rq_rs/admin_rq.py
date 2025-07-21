from pydantic import BaseModel

class UserInput(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    email: str
    jobrole: str
    isd: str
    mobile_number: str
class ProductRQ(BaseModel):
    product_name: str
    product_short_code: str
class ScenarioRQ(BaseModel):
    scenario_name: str
    product_id: int