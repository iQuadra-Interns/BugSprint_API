import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()


class ConnectionDetails:
    database_type = os.getenv("DB_TYPE")
    user_name = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_default_schema_name = os.getenv("DB_DEFAULT_SCHEMA_NAME")

    connection_string = f'{database_type}://{user_name}:{password}@{host}:{port}/{db_default_schema_name}'
    print(f"Connection string: {connection_string}")
    engine = create_engine(connection_string)
    metadata = MetaData()


class Tables:
    USER_LOGIN_TABLE = "user_details"
    DEVELOPER_PERSONAL_DETAILS = "developer_details"
    TESTER_PERSONAL_DETAILS = "tester_details"
    BUGS_TABLE = "bugs"
    ADMIN_PERSONAL_DETAILS = "admin_details"
