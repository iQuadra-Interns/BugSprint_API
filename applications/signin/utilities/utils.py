import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy import Engine, MetaData, Table
from sqlalchemy import select, and_
import logging
from config.database import DatabaseDetails, Tables, Views
from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import PersonalDetails, SignInRs
from common.classes.generic import Status, UserId
from passlib.context import CryptContext

logging.basicConfig(level=logging.DEBUG)


def fetch_complete_user_info(engine: Engine, sign_in_info: SignInRq):
    user_details_table = Table(Views.USER_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
    user_info_query = select(user_details_table).where(and_(user_details_table.c.email == sign_in_info.email))

    with engine.begin() as connection:
        user_df = pd.read_sql(user_info_query, connection)

    if user_df.empty:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}",
                          message="User not found")
        )

    user_details = user_df.iloc[0].to_dict()

    role_table = Table(Views.USER_TYPE_TO_PERSONAL_DETAILS[user_details["user_type_name"]],
                       DatabaseDetails.METADATA, autoload_with=engine)

    query_get_personal_details = select(
        role_table.c.id,
        role_table.c.first_name,
        role_table.c.middle_name,
        role_table.c.last_name,
        role_table.c.email,
        role_table.c.jobrole,
        role_table.c.isd,
        role_table.c.mobile_number,
        role_table.c.account_status,
        role_table.c.created_at,
        role_table.c.last_updated,
        role_table.c.hashed_password

    ).where(and_(role_table.c.id == user_details["user_category_id"]))

    with engine.begin() as connection:
        details_df = pd.read_sql(query_get_personal_details, connection)

    if details_df.empty:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_404_NOT_FOUND}",
                          message="Personal details not found")
        )

    personal_details = PersonalDetails(
        first_name=details_df.iloc[0]['first_name'],
        middle_name=details_df.iloc[0]['middle_name'],
        last_name=details_df.iloc[0]['last_name'],
        email=details_df.iloc[0]['email'],
        job_role=details_df.iloc[0]['jobrole'],
        isd=details_df.iloc[0]['isd'],
        mobile_number=details_df.iloc[0]['mobile_number'],
        created_at=details_df.iloc[0]['created_at'],
        last_updated=details_df.iloc[0]['last_updated']
    )
    hashed_pw = details_df.iloc[0]['hashed_password']

    user_id_obj = UserId(
        user_id=user_details['user_id'],
        user_category=user_details["user_type_name"],
        user_cat_id=user_details['user_category_id']
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class authentication():

        def verify_password(self, plain_password, hashed_password):
            k = pwd_context.verify(plain_password, hashed_password)
            return k

    auth = authentication()
    result = auth.verify_password(sign_in_info.password, hashed_pw)

    if result:
        if user_details["user_type_name"] == 'DEV':
            return SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
                developer_details=personal_details
            )
        elif user_details["user_type_name"] == 'TES':
            return SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
                tester_details=personal_details
            )
        elif user_details["user_type_name"] == 'ADM':
            return SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
                admin_details=personal_details
            )
    else:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_404_NOT_FOUND}",
                          message="Incorrect Password")
        )
