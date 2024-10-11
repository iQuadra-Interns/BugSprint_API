import logging

import pandas as pd
from fastapi import HTTPException,status
from sqlalchemy import MetaData, Table, insert ,update ,select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs.rq_rs.rq_bugs import AddBugRq , UpdateBugRq
from common.classes.generic import Status
from applications.bugs.rq_rs.rs_bugs import AddBugResponse,UpdateBugResponse, FindBugResponse, BugDetails
from config.database import Tables, DatabaseDetails

logger = logging.getLogger(__name__)


def add_bug(engine: Engine, bug_info: AddBugRq):
    logger.info("Creating a new bug entry")
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS_TABLE, metadata, autoload_with=engine)

    insert_into_bugs_query = bugs_table.insert().values(

        product_id=bug_info.product_id,
        environment_id=bug_info.environment_id,
        scenario_id=bug_info.scenario_id,
        testing_medium=bug_info.testing_medium,
        description=bug_info.description,
        user_data=bug_info.user_data,
        priority_id=bug_info.priority_id,
        reported_by=bug_info.reported_by,
        assignee_id=bug_info.assignee_id,
        root_cause_location=bug_info.root_cause_location,
        root_cause=bug_info.root_cause,
        resolution=bug_info.resolution,
        status=bug_info.status
    )

    try:
        with engine.begin() as connection:
            res = connection.execute(insert_into_bugs_query)
            bug_id = res.inserted_primary_key[0]
            print(bug_id)
            logger.info("Bug entry created successfully")
            if bug_id is None:
                print("If bug id is none.")
                status = Status(status=False, error="500", message="Operation Failed")
                return AddBugResponse(status=status, bug_id=0)

            status = Status(status=True, error="null", message="Bug created successfully")
            return AddBugResponse(status=status, bug_id=bug_id)
    except SQLAlchemyError as e:

        print("Caught the error here.")
        logger.error(f"Error creating bug entry: {e}")
        status = Status(status=False, error="500", message="Operation Failed")
        return AddBugResponse(status=status, bug_id=0)


def update_bug(engine: Engine, bug_id: int, bug_info: UpdateBugRq) :
    logger.info("Updating an existing bug entry")
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS_TABLE, metadata, autoload_with=engine)

    update_bug_query = update(bugs_table).where(bugs_table.c.bug_id == bug_id).values(
        product_id=bug_info.product_id,
        environment_id=bug_info.environment_id,
        scenario_id=bug_info.scenario_id,
        testing_medium=bug_info.testing_medium,
        description=bug_info.description,
        user_data=bug_info.user_data,
        priority_id=bug_info.priority_id,
        reported_by=bug_info.reported_by,
        assignee_id=bug_info.assignee_id,
        root_cause_location=bug_info.root_cause_location,
        root_cause=bug_info.root_cause,
        resolution=bug_info.resolution,
        status=bug_info.status
    )

    try:
        with engine.begin() as connection:
            result = connection.execute(update_bug_query)

            if result.rowcount == 0:
                logger.warning("No bug entry found with the given ID")
                status = Status(status=False, error="404", message="enter proper bug_id")
                raise HTTPException(status_code=404, detail=status.dict())

            logger.info("Bug entry updated successfully")
            status = Status(status=True, error=None, message=f"Bug updated successfully with id : {bug_id}")
            return UpdateBugResponse(status=status)
    except SQLAlchemyError as e:
        logger.error(f"Error updating bug entry: {e}")
        status = Status(status=False, error=str(e), message="enter proper bug_info")
        raise HTTPException(status_code=500, detail=status.dict())
    

def find_bug(engine: Engine, bug_id: int) -> FindBugResponse:
    logger.info("Finding bug entry with ID %s", bug_id)
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS_TABLE, metadata, autoload_with=engine)

    select_bug_query = select(bugs_table).where(bugs_table.c.bug_id == bug_id)

    try:
        with engine.connect() as connection:
            result = pd.read_sql(select_bug_query,connection)
            if result is None:
                logger.warning("No bug entry found with the given ID %s", bug_id)
                status = Status(status=False, error="404", message="Bug not found")
                return FindBugResponse(status=status, bug=None)

            # Access by index if using tuple
            bug_details = BugDetails(
                bug_id = result.iloc[0]['bug_id'],
                product_id = result.iloc[0]['product_id'],
                environment_id = result.iloc[0]['environment_id'],
                scenario_id = result.iloc[0]['scenario_id'],
                testing_medium = result.iloc[0]['testing_medium'],
                description=result.iloc[0]['description'],
                user_data=result.iloc[0]['user_data'],
                priority_id = result.iloc[0]['priority_id'],
                reported_by = result.iloc[0]['reported_by'],
                reported_at = result.iloc[0]['reported_at'],
                assignee_id = result.iloc[0]['assignee_id'],
                root_cause_location = result.iloc[0]['root_cause_location'],
                root_cause=result.iloc[0]['root_cause'],
                resolution = result.iloc[0]['resolution'],
                status = result.iloc[0]['status'],
                created_at = result.iloc[0]['created_at'],
                updated_at = result.iloc[0]['updated_at']
            )

            status = Status(status=True, error=None, message="Bug found successfully")
            return FindBugResponse(status=status, bug=bug_details)
    except SQLAlchemyError as e:
        logger.error(f"Error finding bug entry: {e}")
        status = Status(status=False, error=str(e), message="Operation Failed")
        return FindBugResponse(status=status, bug=None)

