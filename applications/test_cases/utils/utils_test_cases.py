import logging
from sqlalchemy import MetaData, Table, select, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from applications.test_cases.rq_rs.rq_test_cases import TestCasesRequest
from applications.test_cases.rq_rs.rs_test_cases import UpdateTestCaseResponse,DeleteTestCaseResponse,GetTestCasesResponse, TestCase,TestCasesResponse
from config.database import Tables, DatabaseDetails
from common.classes.generic import Status

logger = logging.getLogger(__name__)


def add_test_case_details(engine: Engine, test_case_info: TestCasesRequest) -> TestCasesResponse:
    logger.info("Creating a new test case entry")
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)

    test_cases_table = Table(Tables.TESTCASES, metadata, autoload_with=engine)
    products_table = Table(Tables.PRODUCTS, metadata, autoload_with=engine)

    product_id = test_case_info.product_id

    try:
        with engine.begin() as connection:
            select_product_query = select(
                products_table.c.test_case_count,
                products_table.c.product_short_code
            ).where(products_table.c.product_id == product_id)

            product_data = connection.execute(select_product_query).fetchone()

            if not product_data:
                logger.warning(f"No product found with product_id {product_id}. Cannot create test case.")
                return TestCasesResponse(
                    status=Status(status=False, error="Product Not Found", message="Invalid product_id"),
                    test_case_id=-1
                )

            test_case_count =  product_data[0] if product_data[0] is not None else 0
            product_short_code = product_data[1]
            testcase_code = f"TC-{product_short_code}-{test_case_count + 1}"

            insert_query = test_cases_table.insert().values(
                testcase_code=testcase_code,
                product_id=product_id,
                test_scenario=test_case_info.test_scenario,
                test_steps=test_case_info.test_steps,
                actual_result=test_case_info.actual_result,
                expected_result=test_case_info.expected_result,
                comment=test_case_info.comment,
                developer_comment=test_case_info.developer_comment
            )
            result = connection.execute(insert_query)
            new_test_case_id = result.inserted_primary_key[0]

            update_query = products_table.update().where(
                products_table.c.product_id == product_id
            ).values(test_case_count=test_case_count + 1)

            connection.execute(update_query)

            return TestCasesResponse(
                status=Status(status=True, error=None, message="Test case added successfully"),
                test_case_id=new_test_case_id
            )

    except SQLAlchemyError as e:
        logger.error(f"Database error while adding test case: {e}")
        return TestCasesResponse(
            status=Status(status=False, error="500", message="Failed to add test case"),
            test_case_id=-1
        )




def update_test_case_details(engine, testcase_id, test_case_info):
    logger.info(f"Updating test case ID {testcase_id}")

    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    test_cases_table = Table(Tables.TESTCASES, metadata, autoload_with=engine)

    update_query = (
        test_cases_table.update()
        .where(test_cases_table.c.testcase_id == testcase_id)
        .values(
            test_scenario=test_case_info.test_scenario,
            test_steps=test_case_info.test_steps,
            actual_result=test_case_info.actual_result,
            expected_result=test_case_info.expected_result,
            comment=test_case_info.comment,
            developer_comment=test_case_info.developer_comment
        )
    )

    try:
        with engine.begin() as connection:
            connection.execute(update_query)

        logger.info(f"Test case ID {testcase_id} updated successfully")

        return UpdateTestCaseResponse(
            status=Status(status=True, error=None, message="Test case updated successfully")
        )

    except SQLAlchemyError as e:
        logger.error(f"Error updating test case: {e}")
        return UpdateTestCaseResponse(
            status=Status(status=False, error="500", message="Failed to update test case")
        )




def delete_test_case(engine, testcase_id: int) -> DeleteTestCaseResponse:
    logger.info(f"Deleting test case with ID {testcase_id}")

    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    test_cases_table = Table(Tables.TESTCASES, metadata, autoload_with=engine)

    delete_query = delete(test_cases_table).where(test_cases_table.c.testcase_id == testcase_id)
    try:
        with engine.begin() as connection:
            result = connection.execute(delete_query)
            if result.rowcount == 0:
                logger.warning(f"No test case found with ID {testcase_id}")
                return DeleteTestCaseResponse(
                    status=Status(status=False, error="404", message="Test case not found")
                )

        logger.info(f"Test case ID {testcase_id} deleted successfully")
        return DeleteTestCaseResponse(
            status=Status(status=True, error=None, message="Test case deleted successfully")
        )

    except SQLAlchemyError as e:
        logger.error(f"Error deleting test case: {e}")
        return DeleteTestCaseResponse(
            status=Status(status=False, error="500", message="Failed to delete test case")
        )





def get_test_cases(engine: Engine) -> GetTestCasesResponse:

    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    test_cases_table = Table(Tables.TESTCASES, metadata, autoload_with=engine)
    select_query = select(
        test_cases_table.c.product_id,
        test_cases_table.c.testcase_id,
        test_cases_table.c.testcase_code,
        test_cases_table.c.test_scenario,
        test_cases_table.c.test_steps,
        test_cases_table.c.actual_result,
        test_cases_table.c.expected_result,
        test_cases_table.c.comment,
        test_cases_table.c.developer_comment,
    )

    try:
        with engine.begin() as connection:
            result = connection.execute(select_query).fetchall()

        if not result:
            logger.warning("No test cases found.")
            return GetTestCasesResponse(
                status=Status(sts=False, err="404", msg="No test cases found"),
                test_cases=[]
            )

        test_cases_list = [
            TestCase(
                testcase_id=row.testcase_id,
                product_id=row.product_id,
                testcase_code=row.testcase_code,
                test_scenario=row.test_scenario,
                test_steps=row.test_steps,
                actual_result=row.actual_result,
                expected_result=row.expected_result,
                comment=row.comment,
                developer_comment=row.developer_comment
            )
            for row in result
        ]

        return GetTestCasesResponse(
            status=Status(sts=True, err=None, msg="Test cases fetched successfully"),
            test_cases=test_cases_list
        )

    except SQLAlchemyError as e:
        logger.error(f"Error fetching test cases: {e}")
        return GetTestCasesResponse(
            status=Status(sts=False, err="500", msg="Failed to fetch test cases"),
            test_cases=[]
        )