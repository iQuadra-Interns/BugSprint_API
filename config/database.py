import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()


class DatabaseDetails:
    DB_TYPE = os.getenv("DB_TYPE")
    DB_USERNAME = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DEFAULT_SCHEMA = os.getenv("DB_DEFAULT_SCHEMA_NAME")

    CONNECTION_STRING = f'{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DEFAULT_SCHEMA}'
    ENGINE = create_engine(CONNECTION_STRING)
    METADATA = MetaData(schema=DEFAULT_SCHEMA)


class Tables:
    BUG_HISTORY = "bug_history"
    BUG_STATUS = "bug_status"
    BUGS = "bugs"
    COMMENTS = "comments"
    CONSTANTS_TABLE_NAMES = "constant_table_names"
    ENVIRONMENTS = "environments"
    PERSONAL_DETAILS_ADMIN = "personal_details_admin"
    PERSONAL_DETAILS_DEVELOPER = "personal_details_developer"
    PERSONAL_DETAILS_TESTER = "personal_details_tester"
    PRIORITY = "priority"
    PRODUCTS = "products"
    ROOT_CAUSE_LOCATION = "root_cause_location"
    SCENARIOS = "scenarios"
    TESTING_MEDIUM = "testing_medium"
    USER_TYPES = "user_types"
    USERS = "users"
    FORGOT_PASSWORD_OTP_STAGING = "forgot_password_otp_staging"
    TESTCASES="testcases"


class Views:
    USER_DETAILS = "user_details"
    USER_TYPE_TO_PERSONAL_DETAILS = {
        "ADM": Tables.PERSONAL_DETAILS_ADMIN,
        "DEV": Tables.PERSONAL_DETAILS_DEVELOPER,
        "TES": Tables.PERSONAL_DETAILS_TESTER,
    }
