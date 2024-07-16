from fastapi import APIRouter, Depends, Query
from sqlalchemy.engine import Connection
from applications.common_constants.rq_rs.rq_common_constants import TableNameRequest
from applications.common_constants.utils.common_constants_utils import get_table_data
from applications.common_constants.utils.db import get_db_connection
from applications.common_constants.rq_rs.rs_common_constants import TableDataResponse

router = APIRouter()

@router.post("/common_constants", response_model=TableDataResponse)
def get_table_data_endpoint(request: TableNameRequest, connection: Connection = Depends(get_db_connection)):
    return get_table_data(connection, request.table_name)
