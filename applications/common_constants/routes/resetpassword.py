import logging
from fastapi import APIRouter, Request
from sqlalchemy import create_engine
from applications.common_constants.rq_rs.reset_password_rq import ResetPasswordRq
from applications.common_constants.rq_rs.reset_password_rs import ResetPasswordRs
from applications.common_constants.utils.reset_password_utils import reset_password
from config.database import DatabaseDetails

logger = logging.getLogger()
logger.setLevel(logging.INFO)

reset_password_router = APIRouter()

@reset_password_router.post(
    "/api/common/reset-password",
    response_model=ResetPasswordRs,
    response_model_exclude_unset=True
)
def reset_password_endpoint(
        reset_pswd: ResetPasswordRq
) -> ResetPasswordRs:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    response = reset_password(engine, reset_pswd)
    engine.dispose()
    return response

