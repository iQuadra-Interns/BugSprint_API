import logging
from sqlalchemy import Table
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from config.config import Config
from config.database import Tables, DatabaseDetails
from common.classes.generic import Status
from applications.admin.rq_rs.admin_rs import AddUserResponse
from typing import Optional
from applications.admin.rq_rs.admin_rq import UserInput
import random
import string
import bcrypt


logger = logging.getLogger(__name__)

def add_user_details(engine: Engine, user_info: UserInput):

    logger.info("Adding user and personal details")
    if user_info.jobrole == "admin":
        personal_details_table = Table(Tables.PERSONAL_DETAILS_ADMIN, DatabaseDetails.METADATA, autoload_with=engine)
        users_type=2
    elif user_info.jobrole == "developer":
        personal_details_table = Table(Tables.PERSONAL_DETAILS_DEVELOPER, DatabaseDetails.METADATA, autoload_with=engine)
        users_type=3
    elif user_info.jobrole == "tester":
        personal_details_table = Table(Tables.PERSONAL_DETAILS_TESTER, DatabaseDetails.METADATA, autoload_with=engine)
        users_type=4
    else:
        return AddUserResponse(
            status=Status(status=False, error="400",
                          message="Please mention the role of the user properly")
        )
    salt=bcrypt.gensalt(rounds=Config.HASHING_SALT_ROUNDS)
    random_string = ''.join(random.choices(string.ascii_letters, k=8))
    pw = bcrypt.hashpw(random_string.encode('utf-8'),salt)

    user_login_table = Table(Tables.USERS, DatabaseDetails.METADATA, autoload_with=engine)

    insert_personal_details_query = personal_details_table.insert().values(
        first_name=user_info.first_name,
        middle_name=user_info.middle_name,
        last_name=user_info.last_name,
        email = user_info.email,
        hashed_password=pw,
        password=random_string,
        previous_passwords=[],
        jobrole = user_info.jobrole,
        isd=user_info.isd,
        mobile_number=user_info.mobile_number


    )

    try:
        with engine.begin() as connection:
            res = connection.execute(insert_personal_details_query)
            category_id = res.inserted_primary_key[0]


            insert_user_login_query = user_login_table.insert().values(

                user_type = users_type,
                user_category_id=category_id,
                email=user_info.email
            )
            connection.execute(insert_user_login_query)
            logger.info("User and personal details added successfully")
            if category_id is None:
                return AddUserResponse(
                    status=Status(status=False, error="500",
                                  message="Operation Failed ,Once verify the input details")
                )

            return AddUserResponse(

                status=Status(status=True, error="no error", message="Operation successful"),
                category_id=category_id
            )
    except SQLAlchemyError as e:
        logger.error("Failed to add user: %s", e)
        return AddUserResponse(
            status=Status(status=False, error="500", war="Be cautious while entering the info",
                          message="Operation Failed due to invalid credentials")
        )