from sqlalchemy.engine import Connection
from sqlalchemy import text, inspect
from fastapi import HTTPException

def get_table_data(connection: Connection, table_name: str):
    try:
        # Get the columns of the table
        inspector = inspect(connection)
        columns = [col['name'] for col in inspector.get_columns(table_name)]

        # Execute the query
        query = text(f"SELECT * FROM {table_name}")
        result = connection.execute(query).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail=f"No data found for table {table_name}")

        # Convert result to list of dictionaries
        data = [dict(zip(columns, row)) for row in result]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
