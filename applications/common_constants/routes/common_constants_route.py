from fastapi import APIRouter, Depends, Query
from sqlalchemy.engine import Connection
from applications.common_constants.rq_rs.rq_common_constants import DatabaseNameRequest
from applications.common_constants.utils.common_constants_utils import get_all_table_data
from applications.common_constants.utils.db import get_db_connection
from applications.common_constants.rq_rs.rs_common_constants import AllTablesDataResponse


router = APIRouter()

@router.post("/common_constants", response_model=AllTablesDataResponse)
def get_all_table_data_endpoint(request: DatabaseNameRequest):
    connection_generator = get_db_connection(request.database)
    connection = next(connection_generator)
    try:
        return get_all_table_data(connection)
    finally:
        connection_generator.close()
