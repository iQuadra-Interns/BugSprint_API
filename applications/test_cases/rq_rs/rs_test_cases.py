from pydantic import BaseModel
from typing import List, Optional

class Status(BaseModel):
    sts: bool = False
    err: Optional[str] = "Operation failed"
    war: Optional[str] = None
    msg: Optional[str] = None


class TestCase(BaseModel):
    testcase_id: Optional[str] = None
    product_id: int
    test_scenario: str
    test_steps: str
    actual_result: str
    comment: str
    developer_comment: str



class TestCasesResponse(BaseModel):
    status: Status
    test_cases: Optional[List[TestCase]] = None
