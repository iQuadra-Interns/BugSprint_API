import logging
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from config.database import ConnectionDetails
from applications.bugs.rq_rs.rq_bugs import AddBugRq,UpdateBugRq
from applications.bugs.rq_rs.rs_bugs import AddBugResponse,UpdateBugResponse
from applications.bugs.utils.db_utils import add_bug,update_bug
from common.classes.generic import Status

logger = logging.getLogger(__name__)

bug_router = APIRouter()

@bug_router.post("/api/add-bug",
                 response_model=AddBugResponse,
                 response_model_exclude_unset=True)
def add_bug_endpoint(bug_info: AddBugRq) -> AddBugResponse:
    logger.info("Received request to create bug")
    engine = create_engine(ConnectionDetails.connection_string)
    resp=add_bug(engine,bug_info)
    return resp

@bug_router.post("/api/update-bug/{bug_id}",
                 response_model=UpdateBugResponse,
                 response_model_exclude_unset=True)
def update_bug_endpoint(bug_id: int, bug_info: UpdateBugRq) -> UpdateBugResponse:
    logger.info("Received request to update bug with ID %s", bug_id)
    engine = create_engine(ConnectionDetails.connection_string)
    resp = update_bug(engine,bug_id,bug_info)
    return resp