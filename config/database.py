from sqlalchemy import create_engine, MetaData, Table, Column, String

import pandas as pd # type: ignore

hostname = "localhost"
username = "root"
password = ""
database = "bug_sprint"
port = 3306


engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + hostname + ':' + str(port) + '/' + database)
metadata = MetaData()
