from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs_list.utils.db import bugs_List, engine

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
        print(f"Error fetching bugslist: {e}")
        return []
