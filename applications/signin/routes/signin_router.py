from fastapi import APIRouter
from fastapi.requests import Request
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import SignInRs
from applications.signin.utilities.utils import fetch_complete_user_info
signin_router = APIRouter()


# Fetch sign information of the user
@signin_router.post(
    "/api/sign-in",
    response_model=SignInRs,
    response_model_exclude_unset=True
)
def sign_in_info(rq: Request, sign_in: SignInRq) -> SignInRs:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    user = fetch_complete_user_info(engine, sign_in)
    engine.dispose()
    return user
