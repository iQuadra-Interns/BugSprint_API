import sys
import os

sys.path.append('/home/sanju/Documents/Intern_work/BugSprint_API')

from sqlalchemy import Table, select
from sqlalchemy.exc import SQLAlchemyError
from config.database import ConnectionDetails
from applications.bugs_list.rq_rs.rs_bugs_list import BugsList, Status, BugsListResponse

# Define the bugs_List table using existing metadata
bugs_List = Table(
    'bugs_list', ConnectionDetails.metadata,
    autoload_with=ConnectionDetails.engine
)

def fetch_bugs_list() -> BugsListResponse:
    query = select(
        bugs_List.c.bug_id,
        bugs_List.c.bug,
        bugs_List.c.scenario,
        bugs_List.c.status,
        bugs_List.c.assignee
    )
    try:
        with ConnectionDetails.engine.connect() as connection:
            result = connection.execute(query).fetchall()
            bugs_list = [
                BugsList(
                    bug_id=row.bug_id,
                    bug=row.bug,
                    scenario=row.scenario,
                    status=row.status,
                    assignee=row.assignee
                )
                for row in result
            ]
            return BugsListResponse(
                status=Status(sts=True, msg="Fetched successfully"),
                data=bugs_list
            )
    except SQLAlchemyError as e:
        return BugsListResponse(
            status=Status(sts=False, err=f"Error fetching bugs list: {e}"),
            data=[]
        )
