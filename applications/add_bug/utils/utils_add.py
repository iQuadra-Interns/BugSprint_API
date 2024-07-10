from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from applications.add_bug.utils.db import bugs_common_constants, engine
from applications.add_bug.rq_rs.rq_add import AddBugRequest

def add_bug(bug: AddBugRequest):
    query = insert(bugs_common_constants).values(
        bug_id=bug.bug_id,
        bug=bug.bug,
        scenario=bug.scenario,
        status=bug.status,
        assignee=bug.assignee,
        environment=bug.environment,
        testing_medium=bug.testing_medium,
        root_cause_location=bug.root_cause_location,
        priority=bug.priority,
        description=bug.description,
        user_data=bug.user_data
    )
    try:
        with engine.connect() as connection:
            connection.execute(query)
            connection.commit()
        return {"message": "Bug added successfully"}
    except SQLAlchemyError as e:
        print(f"Error adding bug: {e}")
        return {"message": "Error adding bug"}
