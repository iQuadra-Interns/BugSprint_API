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

from sqlalchemy import select, insert, update, delete
from applications.admin.rq_rs.admin_rs import GenericResponse
from applications.admin.rq_rs.admin_rq import (ProductRQ, ScenarioRQ)
from applications.admin.rq_rs.admin_rs import (ProductRS, ScenarioRS)


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
            status=Status(status=False, error="This email is already registered")
        )


# PRODUCTS
def add_product(engine: Engine, product_info: ProductRQ):
    table = Table(Tables.PRODUCTS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(insert(table).values(product_name=product_info.product_name))
        return GenericResponse(status=Status(status=True, message="Product added"))
    except SQLAlchemyError as e:
        logger.error("add_product error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to add product"))

def get_products(engine: Engine):
    table = Table(Tables.PRODUCTS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.connect() as conn:
            results = conn.execute(select(table)).mappings().all()
            return ProductRS(
                status=Status(status=True, message="Fetched products"),
                products=[dict(row) for row in results]
            )
    except SQLAlchemyError as e:
        logger.error("get_products error: %s", e)
        return ProductRS(status=Status(status=False, error="500", message="Failed to fetch products"))

def update_product(engine: Engine, product_id: int, product_info: ProductRQ):
    table = Table(Tables.PRODUCTS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(update(table).where(table.c.product_id == product_id).values(product_name=product_info.product_name))
        return GenericResponse(status=Status(status=True, message="Product updated"))
    except SQLAlchemyError as e:
        logger.error("update_product error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to update product"))

def delete_product(engine: Engine, product_id: int):
    product_table = Table(Tables.PRODUCTS, DatabaseDetails.METADATA, autoload_with=engine)
    scenario_table = Table(Tables.SCENARIOS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(delete(scenario_table).where(scenario_table.c.product_id == product_id))
            conn.execute(delete(product_table).where(product_table.c.product_id == product_id))
        return GenericResponse(status=Status(status=True, message="Product and related scenarios deleted"))
    except SQLAlchemyError as e:
        logger.error("delete_product error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to delete product"))
    
# SCENARIOS
def add_scenario(engine: Engine, scenario_info: ScenarioRQ):
    table = Table(Tables.SCENARIOS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(insert(table).values(scenario_name=scenario_info.scenario_name, product_id=scenario_info.product_id))
        return GenericResponse(status=Status(status=True, message="Scenario added"))
    except SQLAlchemyError as e:
        logger.error("add_scenario error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to add scenario"))

def get_scenarios_by_product(engine: Engine, product_id: int):
    table = Table(Tables.SCENARIOS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.connect() as conn:
            stmt = select(table).where(table.c.product_id == product_id)
            results = conn.execute(stmt).mappings().all()
            return ScenarioRS(
                status=Status(status=True, message="Fetched scenarios"),
                scenarios=[dict(row) for row in results]
            )
    except SQLAlchemyError as e:
        logger.error("get_scenarios_by_product error: %s", e)
        return ScenarioRS(status=Status(status=False, error="500", message="Failed to fetch scenarios"))

def update_scenario(engine: Engine, scenario_id: int, scenario_info: ScenarioRQ):
    table = Table(Tables.SCENARIOS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(update(table).where(table.c.scenario_id == scenario_id).values(scenario_name=scenario_info.scenario_name, product_id=scenario_info.product_id))
        return GenericResponse(status=Status(status=True, message="Scenario updated"))
    except SQLAlchemyError as e:
        logger.error("update_scenario error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to update scenario"))

def delete_scenario(engine: Engine, scenario_id: int):
    table = Table(Tables.SCENARIOS, DatabaseDetails.METADATA, autoload_with=engine)
    try:
        with engine.begin() as conn:
            conn.execute(delete(table).where(table.c.scenario_id == scenario_id))
        return GenericResponse(
            status=Status(status=True, message="Scenario deleted"))
    except SQLAlchemyError as e:
        logger.error("delete_scenario error: %s", e)
        return GenericResponse(status=Status(status=False, error="500", message="Failed to delete scenario"))


