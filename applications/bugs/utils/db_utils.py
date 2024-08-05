import logging
from fastapi import HTTPException,status
from sqlalchemy import MetaData, Table, insert ,update ,select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.bugs.rq_rs.rq_bugs import AddBugRq , UpdateBugRq
from common.classes.generic import Status
from applications.bugs.rq_rs.rs_bugs import AddBugResponse,UpdateBugResponse, FindBugResponse
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
    

def find_bug(engine: Engine, bug_id: int) -> FindBugResponse:
    logger.info("Finding a bug entry with ID: %s", bug_id)
    bugs_table = Table(Tables.BUGS_TABLE, ConnectionDetails.metadata, autoload_with=engine)

    select_bug_query = select([
        bugs_table.c.id.label('bug_id'),
        bugs_table.c.reported_date,
        bugs_table.c.reporter,
        bugs_table.c.assignee,
        bugs_table.c.product_name,
        bugs_table.c.environment,
        bugs_table.c.testing_medium,
        bugs_table.c.scenario,
        bugs_table.c.description,
        bugs_table.c.user_data,
        bugs_table.c.priority,
        bugs_table.c.status,
        bugs_table.c.root_cause_location,
        bugs_table.c.root_cause,
        bugs_table.c.solution,
        bugs_table.c.comments
    ]).where(bugs_table.c.id == bug_id)

    try:
        with engine.begin() as connection:
            result = connection.execute(select_bug_query)
            bug = result.fetchone()

            if not bug:
                logger.warning("No bug entry found with the given ID: %s", bug_id)
                status = Status(sts=False, err="404", msg="Bug not found")
                raise HTTPException(status_code=404, detail=status.dict())

            logger.info("Bug entry found successfully with ID: %s", bug_id)
            status = Status(sts=True, err=None, msg="Bug found successfully")
            return FindBugResponse(
                status=status,
                bug_id=bug.bug_id,
                reported_date=bug.reported_date,
                reporter=bug.reporter,
                assignee=bug.assignee,
                product_name=bug.product_name,
                environment=bug.environment,
                testing_medium=bug.testing_medium,
                scenario=bug.scenario,
                description=bug.description,
                user_data=bug.user_data,
                priority=bug.priority,
                status=bug.status,
                root_cause_location=bug.root_cause_location,
                root_cause=bug.root_cause,
                solution=bug.solution,
                comments=bug.comments
            )
    except SQLAlchemyError as e:
        logger.error(f"Error finding bug entry: {e}")
        status = Status(sts=False, err=str(e), msg="Failed to find the bug")
        raise HTTPException(status_code=500, detail=status.model_dump())
    