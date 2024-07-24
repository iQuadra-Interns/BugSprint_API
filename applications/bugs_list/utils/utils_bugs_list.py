# applications/bugs_list/utils/utils_bugs_list.py
import sys
import os

# Add the project root directory to the Python path

sys.path.append('/home/sanju/Documents/Intern_work/BugSprint_API')

from sqlalchemy import Table, Column, String, select
from sqlalchemy.exc import SQLAlchemyError
from config.database import engine, metadata

# Define the bugs_List table
bugs_List = Table(
    'bugs_list', metadata,
    Column('bug_id', String(20), primary_key=True),
    Column('bug', String(255)),
    Column('scenario', String(255)),
    Column('status', String(50)),
    Column('assignee', String(50))
)

metadata.create_all(engine)

def fetch_bugs_list():
    query = select(
        bugs_List.c.bug_id,
        bugs_List.c.bug,
        bugs_List.c.scenario,
        bugs_List.c.status,
        bugs_List.c.assignee
    )
    try:
        with engine.connect() as connection:
            result = connection.execute(query).fetchall()
            constants = [
                {
                    "bug_id": row.bug_id,
                    "bug": row.bug,
                    "scenario": row.scenario,
                    "status": row.status,
                    "assignee": row.assignee
                }
                for row in result
            ]
        return constants
    except SQLAlchemyError as e:
        print(f"Error fetching bugs list: {e}")
        return []
