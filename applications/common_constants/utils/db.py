from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.engine import Engine

# Database configuration
hostname = "localhost"
username = "root"
password = ""
database = "common_constants"
port = 3306

# Create an engine
engine: Engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')

# Create MetaData instance
metadata = MetaData()

# Function to get the database connection
def get_db_connection():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

# Reflect existing tables
metadata.reflect(bind=engine)
