import logging
from common.classes.generic import Status
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import logging
from sqlalchemy import MetaData, Table, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.test_cases.rq_rs.rs_test_cases import TestCasesResponse, Status
from applications.test_cases.rq_rs.rq_test_cases import TestCasesRequest
from config.database import Tables, DatabaseDetails

logger = logging.getLogger(__name__)

def add_test_case_details(engine: Engine, test_case_info: TestCasesRequest) -> TestCasesResponse:
    logger.info("Adding test case details")

    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    test_cases_table = Table(Tables.TEST_CASES, metadata, autoload_with=engine)
    products_table = Table(Tables.PRODUCTS, metadata, autoload_with=engine)

    try:
        with engine.begin() as connection:
            product_query = select(
                products_table.c.product_short_name,
                products_table.c.test_cases_count
            ).where(products_table.c.product_id == test_case_info.product_id)

            product_data = connection.execute(product_query).fetchone()

            if not product_data:
                logger.error(f"Product with product_id {test_case_info.product_id} not found.")
                return TestCasesResponse(status=Status(sts=False, err="Product not found", msg="Operation Failed"))

            product_short_name = product_data["product_short_name"]
            current_test_cases_count = product_data["test_cases_count"] or 0

            new_test_cases_count = current_test_cases_count + 1
            testcase_id = f"TC-{product_short_name}-{new_test_cases_count}"

            insert_query = test_cases_table.insert().values(
                testcase_id=testcase_id,
                product_id=test_case_info.product_id,
                test_scenario=test_case_info.test_scenario,
                test_steps=test_case_info.test_steps,
                actual_result=test_case_info.actual_result,
                comment=test_case_info.comment,
                developer_comment=test_case_info.developer_comment
            )
            connection.execute(insert_query)

            update_query = update(products_table).where(
                products_table.c.product_id == test_case_info.product_id
            ).values(test_cases_count=new_test_cases_count)
            connection.execute(update_query)

            logger.info(f"Test case added successfully with testcase_id {testcase_id}")
            return TestCasesResponse(status=Status(sts=True, err=None, msg="Test case added successfully"))

    except SQLAlchemyError as e:
        logger.error(f"Error adding test case: {e}")
        return TestCasesResponse(status=Status(sts=False, err=str(e), msg="Operation Failed"))
