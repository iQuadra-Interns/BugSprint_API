import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy import Engine, MetaData, Table
from sqlalchemy import select, and_
import logging
from config.database import DatabaseDetails, Tables
from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import PersonalDetails, SignInRs
from common.classes.generic import Status, UserId
from passlib.context import CryptContext

logging.basicConfig(level=logging.DEBUG)

def fetch_complete_user_info(engine: Engine, sign_in_info: SignInRq):

    users_table = Table(Tables.USERS_TABLE, DatabaseDetails.METADATA, autoload_with=engine)
    query_get_user_info = select(
        users_table.c.user_id,
        users_table.c.email,
        users_table.c.user_type,
        users_table.c.user_category_id
    ).where(users_table.c.email == sign_in_info.email)

    with engine.begin() as connection:
        user_df = pd.read_sql(query_get_user_info, connection)

    if user_df.empty:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}",
                          message="User not found")
        )


    user_info = {
        'user_id': user_df.iloc[0]['user_id'],
        'email': user_df.iloc[0]['email'],
        'user_type': user_df.iloc[0]['user_type'],
        'user_category_id':user_df.iloc[0]['user_category_id']
    }

    user_types_table = Table(Tables.USER_TYPES_TABLE, DatabaseDetails.METADATA, autoload_with=engine)
    query_get_user_type_name = select(
        user_types_table.c.user_type_name
    ).where(user_types_table.c.id == user_info['user_type'])

    with engine.begin() as connection:
        user_type_df = pd.read_sql(query_get_user_type_name, connection)

    if user_type_df.empty:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}",
                          message="Invalid user type")
        )

    user_type_name = user_type_df.iloc[0]['user_type_name']


    if user_type_name == 'DEV':
        role_table = Table(Tables.DEVELOPER_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
    elif user_type_name == 'TES':
        role_table = Table(Tables.TESTER_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
    elif user_type_name == 'ADM':
        role_table = Table(Tables.ADMIN_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)

    else:
        return SignInRs(
            status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}",
                          message="Invalid role")
        )


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

    ).where(role_table.c.id == user_info['user_category_id'])

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
        email_id=details_df.iloc[0]['email'],
        jobrole=details_df.iloc[0]['jobrole'],
        isd=details_df.iloc[0]['isd'],
        mobile_number=details_df.iloc[0]['mobile_number'],
        created_at=str(details_df.iloc[0]['created_at']),
        last_updated=str(details_df.iloc[0]['last_updated'])
    )
    hashed_pw = details_df.iloc[0]['hashed_password']

    user_id_obj = UserId(
        user_id=user_info['user_id'],
        user_category=user_type_name,
        user_cat_id=user_info['user_category_id']
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class authentication():


        def verify_password(self, plain_password, hashed_password):
            k = pwd_context.verify(plain_password, hashed_password)
            return k

    auth = authentication()
    result = auth.verify_password(sign_in_info.password,hashed_pw)
    if result == True:

        if user_type_name == 'DEV':
            return SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
                developer_details=personal_details
            )
        elif user_type_name == 'TES':
            return SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
                tester_details=personal_details
            )
        elif user_type_name == 'ADM':
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




