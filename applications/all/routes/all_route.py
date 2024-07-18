from fastapi import APIRouter, Depends, Query
from sqlalchemy.engine import Connection
from applications.all.rq_rs.rq_all import DatabaseNameRequest
from applications.all.utils.all_utils import get_all_table_data
from applications.all.utils.db import get_db_connection
from applications.all.rq_rs.rs_all import AllTablesDataResponse


router = APIRouter()

@router.post("/all_common_constants", response_model=AllTablesDataResponse)
def get_all_table_data_endpoint(request: DatabaseNameRequest):
    connection_generator = get_db_connection(request.database)
    connection = next(connection_generator)
    try:
        return get_all_table_data(connection)
    finally:
        connection_generator.close()
