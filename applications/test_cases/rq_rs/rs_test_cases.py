from pydantic import BaseModel
from typing import List, Optional
from common.classes.generic import Status



class TestCase(BaseModel):
    testcase_id: Optional[str] = None
    product_id: int
    test_scenario: str
    test_steps: str
    actual_result: str
    expected_result: str
    comment: str
    developer_comment: str


class TestCasesResponse(BaseModel):
    status: Status
    test_cases: Optional[List[TestCase]] = None


class UpdateTestCaseResponse(BaseModel):
    status: Status


class DeleteTestCaseResponse(BaseModel):
    status: Status



class TestCase(BaseModel):
    testcase_id: int
    product_id: int
    testcase_code: str
    test_scenario: str
    test_steps: str
    actual_result: str
    expected_result: str
    comment: str
    developer_comment: str

class GetTestCasesResponse(BaseModel):
    status: Status
    test_cases: List[TestCase]
