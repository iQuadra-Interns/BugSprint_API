from fastapi import APIRouter
from fastapi.requests import Request
import logging

from pydantic import EmailStr
from sqlalchemy import create_engine, MetaData

from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import SignInRs

from config.config import Config

signin_router = APIRouter()


# Fetch sign information of the user
@signin_router.post(
    "/api/sign-in",
    response_model=SignInRs,
    response_model_exclude_unset=True
)
def _(rq: Request, email: EmailStr, password: str) -> SignInRs:
    pass
