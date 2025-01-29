import logging
from fastapi import APIRouter
from sqlalchemy import create_engine
from applications.test_cases.utils.utils_test_cases import add_test_case_details,update_test_case_details,delete_test_case,get_test_cases
from applications.test_cases.rq_rs.rs_test_cases import TestCasesResponse,UpdateTestCaseResponse,DeleteTestCaseResponse,GetTestCasesResponse
from applications.test_cases.rq_rs.rq_test_cases import TestCasesRequest,UpdateTestCaseRequest
from config.database import DatabaseDetails

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/add-test-case",
             response_model=TestCasesResponse,
             response_model_exclude_unset=True)
def add_test_case_endpoint(test_case_info: TestCasesRequest) -> TestCasesResponse:
    logger.info("Received request to add a new test case")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = add_test_case_details(engine, test_case_info)
    engine.dispose()
    return resp




@router.post(
    "/api/update-test-case",
    response_model=UpdateTestCaseResponse,
    response_model_exclude_unset=True
)
def update_test_case_endpoint(testcase_id: int, test_case_info: UpdateTestCaseRequest) -> UpdateTestCaseResponse:
    logger.info("Received request to update test case with ID %s", testcase_id)
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = update_test_case_details(engine, testcase_id, test_case_info)
    return resp





@router.delete("/api/delete-test-case/{testcase_id}", response_model=DeleteTestCaseResponse)
def delete_test_case_endpoint(testcase_id: int) -> DeleteTestCaseResponse:
    logger.info(f"Received request to delete test case with ID {testcase_id}")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = delete_test_case(engine, testcase_id)
    return resp





@router.get("/api/get-test-cases", response_model=GetTestCasesResponse)
def get_test_cases_endpoint():
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = get_test_cases(engine)
    engine.dispose()
    return resp