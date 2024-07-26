import sys
import os

sys.path.append('/home/sanju/Documents/Intern_work/BugSprint_API')

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection, Engine
from fastapi import HTTPException
from typing import Generator, Dict, List, Any, Union
from applications.common_constants.rq_rs.rs_all import Status

def get_db_connection(engine: Engine) -> Generator[Connection, None, None]:
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

def get_all_table_data(connection: Connection) -> Dict[str, Union[Dict[str, List[Dict[str, Any]]], Status]]:
    try:
        inspector = inspect(connection)
        table_names = inspector.get_table_names()

        if not table_names:
            raise HTTPException(status_code=404, detail="No tables found in the database")

        data = {}
        for table_name in table_names:
            try:
                # Get the columns of the table
                columns = [col['name'] for col in inspector.get_columns(table_name)]

                # Execute the query to fetch all data
                table_query = text(f"SELECT * FROM {table_name}")
                result = connection.execute(table_query).fetchall()

                # Convert result to list of dictionaries
                table_data = [dict(zip(columns, row)) for row in result]
                data[table_name] = table_data
            except Exception as e:
                data[table_name] = f"Error fetching data: {e}"

        return {"status": Status(sts=True, msg="Fetched successfully"), "data": data}
    except Exception as e:
        return {"status": Status(sts=False, err=f"Error fetching data: {e}"), "data": {}}
