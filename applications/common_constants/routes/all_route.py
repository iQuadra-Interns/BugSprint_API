from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.engine import Connection, create_engine
from applications.common_constants.rq_rs.rq_all import DatabaseNameRequest
from applications.common_constants.utils.all_utils import get_all_table_data, get_db_connection
from applications.common_constants.rq_rs.rs_all import AllTablesDataResponse
from config.database import DatabaseDetails
from typing import Generator

router = APIRouter()

def create_engine_for_db(database: str):
    connection_string = f"{DatabaseDetails.DB_TYPE}://{DatabaseDetails.USER}:{DatabaseDetails.PASS}@{DatabaseDetails.HOST}:{DatabaseDetails.PORT}/{database}"
    return create_engine(connection_string)

def get_connection(database: str) -> Generator[Connection, None, None]:
    engine = create_engine_for_db(database)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.post("/all_common_constants", response_model=AllTablesDataResponse)
def get_all_table_data_endpoint(request: DatabaseNameRequest):
    try:
        connection = get_connection(request.database)
        conn = next(connection)
        response = get_all_table_data(conn)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    finally:
        conn.close()
