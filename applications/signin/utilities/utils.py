import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy import Engine, MetaData, Table
from sqlalchemy import select, and_
import logging
from config.database import DatabaseDetails, Tables
from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import PersonalDetails,SignInRs
from common.classes.generic import Status, UserId

logging.basicConfig(level=logging.DEBUG)


def fetch_complete_user_info(engine: Engine, sign_in_info: SignInRq):
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    login_table = Table(Tables.USER_LOGIN_TABLE, DatabaseDetails.METADATA, autoload_with=engine)

    # Step 1: Get the use type from users table if the user exists
    query_get_user_type = select
    # Step 2: Get the hashed password and other details from respective user_type_personal details

    # Step 3: check if the hashed password matches and give appropriate response
    query_to_check_user_data = select(
        login_table.c.id,
        login_table.c.role,
        login_table.c.category_id,
        login_table.c.email,
        login_table.c.password
    ).where(
        and_(
            login_table.c.email == sign_in_info.email,
            login_table.c.password == sign_in_info.password
        )
    )

    with engine.begin() as connection:
        user_login_info_df = pd.read_sql(query_to_check_user_data, connection)

    if not user_login_info_df.empty:
        user_info = {
            'id': user_login_info_df.iloc[0]['id'],
            'role': user_login_info_df.iloc[0]['role'],
            'category_id': user_login_info_df.iloc[0]['category_id'],
            'email': user_login_info_df.iloc[0]['email'],
            'password': user_login_info_df.iloc[0]['password']
        }

        if user_info['role'] == 'developer':
            table_to_access = Table(Tables.DEVELOPER_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
            details_field = 'developer_details'
        elif user_info['role'] == 'tester':
            table_to_access = Table(Tables.TESTER_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
            details_field = 'tester_details'
        elif user_info['role'] == 'admin':
            table_to_access = Table(Tables.ADMIN_PERSONAL_DETAILS, DatabaseDetails.METADATA, autoload_with=engine)
            details_field = 'admin_details'
        else:
            resp = SignInRs(
                status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}",
                              message="Operation failed due to invalid role"))
            return resp


        query = select(
            table_to_access.c.id,
            table_to_access.c.first_name,
            table_to_access.c.last_name,
            table_to_access.c.phone_no,
            table_to_access.c.role_of_the_user
        ).where(
            and_(table_to_access.c.id == user_info['category_id'])
        )

        with engine.begin() as connection:
            details = pd.read_sql(query, connection)

        logging.debug(f"Fetched details DataFrame: {details}")

        if not details.empty:
            personal_details_obj = PersonalDetails(
                first_name=details.iloc[0]['first_name'],
                last_name=details.iloc[0]['last_name'],
                email_id=user_info['email'],
                mobile_no=details.iloc[0]['phone_no']
            )
            user_id_obj = UserId(
                user_id=user_info['id'],
                user_category=user_info['role'],
                user_cat_id=details.iloc[0]['id']
            )

            sign_in_response = SignInRs(
                status=Status(status=True, error="no error", message="Operation successful"),
                usr=user_id_obj,
            )
            setattr(sign_in_response, details_field, personal_details_obj)

            return sign_in_response
        else:
            resp = SignInRs(status=Status(status=True, error=f"{status.HTTP_404_NOT_FOUND}", message="Operation failed because user personal details are misssing"))
            return resp
    else:
        resp = SignInRs(
            status=Status(status=False, error=f"{status.HTTP_401_UNAUTHORIZED}", message="Operation failed due to invalid credentials"))
        return resp
        
