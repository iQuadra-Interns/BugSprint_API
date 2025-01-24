import logging
from fastapi import APIRouter
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.bugs.rq_rs.rq_bugs import AddBugRq, UpdateBugRq
from applications.bugs.rq_rs.rs_bugs import AddBugResponse, UpdateBugResponse, FindBugResponse, BugDetails
from applications.bugs.utils.db_utils import add_bug, update_bug, find_bug

logger = logging.getLogger(__name__)

bug_router = APIRouter()


@bug_router.post("/api/add-bug",
                 response_model=AddBugResponse,
                 response_model_exclude_unset=True)
def add_bug_endpoint(bug_info: AddBugRq) -> AddBugResponse:
    logger.info("Received request to create bug")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = add_bug(engine, bug_info)
    return resp


@bug_router.post("/api/update-bug",
                 response_model=UpdateBugResponse,
                 response_model_exclude_unset=True)
def update_bug_endpoint(bug_id: int, bug_info: UpdateBugRq) -> UpdateBugResponse:
    logger.info("Received request to update bug with ID %s", bug_id)
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = update_bug(engine, bug_id, bug_info)
    return resp


@bug_router.get("/api/find-bug",
                response_model=FindBugResponse,
                response_model_exclude_unset=True)
def find_bug_endpoint(bug_id: int) -> FindBugResponse:
    logger.info("Received request to find bug with ID %s", bug_id)
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = find_bug(engine, bug_id)
    return resp
