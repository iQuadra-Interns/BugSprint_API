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

@bug_router.post("/api/add-bug", response_model=AddBugResponse)
def add_bug_endpoint(bug_info: AddBugRq) -> AddBugResponse:
    logger.info("Received request to create bug")
    engine = create_engine(ConnectionDetails.connection_string)
    try:
        bug_id = add_bug(engine, bug_info)
        if bug_id is None:
            raise HTTPException(status_code=500, detail="Failed to create bug")
        status = Status(sts=True,err="null", msg="Bug created successfully")
        return AddBugResponse(status=status,bug_id=bug_id,)
    except Exception as e:
        logger.error("Failed to create bug: %s", e)
        status = Status(sts=False, err=str(e))
        raise HTTPException(status_code=500, detail=status.dict())

@bug_router.post("/api/update-bug/{bug_id}", response_model=UpdateBugResponse)
def update_bug_endpoint(bug_id: int, bug_info: UpdateBugRq) -> UpdateBugResponse:
    logger.info("Received request to update bug with ID %s", bug_id)
    engine = create_engine(ConnectionDetails.connection_string)
    try:
        success = update_bug(engine, bug_id, bug_info)
        if not success:
            raise HTTPException(status_code=404, detail="Bug not found")
        status = Status(sts=True, err = None,msg=f"Bug updated successfully with id : {bug_id}")
        return UpdateBugResponse(status=status)
    except Exception as e:
        logger.error("Failed to update bug: %s", e)
        status = Status(sts=False, err=str(e),msg="enter proper bug_id")
        raise HTTPException(status_code=500, detail=status.dict())