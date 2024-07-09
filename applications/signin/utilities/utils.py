import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy import Engine, MetaData, Table
from sqlalchemy import select, and_
import logging
from config.database import ConnectionDetails, Tables
from applications.signin.rq_rs.rq_signin import SignInRq
from applications.signin.rq_rs.rs_signin import PersonalDetails

logging.basicConfig(level=logging.DEBUG)


def fetch_complete_user_info(engine: Engine, sign_in_info: SignInRq):
    metadata = MetaData(schema=ConnectionDetails.db_default_schema_name)
    login_table = Table(Tables.user_login, metadata, autoload_with=engine)

    query_to_check_user_data = select(
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
            'role': user_login_info_df.iloc[0]['role'],
            'category_id': user_login_info_df.iloc[0]['category_id'],
            'email': user_login_info_df.iloc[0]['email'],
            'password': user_login_info_df.iloc[0]['password']
        }

        if user_info['role'] == 'developer':
            table = Table(Tables.developer_personal_details, metadata, autoload_with=engine)
        elif user_info['role'] == 'tester':
            table = Table(Tables.tester_personal_detail, metadata, autoload_with=engine)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid role')

        # Ensure the query includes the 'id' column
        query = select(
            table.c.id,
            table.c.first_name,
            table.c.last_name,
            table.c.phone_no,
            table.c.role_of_the_user
        ).where(
            and_(table.c.id == user_info['category_id'])
        )

        with engine.begin() as connection:
            details = pd.read_sql(query, connection)

        logging.debug(f"Fetched details DataFrame: {details}")

        if not details.empty:
            final_result = {
                'id': details.iloc[0]['id'],
                'first_name': details.iloc[0]['first_name'],
                'last_name': details.iloc[0]['last_name'],
                'phone_no': details.iloc[0]['phone_no'],
                'role_of_the_user': details.iloc[0]['role_of_the_user']
            }
            return PersonalDetails.parse_obj(final_result)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User details not found")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")
