from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection
from typing import Generator

# Database configuration
hostname = "localhost"
username = "root"
password = ""
port = 3306

# Function to create engine dynamically
def create_engine_for_db(database: str) -> Engine:
    return create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')

# Function to get the database connection
def get_db_connection(database: str) -> Generator[Connection, None, None]:
    engine = create_engine_for_db(database)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()
