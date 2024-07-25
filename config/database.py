


from sqlalchemy import create_engine,MetaData

class ConnectionDetails:
    database_type ='mysql+pymysql'
    user_name = 'root'
    password = ''
    host = 'localhost'
    port = '3306'
    db_default_schema_name = 'bug_sprint'

    connection_string = f'{database_type}://{user_name}:{password}@{host}:{port}/{db_default_schema_name}'
    engine = create_engine(connection_string)
    metadata=MetaData()
    metadata.reflect(bind=engine)

class Tables:
    USER_LOGIN_TABLE = "user_details"
    DEVELOPER_PERSONAL_DETAILS = "developer_details"
    TESTER_PERSONAL_DETAILS = "tester_details"
    BUGS_TABLE = "bugs"
    ADMIN_PERSONAL_DETAILS ="admin_details"

def create_engine_for_db(database: str):
    return create_engine(f'{database_type}://{user_name}:{password}@{host}:{port}/{db_default_schema_name}')
