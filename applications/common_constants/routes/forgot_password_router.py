import logging
from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import EmailStr
from sqlalchemy import create_engine
from applications.common_constants.rq_rs.forgot_password_rq import ForgotPasswordRq, ForgotPasswordVerifyEmailRq, \
    ForgotPasswordGenerateOTPRq
from applications.common_constants.rq_rs.forgot_password_rs import UserLoginRs, ForgotPasswordRs
from applications.common_constants.utils.forgot_password_utils import check_login, update_user_info_in_staging_tbl, \
    verify_forgot_password_email_otp, forgot_password_information
from config.database import DatabaseDetails

logger = logging.getLogger()
logger.setLevel(logging.INFO)

forgot_password_router = APIRouter()


@forgot_password_router.get(
    "/api/common/forgot-password/check-email",
    response_model=UserLoginRs,
    response_model_exclude_unset=True
)
def email_check(rq: Request, login: EmailStr):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    resp = check_login(engine, login)
    engine.dispose()
    return resp


@forgot_password_router.post(
    "/api/common/forgot-password/generate-store-otp",
    response_model=ForgotPasswordRs,
    response_model_exclude_unset=True
)
def forgot_password_generate_and_store_otp(
        rq: Request,
        forgot_pswd: ForgotPasswordGenerateOTPRq
) -> ForgotPasswordRs:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    sent_otp = update_user_info_in_staging_tbl(engine, forgot_pswd)
    engine.dispose()
    return sent_otp


@forgot_password_router.post(
    "/api/common/forgot-password/verify-send-email-otp",
    response_model=ForgotPasswordRs,
    response_model_exclude_unset=True
)
def forgot_password_verify_otp(
        rq: Request,
        forgot_pswd: ForgotPasswordVerifyEmailRq
) -> ForgotPasswordRs:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    verify_otp = verify_forgot_password_email_otp(engine, forgot_pswd)
    engine.dispose()
    return verify_otp


@forgot_password_router.post(
    "/api/common/forgot-password/change-forgot-password",
    response_model=ForgotPasswordRs,
    response_model_exclude_unset=True
)
def _forgot_password_(
        rq: Request,
        forgot_pswd: ForgotPasswordRq
) -> ForgotPasswordRs:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    forgot_pswd = forgot_password_information(engine, forgot_pswd)
    engine.dispose()
    return forgot_pswd