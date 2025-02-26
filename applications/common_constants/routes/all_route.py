import logging
from fastapi import APIRouter
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.common_constants.utils.all_utils import get_table_data, get_user_details
from applications.common_constants.rq_rs.rq_all import TableRequest
from applications.common_constants.rq_rs.rs_all import GetTableDataResponse, GetUserDetailsResponse
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/fetch-table-data", response_model=GetTableDataResponse)
def fetch_table_data(request: TableRequest) -> GetTableDataResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    table_name = request.table_name.strip() if request.table_name and request.table_name != "string" else None
    resp = get_table_data(engine, table_name)
    engine.dispose()
    return resp

@router.get("/get-user-details", response_model=GetUserDetailsResponse)
def get_user_details_endpoint() -> GetUserDetailsResponse:
    logger.info("Received request to fetch user details")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    user_details = get_user_details(engine)
    engine.dispose()
    return GetUserDetailsResponse(users=user_details)