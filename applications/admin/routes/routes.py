import logging
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.admin.rq_rs.admin_rq import UserInput
from applications.admin.rq_rs.admin_rs import AddUserResponse
from common.classes.generic import Status
from applications.admin.utils.db_utils import add_user_details

logger = logging.getLogger(__name__)

add_user_router = APIRouter()

@add_user_router.post("/api/add-user",
                      response_model=AddUserResponse,
                      response_model_exclude_unset=True)
def add_user_endpoint(user_info: UserInput) -> AddUserResponse:
    logger.info("Received request to add user")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp=add_user_details(engine,user_info)
    return resp