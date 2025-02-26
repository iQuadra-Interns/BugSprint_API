from pydantic import BaseModel

class TestCasesRequest(BaseModel):
    product_id: int
    test_scenario: str
    test_steps: str
    actual_result: str
    expected_result: str
    comment: str
    developer_comment: str



class UpdateTestCaseRequest(BaseModel):
    test_scenario: str
    test_steps: str
    actual_result: str
    expected_result: str
    comment: str
    developer_comment: str



class DeleteTestCaseRequest(BaseModel):
    testcase_id: int



class GetTestCasesRequest(BaseModel):
    pass