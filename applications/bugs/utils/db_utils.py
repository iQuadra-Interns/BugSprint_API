import json
import logging

import pandas as pd
from fastapi import HTTPException,status
from openpyxl.styles.builtins import warning
from sqlalchemy import MetaData, Table, insert, update, select, create_engine, and_, or_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs.rq_rs.rq_bugs import AddBugRq , UpdateBugRq
from common.classes.generic import Status
from applications.bugs.rq_rs.rs_bugs import AddBugResponse,UpdateBugResponse, FindBugResponse, BugDetails,ViewBugDetails
from config.database import Tables, DatabaseDetails, Views

logger = logging.getLogger(__name__)


def add_bug(engine: Engine, bug_info: AddBugRq):
    logger.info("Creating a new bug entry")
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS, metadata, autoload_with=engine)

    insert_into_bugs_query = bugs_table.insert().values(

        product_id=bug_info.product_id,
        title=bug_info.title,
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

    status = Status(status=False, error="Bug creation Unsuccessful", message=None)
    response = AddBugResponse(status=status, bug_id=-1)
    try:
        with engine.begin() as connection:
            res = connection.execute(insert_into_bugs_query)
            bug_id = res.inserted_primary_key[0]
            logger.info(f"Bug entry created successfully: {bug_id}")
            if bug_id:
                response = AddBugResponse(
                    status=Status(status=True, error=None, message="Bug Created Successfully"),
                    bug_id=bug_id
                )
    except SQLAlchemyError as e:
        logger.error(f"Error creating bug entry: {e}")
        response = AddBugResponse(status=Status(status=False, error="500", message="Enter Proper Bug Info"), bug_id=-1)
    finally:
        return response


def update_bug(engine: Engine, bug_id: int, bug_info: UpdateBugRq):
    logger.info("Updating an existing bug entry")
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS, metadata, autoload_with=engine)
    bug_history = Table(Tables.BUG_HISTORY, metadata, autoload_with=engine)
    reviewer = True

    # Select the current bug details
    qu = select(
        bugs_table.c.product_id,
        bugs_table.c.title,
        bugs_table.c.environment_id,
        bugs_table.c.scenario_id,
        bugs_table.c.testing_medium,
        bugs_table.c.description,
        bugs_table.c.user_data,
        bugs_table.c.priority_id,
        bugs_table.c.reported_by,
        bugs_table.c.assignee_id,
        bugs_table.c.root_cause_location,
        bugs_table.c.root_cause,
        bugs_table.c.resolution,
        bugs_table.c.status
    ).where(bugs_table.c.bug_id == bug_id)

    # Build update query
    update_bug_query = update(bugs_table).where(bugs_table.c.bug_id == bug_id).values(
        product_id=bug_info.product_id,
        title=bug_info.title,
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
            # Fetch current bug data
            old_values_list = pd.read_sql(qu, connection).to_dict('records')  # Extract the first record
            if not old_values_list:
                logger.warning("No bug entry found with the given ID")
                status = Status(status=False, error="404", message="Enter proper bug_id")
                return UpdateBugResponse(status=status)

            old_values = old_values_list[0]
            # Execute the update query
            result = connection.execute(update_bug_query)

        if result.rowcount == 0:
            logger.warning("No bug entry found with the given ID")
            status = Status(status=False, error="404", message="Enter proper bug_id")
            return UpdateBugResponse(status=status)

        # Compare old and new values and build changes dict
        changes = {}
        new_values = dict(bug_info)

        for field, old_value in old_values.items():
            new_value = new_values.get(field)
            if new_value != old_value:
                changes[field] = [old_value, new_value]  # Store only changed values

        if changes:
            changes_json = json.dumps(changes)

            # Insert the changes into bug history
            q2 = bug_history.insert().values(bug_id=bug_id, changes=changes_json, changed_by=bug_info.reported_by)
            with engine.begin() as connection:
                final_res = connection.execute(q2)

        else:
            reviewer = False

        if reviewer == True:

            logger.info("Bug entry updated successfully")
            status = Status(status=True, error=None, message=f"Bug updated successfully with id: {bug_id}")
            return UpdateBugResponse(status=status)
        elif reviewer == False:
            status = Status(status=True, error=" ", warning="no changes detected",
                            message="not inserted into bug_history")
            return UpdateBugResponse(status=status)



    except SQLAlchemyError as e:
        logger.error(f"Error updating bug entry: {e}")
        status = Status(status=False, error=str(e), message="Enter proper bug_info")
        return UpdateBugResponse(status=status)


def find_bug(engine: Engine, bug_id: int) -> FindBugResponse:
    logger.info("Finding bug entry with ID %s", bug_id)

    # Define metadata and tables
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    bugs_table = Table(Tables.BUGS, metadata, autoload_with=engine)
    products_table = Table(Tables.PRODUCTS, metadata, autoload_with=engine)
    priority_table = Table(Tables.PRIORITY, metadata, autoload_with=engine)
    environments_table = Table(Tables.ENVIRONMENTS, metadata, autoload_with=engine)
    scenarios_table = Table(Tables.SCENARIOS, metadata, autoload_with=engine)
    testing_medium_table = Table(Tables.TESTING_MEDIUM, metadata, autoload_with=engine)
    user_details_table = Table(Views.USER_DETAILS, metadata, autoload_with=engine)
    root_cause_location_table = Table(Tables.ROOT_CAUSE_LOCATION, metadata, autoload_with=engine)
    bugs_status_table = Table(Tables.BUG_STATUS, metadata, autoload_with=engine)
    user_details_table_copy = user_details_table.alias('user_details_table_copy')

    # # Query to select bug details
    select_bug_query = select(
           bugs_table.c.bug_id,
           bugs_table.c.title,
           products_table.c.product_name,
           environments_table.c.environment_name,
           scenarios_table.c.scenario_name,
           testing_medium_table.c.medium_name,
           bugs_table.c.description,
           bugs_table.c.user_data,
           priority_table.c.priority_name,
           user_details_table_copy.c.user_name.label('assignee_user_name'),
           user_details_table.c.user_name.label('reported_user_name'),
           bugs_table.c.reported_at,
           bugs_table.c.assignee_id,
           root_cause_location_table.c.location_name,
           bugs_table.c.root_cause,
           bugs_table.c.resolution,
           bugs_status_table.c.status_name,
           bugs_table.c.created_at,
           bugs_table.c.updated_at
             ).join(products_table, bugs_table.c.product_id == products_table.c.product_id
                    ).join(environments_table, bugs_table.c.environment_id == environments_table.c.environment_id
                           ).join(scenarios_table, bugs_table.c.scenario_id == scenarios_table.c.scenario_id
                                  ).join(testing_medium_table, bugs_table.c.testing_medium == testing_medium_table.c.medium_id
                                         ).join(priority_table, bugs_table.c.priority_id == priority_table.c.priority_id
                                                ).join(user_details_table, bugs_table.c.reported_by == user_details_table.c.user_id
                                                       ).join(user_details_table_copy, bugs_table.c.assignee_id == user_details_table_copy.c.user_id
                                                            ).join(root_cause_location_table,bugs_table.c.root_cause_location == root_cause_location_table.c.location_id
                                                                   ).join(bugs_status_table,bugs_table.c.status == bugs_status_table.c.status_id
                                                                         ).where(and_(bugs_table.c.bug_id == bug_id))

    try:
        with engine.begin() as connection:
            result = pd.read_sql(select_bug_query, connection).to_dict('records')

        # # Check if the result is empty
        if len(result) == 0:
            logger.warning("No bug entry found with the given ID %s", bug_id)
            status = Status(status=False, error="404", message="Bug not found")
            return FindBugResponse(status=status)

        bug_details = ViewBugDetails(

            bug_id=result[0]['bug_id'],
            title=result[0]['title'],
            product=result[0]['product_name'],
            environment=result[0]['environment_name'],
            scenario=result[0]['scenario_name'],
            testing_medium=result[0]['medium_name'],
            description=result[0]['description'],
            user_data=result[0]['user_data'],
            priority=result[0]['priority_name'],
            reported_by=result[0]['reported_user_name'],
            reported_at=result[0]['reported_at'],
            assignee=result[0]['assignee_user_name'],  # This will be replaced later
            root_cause_location=result[0]['location_name'],
            root_cause=result[0]['root_cause'],
            resolution=result[0]['resolution'],
            status=result[0]['status_name'],
            created_at=result[0]['created_at'],
            updated_at=result[0]['updated_at']
        )

        status = Status(status=True, error=None, message="Bug found successfully")
        return FindBugResponse(status=status, bug_details=bug_details)

    except SQLAlchemyError as e:
        logger.error(f"Error finding bug entry: {e}")
        status = Status(status=False, error=str(e), message="Operation Failed")
        return FindBugResponse(status=status)
