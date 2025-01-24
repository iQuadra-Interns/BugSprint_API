from sqlalchemy import Table, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from config.database import DatabaseDetails, Views
from applications.common_constants.rq_rs.edit_profile_rs import EditProfileResponse
from common.classes.generic import Status
import logging

logger = logging.getLogger(__name__)

def edit_user_profile(engine: Engine, user_id: int, user_info) -> EditProfileResponse:
    resp = EditProfileResponse(status=Status())

    try:

        with engine.begin() as connection:
            logger.info(f"Fetching user_type and email for user_id: {user_id}")
            user_details_view = Table(
                "user_details", DatabaseDetails.METADATA, autoload_with=engine
            )


            user_query = select(
                user_details_view.c.user_type,
                user_details_view.c.email
            ).where(user_details_view.c.user_id == user_id)

            user_record = connection.execute(user_query).mappings().fetchone()

            if not user_record:
                logger.error(f"No user found for user_id: {user_id}")
                resp.status.error = "User not found."
                resp.status.status = False
                return resp


            user_type = user_record["user_type"]
            email = user_record["email"]
            logger.info(f"User type: {user_type}, Email: {email}")


            if user_type not in Views.USER_TYPE_TO_PERSONAL_DETAILS:
                logger.error(f"Invalid user type: {user_type}")
                resp.status.error = "Invalid user type."
                resp.status.status = False
                return resp


            role_table = Table(
                Views.USER_TYPE_TO_PERSONAL_DETAILS[user_type],
                DatabaseDetails.METADATA,
                autoload_with=engine,
            )


            logger.info(f"Updating profile in table: {role_table.name}")
            update_query = (
                update(role_table)
                .where(role_table.c.email == email)
                .values(
                    first_name=user_info.first_name,
                    middle_name=user_info.middle_name,
                    last_name=user_info.last_name,
                    mobile_number=user_info.mobile_number,
                )
            )
            update_result = connection.execute(update_query)

            if update_result.rowcount == 0:
                logger.error(f"No records updated for email: {email}")
                resp.status.error = "Update failed; no records updated."
                resp.status.status = False
                return resp


            logger.info(f"Fetching updated profile from table: {role_table.name}")
            fetch_query = select(
                role_table.c.first_name,
                role_table.c.middle_name,
                role_table.c.last_name,
                role_table.c.mobile_number,
            ).where(role_table.c.email == email)

            updated_user = connection.execute(fetch_query).mappings().fetchone()

            if not updated_user:
                logger.error("Failed to fetch updated user data.")
                resp.status.error = "Failed to fetch updated user data."
                resp.status.status = False
                return resp


        resp.status.status = True
        resp.status.error = ""
        resp.status.message = "Profile updated successfully."
        resp.first_name = updated_user["first_name"] or ""
        resp.middle_name = updated_user["middle_name"] or ""
        resp.last_name = updated_user["last_name"] or ""
        resp.mobile_number = updated_user["mobile_number"] or ""
        return resp

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error occurred: {e}")
        resp.status.error = "Database error occurred."
        resp.status.status = False
        return resp
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        resp.status.error = "Unexpected error occurred."
        resp.status.status = False
        return resp
