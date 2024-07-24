import logging
from sqlalchemy import MetaData, Table, insert ,update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs.rq_rs.rq_bugs import AddBugRq , UpdateBugRq
from config.database import Tables, ConnectionDetails

logger = logging.getLogger(__name__)


def add_bug(engine: Engine, bug_info: AddBugRq) -> int:
    logger.info("Creating a new bug entry")
    metadata = MetaData(schema=ConnectionDetails.db_default_schema_name)
    bugs_table = Table(Tables.BUGS_TABLE, metadata, autoload_with=engine)

    insert_into_bugs_query = bugs_table.insert().values(
        reported_date=bug_info.reported_date,
        reporter=bug_info.reporter,
        assignee=bug_info.assignee,
        product_name=bug_info.product_name,
        environment=bug_info.environment,
        testing_medium=bug_info.testing_medium,
        scenario=bug_info.scenario,
        description=bug_info.description,
        user_data=bug_info.user_data,
        priority=bug_info.priority,
        status=bug_info.status,
        root_cause_location=bug_info.root_cause_location,
        root_cause=bug_info.root_cause,
        solution=bug_info.solution,
        comments=bug_info.comments
    )

    try:
        with engine.begin() as connection:
            res = connection.execute(insert_into_bugs_query)
            bug_id = res.inserted_primary_key[0]
            logger.info("Bug entry created successfully")
            return bug_id
    except SQLAlchemyError as e:
        logger.error(f"Error creating bug entry: {e}")
        return None


def update_bug(engine: Engine, bug_id: int, bug_info: UpdateBugRq) :
    logger.info("Updating an existing bug entry")
    metadata = MetaData(schema=ConnectionDetails.db_default_schema_name)
    bugs_table = Table(Tables.BUGS_TABLE, metadata, autoload_with=engine)

    update_bug_query = update(bugs_table).where(bugs_table.c.id == bug_id).values(
        reported_date=bug_info.reported_date,
        reporter=bug_info.reporter,
        assignee=bug_info.assignee,
        product_name=bug_info.product_name,
        environment=bug_info.environment,
        testing_medium=bug_info.testing_medium,
        scenario=bug_info.scenario,
        description=bug_info.description,
        user_data=bug_info.user_data,
        priority=bug_info.priority,
        status=bug_info.status,
        root_cause_location=bug_info.root_cause_location,
        root_cause=bug_info.root_cause,
        solution=bug_info.solution,
        comments=bug_info.comments
    )

    try:
        with engine.begin() as connection:
            result = connection.execute(update_bug_query)
            if result.rowcount == 0:
                logger.warning("No bug entry found with the given ID")
                return False
            logger.info("Bug entry updated successfully")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Error updating bug entry: {e}")
        return False