from sqlalchemy import create_engine, MetaData, Table, Column, String

import pandas as pd # type: ignore

hostname = "localhost"
username = "root"
password = ""
database = "bug_sprint"
port = 3306


engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + hostname + ':' + str(port) + '/' + database)
metadata = MetaData()


bugs_List = Table(
    'bugs_list', metadata,
    Column('bug_id', String(20), primary_key=True),
    Column('bug', String(255)),
    Column('scenario', String(255)),
    Column('status', String(50)),
    Column('assignee', String(50))
)

metadata.create_all(engine)

