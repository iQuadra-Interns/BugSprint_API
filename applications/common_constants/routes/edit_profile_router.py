import logging
from fastapi import APIRouter
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.common_constants.rq_rs.edit_profile_rq import EditProfileRequest
from applications.common_constants.rq_rs.edit_profile_rs import EditProfileResponse
from applications.common_constants.utils.edit_profile_utils import edit_user_profile

logger = logging.getLogger(__name__)

edit_profile_router = APIRouter()


@edit_profile_router.put("/api/edit-profile/{user_id}", response_model=EditProfileResponse)
def edit_profile_endpoint(
        user_id: int,
        profile_data: EditProfileRequest
) -> EditProfileResponse:
    logger.info(f"Received request to edit profile for user_id: {user_id}")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = edit_user_profile(engine, user_id, profile_data)
    engine.dispose()
    return resp
