import logging
from sqlalchemy import MetaData, Table, insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from config.database import Tables, ConnectionDetails
from common.classes.generic import Status
from applications.admin.rq_rs.admin_rs import AddUserResponse
from typing import Optional
from applications.admin.rq_rs.admin_rq import UserInput

logger = logging.getLogger(__name__)

def add_user_details(engine: Engine, user_info: UserInput):
    logger.info("Adding user and personal details")
    metadata = MetaData(schema=ConnectionDetails.db_default_schema_name)
    if user_info.role == "admin":
        personal_details_table = Table(Tables.ADMIN_PERSONAL_DETAILS, metadata, autoload_with=engine)
    elif user_info.role == "developer":
        personal_details_table = Table(Tables.DEVELOPER_PERSONAL_DETAILS, metadata, autoload_with=engine)
    elif user_info.role == "tester":
        personal_details_table = Table(Tables.TESTER_PERSONAL_DETAILS, metadata, autoload_with=engine)
    else:
        return AddUserResponse(
            status=Status(sts=False, err="400",
                          msg="Please mention the role of the user properly")
        )


    user_login_table = Table(Tables.USER_LOGIN_TABLE, metadata, autoload_with=engine)

    insert_personal_details_query = personal_details_table.insert().values(
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        phone_no=user_info.phone_no,
        role_of_the_user=user_info.role
    )

    try:
        with engine.begin() as connection:
            res = connection.execute(insert_personal_details_query)
            category_id = res.inserted_primary_key[0]


            insert_user_login_query = user_login_table.insert().values(
                email=user_info.email,
                password=user_info.password,
                role=user_info.role,
                category_id=category_id
            )
            connection.execute(insert_user_login_query)
            logger.info("User and personal details added successfully")
            if category_id is None:
                return AddUserResponse(
                    status=Status(sts=False, err="500",
                                  msg="Operation Failed ,Once verify the input details")
                )

            return AddUserResponse(

                status=Status(sts=True, err="no error", msg="Operation successful"),
                category_id=category_id
            )
    except SQLAlchemyError as e:
        logger.error("Failed to add user: %s", e)
        return AddUserResponse(
            status=Status(sts=False, err="500", war="Be cautious while entering the info",
                          msg="Operation Failed due to invalid credentials")
        )
