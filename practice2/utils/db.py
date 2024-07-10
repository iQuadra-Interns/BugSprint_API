from sqlalchemy import create_engine, MetaData, Table, Column, String

import pandas as pd # type: ignore

hostname = "localhost"
username = "root"
password = ""
database = "bug_sprint"
port = 3306


engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + hostname + ':' + str(port) + '/' + database)
metadata = MetaData()

bugs_common_constants = Table(
    'bug_add', metadata,
    Column('bug_id', String(20), primary_key=True),
    Column('bug', String(255)),
    Column('scenario', String(255)),
    Column('status', String(50)),
    Column('assignee', String(50)),
    Column('environment', String(50)),
    Column('testing_medium', String(50)),
    Column('root_cause_location', String(50)),
    Column('priority', String(50)),
    Column('description', String(255)),
    Column('user_data', String(255))
)

metadata.create_all(engine, checkfirst=True)
