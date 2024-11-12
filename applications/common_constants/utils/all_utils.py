import logging
from sqlalchemy import Table, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from config.database import DatabaseDetails, Tables
from common.classes.generic import Status
from typing import Optional
from applications.common_constants.rq_rs.rs_all import GetTableDataResponse

logger = logging.getLogger(__name__)

def get_table_data(engine: Engine, table_name: Optional[str] = None):
    logger.info("Fetching table data for table: %s", table_name if table_name else "all tables from common_constants")

    # Define the common_constants table to retrieve the list of table names
    common_constants_table = Table(Tables.CONSTANTS_TABLE_NAMES, DatabaseDetails.METADATA, autoload_with=engine)

    try:
        with engine.begin() as connection:
            # Query all table names in the common_constants table, using mappings() to get rows as dictionaries
            all_tables_query = select(common_constants_table.c.table_name)
            table_names = connection.execute(all_tables_query).mappings().fetchall()

            # Extract table names and normalize case for consistency
            all_table_names = [row['table_name'].strip().lower() for row in table_names]

            logger.debug("Retrieved table names from common_constants: %s", all_table_names)

            # If no table_name is specified, fetch data from all tables listed in common_constants
            if table_name is None:
                if not all_table_names:
                    logger.warning("No tables found in common_constants")
                    return GetTableDataResponse(
                        status=Status(status=False, error="404", message="No tables found in common_constants")
                    )

                data = {}
                # Fetch data from each table listed in common_constants
                for tbl_name_value in all_table_names:
                    logger.debug("Attempting to access table: %s", tbl_name_value)

                    # Use getattr to dynamically access the corresponding table attribute from the Tables class
                    tbl_name = getattr(Tables, tbl_name_value.upper(), None)
                    if not tbl_name:
                        logger.error(f"Table name '{tbl_name_value}' not found in Tables class.")
                        continue

                    dynamic_table = Table(tbl_name, DatabaseDetails.METADATA, autoload_with=engine)
                    fetch_data_query = select(dynamic_table)
                    rows = connection.execute(fetch_data_query).mappings().fetchall()

                    # Add data from each table to the response dictionary
                    data[tbl_name_value] = [dict(row) for row in rows] if rows else []

                return GetTableDataResponse(
                    status=Status(status=True, error="no error", message="Operation successful"),
                    data=data  # Dictionary of table names and their respective data
                )

            # Normalize the specific table name input for consistent matching
            table_name_normalized = table_name.strip().lower()
            logger.debug("Normalized user input table name: %s", table_name_normalized)

            # Check if the specific table_name exists in the retrieved common_constants
            if table_name_normalized not in all_table_names:
                logger.warning(f"Table '{table_name}' not found in common_constants")
                return GetTableDataResponse(
                    status=Status(status=False, error="404",
                                  message=f"Table '{table_name}' not found in common_constants")
                )

            # Use getattr to dynamically access the corresponding table attribute from Tables class
            dynamic_table_name = getattr(Tables, table_name_normalized.upper(), None)
            if not dynamic_table_name:
                logger.error(f"Table '{table_name}' not found in Tables class.")
                return GetTableDataResponse(
                    status=Status(status=False, error="404", message=f"Table '{table_name}' not found in Tables class")
                )

            # Fetch data from the specified table
            dynamic_table = Table(dynamic_table_name, DatabaseDetails.METADATA, autoload_with=engine)
            fetch_data_query = select(dynamic_table)
            rows = connection.execute(fetch_data_query).mappings().fetchall()

            if not rows:
                logger.warning(f"No data found in table '{table_name}'")
                return GetTableDataResponse(
                    status=Status(status=False, error="404", message=f"No data found in table '{table_name}'")
                )

            data = [dict(row) for row in rows]

            logger.info("Data fetched successfully from table: %s", table_name)

            return GetTableDataResponse(
                status=Status(status=True, error="no error", message="Operation successful"),
                data=data  # List of rows from the specified table
            )

    except SQLAlchemyError as e:
        logger.error("Error fetching data for table '%s': %s", table_name if table_name else "all tables", e)
        return GetTableDataResponse(
            status=Status(status=False, error="500", message="Database error occurred")
        )
