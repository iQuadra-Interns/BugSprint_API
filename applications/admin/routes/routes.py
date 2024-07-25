import logging
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from config.database import ConnectionDetails
from applications.admin.rq_rs.admin_rq import UserInput
from applications.admin.rq_rs.admin_rs import AddUserResponse
from common.classes.generic import Status
from applications.admin.utils.db_utils import add_user_details

logger = logging.getLogger(__name__)

add_user_router = APIRouter()

@add_user_router.post("/api/add-user", response_model=AddUserResponse)
def add_user_endpoint(user_info: UserInput) -> AddUserResponse:
    logger.info("Received request to add user")
    engine = create_engine(ConnectionDetails.connection_string)

    try:
        category_id = add_user_details(engine, user_info)
        if category_id is None:
            return AddUserResponse(
                status=Status(sts=False, err="Failed to add user and personal details",msg="Operation Failed ,Once verify the input details")
            )

        return AddUserResponse(

            status=Status(sts=True, err="no error", msg="Operation successful"),
            category_id=category_id
        )
    except Exception as e:
        logger.error("Failed to add user: %s", e)
        return AddUserResponse(
            status=Status(sts=False, err=f"{e}",war="Be cautious while entering the credentials",
                          msg="Operation Failed ")
        )

