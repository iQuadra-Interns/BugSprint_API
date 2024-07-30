import logging
from fastapi import HTTPException,status
from sqlalchemy import MetaData, Table, insert ,update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs.rq_rs.rq_bugs import AddBugRq , UpdateBugRq
from common.classes.generic import Status
from applications.bugs.rq_rs.rs_bugs import AddBugResponse,UpdateBugResponse
from config.database import Tables, ConnectionDetails

logger = logging.getLogger(__name__)


def add_bug(engine: Engine, bug_info: AddBugRq):
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
            if bug_id is None:
                status = Status(sts=False,err="500",msg="Operation Failed")
                return AddBugResponse(status=status, bug_id=0)

            status = Status(sts=True, err="null", msg="Bug created successfully")
            return AddBugResponse(status=status, bug_id=bug_id )
    except SQLAlchemyError as e:
        logger.error(f"Error creating bug entry: {e}")
        status = Status(sts=False, err="500", msg="Operation Failed")
        return AddBugResponse(status=status, bug_id=0)


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
                status = Status(sts=False, err="404", msg="enter proper bug_id")
                raise HTTPException(status_code=404, detail=status.dict())

            logger.info("Bug entry updated successfully")
            status = Status(sts=True, err=None, msg=f"Bug updated successfully with id : {bug_id}")
            return UpdateBugResponse(status=status)
    except SQLAlchemyError as e:
        logger.error(f"Error updating bug entry: {e}")
        status = Status(sts=False, err=str(e), msg="enter proper bug_info")
        raise HTTPException(status_code=500, detail=status.dict())