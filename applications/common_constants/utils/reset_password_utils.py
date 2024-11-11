import logging
from sqlalchemy import MetaData, Table, select, and_, update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from common.classes.generic import Status
from applications.common_constants.rq_rs.reset_password_rq import ResetPasswordRq
from applications.common_constants.rq_rs.reset_password_rs import ResetPasswordRs
from config.database import Views, DatabaseDetails
import bcrypt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def reset_password(engine: Engine, reset_pswd: ResetPasswordRq) -> ResetPasswordRs:
    resp = ResetPasswordRs(status=Status(), userid=reset_pswd.userid)

    try:
        user_category = reset_pswd.userid.user_category
        user_cat_id = reset_pswd.userid.user_cat_id
        email = reset_pswd.email
        old_password = reset_pswd.old_password
        new_password = reset_pswd.new_password

        user_table_name = Views.USER_TYPE_TO_PERSONAL_DETAILS.get(user_category)
        if not user_table_name:
            logger.error(f"Invalid user category: {user_category}")
            resp.status.error = "Invalid user category."
            resp.status.status = False
            return resp


        users_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
        users_table = Table(user_table_name, users_metadata, autoload_with=engine)

        select_old_password_query = select(
            users_table.c.hashed_password,
            users_table.c.previous_passwords
        ).where(and_(
            users_table.c.id == user_cat_id,
            users_table.c.email == email
        ))

        with engine.begin() as connection:
            old_password_result = connection.execute(select_old_password_query).fetchone()

        if not old_password_result:
            logger.error(f"User not found for email: {email} and user_cat_id: {user_cat_id}")
            resp.status.error = "User not found."
            resp.status.status = False
            return resp

        stored_old_password_hash = old_password_result[0].encode('utf-8')
        previous_passwords = old_password_result[1] or []

        if not bcrypt.checkpw(old_password.encode('utf-8'), stored_old_password_hash):
            logger.error("Old password is incorrect.")
            resp.status.error = "Old password is incorrect."
            resp.status.status = False
            return resp

        if bcrypt.checkpw(new_password.encode('utf-8'), stored_old_password_hash):
            logger.error("New password cannot be the same as the old password.")
            resp.status.error = "New password cannot be the same as the old password."
            resp.status.status = False
            return resp

        for old_pw in previous_passwords:
            if bcrypt.checkpw(new_password.encode('utf-8'), old_pw.encode('utf-8')):
                logger.error("New password matches a previous password.")
                resp.status.error = "New password cannot be one of the last three passwords."
                resp.status.status = False
                return resp

        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), stored_old_password_hash)

        if len(previous_passwords) >= 3:
            previous_passwords = previous_passwords[1:]
        previous_passwords.append(new_password_hash.decode('utf-8'))

        update_password_query = update(users_table).values(
            hashed_password=new_password_hash.decode('utf-8'),
            previous_passwords=previous_passwords
        ).where(and_(
            users_table.c.id == user_cat_id,
            users_table.c.email == email
        ))

        with engine.begin() as connection:
            update_result = connection.execute(update_password_query)

        if update_result.rowcount != 1:
            logger.error("Failed to update the password.")
            resp.status.error = "Failed to update the password."
            resp.status.status = False
            return resp

        resp.status.status = True
        resp.status.error = ""
        resp.status.message = "Password successfully updated."
        return resp

    except SQLAlchemyError as e:
        logger.error(f"Database error in reset_password function: {str(e)}")
        resp.status.error = "Database error."
        resp.status.status = False
        return resp
    except Exception as e:
        logger.error(f"Unexpected error in reset_password function: {str(e)}")
        resp.status.error = "Internal server error."
        resp.status.status = False
        return resp
