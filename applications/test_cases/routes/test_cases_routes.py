import logging
from fastapi import APIRouter
from sqlalchemy import create_engine

from applications.test_cases.utils.utils_test_cases import add_test_case_details
from applications.test_cases.rq_rs.rs_test_cases import TestCasesResponse
from config.database import DatabaseDetails

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/test_cases", response_model=TestCasesResponse)
def get_test_cases():
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = add_test_case_details(engine)
    engine.dispose()
    return resp
