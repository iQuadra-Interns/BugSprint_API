import logging

import pandas as pd
from sqlalchemy import Table, select, MetaData
from sqlalchemy.exc import SQLAlchemyError
from config.database import DatabaseDetails
from applications.bugs_list.rq_rs.rs_bugs_list import Status, BugsListResponse, Bug

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def fetch_bugs_list() -> BugsListResponse:
    metadata = DatabaseDetails.METADATA
    # Define the bugs_report table using existing metadata
    try:
        bugs_report = Table(
            'bugs_report', metadata,
            autoload_with=DatabaseDetails.ENGINE
        )
        # logger.debug("Table 'bugs_report' loaded successfully")
    except SQLAlchemyError as e:
        # logger.error("Error loading table 'bugs_report': %s", e)
        raise

    query = select(bugs_report)
    try:
        #logger.debug("Executing query: %s", query)
        with DatabaseDetails.ENGINE.connect() as connection:
            result = pd.read_sql(query, connection)
            #logger.debug("Query executed successfully, processing results")
            bugs_list = []
            for index, row in result.iterrows():
                bug = Bug(
                    id=row["id"],
                    product=row["product"],
                    environment=row["environment"],
                    scenario=row["scenario"],
                    testing_medium=row["testing_medium"],
                    description=row["description"],
                    user_data=row["user_data"],
                    priority=row["priority"],
                    reported_by=row["reported_by"],
                    reported_at=row["reported_at"],
                    assignee=row["assignee_id"],
                    root_cause_location=row["route_cause_location"],
                    root_cause=row["root_cause"],
                    resolution=row["resolution"],
                    status=row["status"],
                    created_At=row["created_at"],
                    updated_At=row["updated_at"]
                )
                logger.debug("Fetched bugs list: %s", bugs_list)
            return BugsListResponse(
                status=Status(sts=True, msg="Fetched successfully"),
                data=bugs_list
            )
    except SQLAlchemyError as e:
        #logger.error("Error fetching bugs list: %s", e)
        return BugsListResponse(
            status=Status(sts=False, err=f"Error fetching bugs list: {e}"),
            data=[]
        )


# Example usage (for testing purposes)
if __name__ == "__main__":
    response = fetch_bugs_list()
