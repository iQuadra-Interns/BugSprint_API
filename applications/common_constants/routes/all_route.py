

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.engine import Connection
from applications.common_constants.rq_rs.rq_all import DatabaseNameRequest
from applications.common_constants.utils.all_utils import get_all_table_data, get_db_connection
from applications.common_constants.rq_rs.rs_all import AllTablesDataResponse
from typing import Generator

router = APIRouter()

def get_connection(request: DatabaseNameRequest) -> Generator[Connection, None, None]:
    try:
        return get_db_connection(request.database)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {e}")

@router.post("/all_common_constants", response_model=AllTablesDataResponse)
def get_all_table_data_endpoint(request: DatabaseNameRequest, connection: Connection = Depends(get_connection)):
    try:
        conn = next(connection)
        response = get_all_table_data(conn)
        return response
    finally:
        conn.close()
