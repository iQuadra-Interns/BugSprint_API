from sqlalchemy import create_engine,MetaData

class ConnectionDetails:
    database_type ='mysql+pymysql'
    user_name = 'satish'
    password = 'satish123'
    host = 'localhost'
    port = '3306'
    db_default_schema_name = 'bugsprint'

    connection_string = f'{database_type}://{user_name}:{password}@{host}:{port}/{db_default_schema_name}'
    engine = create_engine(connection_string)
    metadata=MetaData()

class Tables:
    user_login = "user_details"
    developer_personal_details="developer_details"
    tester_personal_detail="tester_details"