from fastapi import APIRouter
from sqlalchemy import create_engine
from config.database import DatabaseDetails  # Assuming this provides the DB engine
from applications.common_constants.utils.all_utils import get_table_data  # Import the function from utils.py
from applications.common_constants.rq_rs.rq_all import TableRequest  # Import the request model
from applications.common_constants.rq_rs.rs_all import GetTableDataResponse  # Import the response model

router = APIRouter()

@router.post("/fetch-table-data", response_model=GetTableDataResponse)
def fetch_table_data(request: TableRequest):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    table_name = request.table_name.strip() if request.table_name and request.table_name != "string" else None
    return get_table_data(engine,table_name)
