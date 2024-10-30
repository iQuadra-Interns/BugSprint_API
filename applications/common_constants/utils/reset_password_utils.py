import logging
from sqlalchemy import MetaData, Table, select, and_
from sqlalchemy.engine import Engine
from common.classes.generic import Status
from applications.common_constants.rq_rs.reset_password_rq import ResetPasswordRq
from applications.common_constants.rq_rs.reset_password_rs import ResetPasswordRs
from config.database import DatabaseDetails, Views
import bcrypt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def reset_password(eng: Engine, reset_pswd: ResetPasswordRq) -> ResetPasswordRs:
    resp = ResetPasswordRs(
        status=Status(),
        userid=reset_pswd.userid
    )

    user_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    user_table = Table(Views.USER_TYPE_TO_PERSONAL_DETAILS[reset_pswd.userid.user_category], user_metadata,
                       autoload_with=eng)

    select_old_password_query = select(user_table.c.password).where(
        and_(
            user_table.c.id == reset_pswd.userid.user_cat_id,
            user_table.c.email == reset_pswd.email
        )
    )

    with eng.begin() as connection:
        old_password_result = connection.execute(select_old_password_query).fetchone()

    if not old_password_result:
        logger.error("User not found.")
        resp.status.error = "User not found."
        resp.status.status = False
        return resp

    hashed_old_password = old_password_result[0].encode('utf-8')

    if not bcrypt.checkpw(reset_pswd.old_password.encode('utf-8'), hashed_old_password):
        logger.error("Old password does not match.")
        resp.status.error = "Old password is incorrect."
        resp.status.status = False
        return resp

    if bcrypt.checkpw(reset_pswd.new_password.encode('utf-8'), hashed_old_password):
        logger.error("New password cannot be the same as the old password.")
        resp.status.error = "New password cannot be the same as the old password."
        resp.status.status = False
        return resp

    hashed_new_password = bcrypt.hashpw(reset_pswd.new_password.encode('utf-8'), bcrypt.gensalt())
    update_password_query = user_table.update().values(
        password=hashed_new_password.decode('utf-8')
    ).where(and_(
        user_table.c.id == reset_pswd.userid.user_cat_id,
        user_table.c.email == reset_pswd.email
    ))

    with eng.begin() as connection:
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
