import json
import logging
import pandas as pd
from sqlalchemy import MetaData, Table, select, create_engine, outerjoin
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from config.database import Tables, DatabaseDetails, Views
from applications.bugs_list.rq_rs.rs_bugs_list import Status, BugsListResponse, Bug

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def fetch_bugs_list(engine: Engine) -> BugsListResponse:
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

    select_bug_query = select(
        bugs_table.c.bug_id,
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
    ).outerjoin(products_table, bugs_table.c.product_id == products_table.c.product_id
           ).outerjoin(environments_table, bugs_table.c.environment_id == environments_table.c.environment_id
                  ).outerjoin(scenarios_table, bugs_table.c.scenario_id == scenarios_table.c.scenario_id
                         ).outerjoin(testing_medium_table, bugs_table.c.testing_medium == testing_medium_table.c.medium_id
                                ).outerjoin(priority_table, bugs_table.c.priority_id == priority_table.c.priority_id
                                       ).outerjoin(user_details_table, bugs_table.c.reported_by == user_details_table.c.user_id
                                              ).outerjoin(user_details_table_copy, bugs_table.c.assignee_id == user_details_table_copy.c.user_id
                                                     ).outerjoin(root_cause_location_table, bugs_table.c.root_cause_location == root_cause_location_table.c.location_id
                                                            ).outerjoin(bugs_status_table, bugs_table.c.status == bugs_status_table.c.status_id)

    try:
        with engine.begin() as connection:
            result = pd.read_sql(select_bug_query, connection).to_dict('records')


        # Log the result for debugging
        logger.debug(f"Query Result: {result}")

        # If result is empty
        if not result:
            logger.warning("No bugs found.")
            status = Status(sts=False, err="404", msg="No bugs found")
            return BugsListResponse(status=status)

        lst = []
        for i in result:
            bug_detail = Bug(
                bug_id=i['bug_id'],
                product=i['product_name'],
                environment=i['environment_name'],
                scenario=i['scenario_name'],
                testing_medium=i['medium_name'],
                description=i['description'],
                user_data=i['user_data'],
                priority=i['priority_name'],
                reported_by=i['reported_user_name'],
                reported_at=i['reported_at'],
                assignee=i['assignee_user_name'],
                root_cause_location=i['location_name'],
                root_cause=i['root_cause'],
                resolution=i['resolution'],
                status=i['status_name'],
                created_at=i['created_at'],
                updated_at=i['updated_at']
            )
            lst.append(bug_detail)

        status = Status(sts=True, err=None, msg="Bugs fetched successfully")
        return BugsListResponse(status=status, bugs=lst)

    except SQLAlchemyError as e:
        logger.error(f"Error fetching bug entries: {e}")
        status = Status(sts=False, err=str(e), msg="Operation Failed")
        return BugsListResponse(status=status)
