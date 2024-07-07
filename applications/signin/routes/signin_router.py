from fastapi import APIRouter
from fastapi.requests import Request
import logging

from pydantic import EmailStr
from sqlalchemy import create_engine, MetaData
from config.database import ConnectionDetails

from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import SignInRs,personal_details
from applications.signin.utilities.utils import fetch_complete_user_info

from config.config import Config

signin_router = APIRouter()


# Fetch sign information of the user
@signin_router.post(
    "/api/sign-in",
    response_model=personal_details,
    response_model_exclude_unset=True
)
def sign_in_info(rq: Request,sign_in:SignInRq) -> SignInRs:
    engine=create_engine(ConnectionDetails.connection_string)
    user=fetch_complete_user_info(engine,sign_in)
    return user
