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

    BUG_HISTORY_TABLE = "bug_history"
    BUG_STATUS_TABLE = "bug_status"
    BUGS_TABLE = "bugs"
    COMMENTS_TABLE = "comments"
    CONSTANTS_TABLE_NAMES_TABLE = "constant_table_names"
    ENVIRONMENTS_TABLE = "environments"
    ADMIN_PERSONAL_DETAILS = "personal_details_admin"
    DEVELOPER_PERSONAL_DETAILS = "personal_details_developer"
    TESTER_PERSONAL_DETAILS = "personal_details_tester"
    PRIORITY_TABLE = "priority"
    PRODUCTS_TABLE = "products"
    ROOT_CAUSE_LOCATION_TABLE = "root_cause_location"
    SCENARIOS_TABLE = "scenarios"
    TESTING_MEDIUM_TABLE = "testing_medium"
    USER_TYPES_TABLE = "user_types"
    USERS_TABLE = "users"
    USER_DETAILS_TABLE="user_details"
    FORGOT_PASSWORD_OTP_STAGING_TABLE="forgot_password_otp_staging"
