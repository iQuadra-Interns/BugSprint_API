from sqlalchemy.engine import Connection
from sqlalchemy import inspect, text
from fastapi import HTTPException

def get_all_table_data(connection: Connection):
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

        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
