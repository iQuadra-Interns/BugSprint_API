from pydantic import BaseModel


class AddBugRq(BaseModel):
    product_id: int
    title:str
    environment_id: int
    scenario_id: int
    testing_medium: int
    description: str
    user_data: str | None = None
    priority_id: int
    reported_by: int
    assignee_id: int | None = None
    root_cause_location: int
    root_cause: str | None = None
    resolution: str | None = None
    status: int | None = None


class UpdateBugRq(BaseModel):
    product_id: int
    title:str
    environment_id: int
    scenario_id: int
    testing_medium: int
    description: str
    user_data: str | None = None
    priority_id: int
    reported_by: int
    assignee_id: int | None = None
    root_cause_location: int
    root_cause: str
    resolution: str
    status: int

class DeleteBugRq(BaseModel):
    bug_id: int
