from pydantic import BaseModel
from typing import List
from common.classes.generic import Status



class TestCase(BaseModel):
    testcase_id: int
    product_id: int
    test_scenario: str
    test_steps: str
    actual_result: str
    expected_result: str
    comment: str
    developer_comment: str



class TestCasesResponse(BaseModel):
    status: Status
    test_cases: List[TestCase] = None



class UpdateTestCaseResponse(BaseModel):
    status: Status



class DeleteTestCaseResponse(BaseModel):
    status: Status



class GetTestCasesResponse(BaseModel):
    status: Status
    test_cases: List[TestCase]
