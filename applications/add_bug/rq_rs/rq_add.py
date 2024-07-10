from pydantic import BaseModel

class AddBugRequest(BaseModel):
    bug_id: str
    bug: str
    scenario: str
    status: str
    assignee: str
    environment: str
    testing_medium: str
    root_cause_location: str
    priority: str
    description: str
    user_data: str
