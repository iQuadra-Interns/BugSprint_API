
from sqlalchemy import create_engine, MetaData

# Database configuration
hostname = "localhost"
username = "root"
password = ""
database = "bug_sprint"
port = 3306

# Create engine and metadata
engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')
metadata = MetaData()

# Reflect the metadata
metadata.reflect(bind=engine)

def create_engine_for_db(database: str):
    return create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')
