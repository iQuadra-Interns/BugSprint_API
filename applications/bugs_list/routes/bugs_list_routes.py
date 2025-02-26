import logging
from fastapi import APIRouter
from sqlalchemy import create_engine

from applications.bugs_list.utils.utils_bugs_list import fetch_bugs_list
from applications.bugs_list.rq_rs.rs_bugs_list import BugsListResponse
from config.database import DatabaseDetails

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/bugs_list", response_model=BugsListResponse)
def get_bugs_list():
    engine=create_engine(DatabaseDetails.CONNECTION_STRING)
    resp=fetch_bugs_list(engine)
    engine.dispose()
    return resp
