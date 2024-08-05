import logging
from sqlalchemy import Table, select, MetaData
from sqlalchemy.exc import SQLAlchemyError
from config.database import ConnectionDetails
from applications.bugs_list.rq_rs.rs_bugs_list import Status, BugsListResponse, BugsList

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize metadata
metadata = ConnectionDetails.metadata

# Define the bugs_report table using existing metadata
try:
    bugs_report = Table(
        'bugs_report', metadata,
        autoload_with=ConnectionDetails.engine
    )
    #logger.debug("Table 'bugs_report' loaded successfully")
except SQLAlchemyError as e:
    #logger.error("Error loading table 'bugs_report': %s", e)
    raise

def fetch_bugs_list() -> BugsListResponse:
    query = select(bugs_report)
    try:
        #logger.debug("Executing query: %s", query)
        with ConnectionDetails.engine.connect() as connection:
            result = connection.execute(query).fetchall()
            #logger.debug("Query executed successfully, processing results")
            bugs_list = [
                BugsList(
                    ID=row[0],
                    Redirected_from=row[1],
                    Redirected_to=row[2],
                    Date=row[3],
                    Bug_identified_Time=row[4],
                    Bug_Reported_Time=row[5],
                    Reported_By=row[6],
                    Product_Name=row[7],
                    Environment=row[8],
                    Testing_Medium=row[9],
                    Scenario=row[10],
                    Description=row[11],
                    User_Data=row[12],
                    Priority=row[13],
                    Status=row[14],
                    Assignee=row[15],
                    Root_Cause_Location=row[16],
                    Root_Cause=row[17],
                    Solution=row[18],
                    Developer_Comment=row[19],
                    Tester_Comments=row[20]
                )
                for row in result
            ]
            #logger.debug("Fetched bugs list: %s", bugs_list)
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
    
