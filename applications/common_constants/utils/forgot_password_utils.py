import logging
import pandas
import sqlalchemy
from pydantic import EmailStr
from sqlalchemy import MetaData, Table, select, and_, create_engine
from sqlalchemy.engine import Engine
from common.classes.generic import Status, UserId
from common.utilities.miscellaneous import generateOTP
from applications.common_constants.rq_rs.forgot_password_rq import ForgotPasswordRq, ForgotPasswordGenerateOTPRq, \
    ForgotPasswordVerifyEmailRq
from applications.common_constants.rq_rs.forgot_password_rs import ForgotPasswordRs, UserLoginRs, UserLogin
from config.database import DatabaseDetails, Tables, Views

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_login(eng: Engine, login: EmailStr) -> UserLoginRs:
    resp = UserLoginRs(
        sts=Status(),
        det=UserLogin(
            userid=UserId()
        )
    )
    users_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    users_table = Table(Views.USER_DETAILS, users_metadata, autoload_with=eng)
    users_query = select(
        users_table.c.user_id,
        users_table.c.email,
        users_table.c.user_category_id
    ).where(
        users_table.c.email == login
    )
    with eng.begin() as connection:
        result = pandas.read_sql(users_query, connection).to_dict('records')

    if not result or len(result) <= 0:
        resp.sts.error = f"{login} does not available"
        resp.sts.message = ""
        resp.sts.status = False
        return resp
    resp.det.userid = UserId.model_validate(result[0])
    resp.det.email = result[0]['email']
    resp.sts.error = ""
    resp.sts.message = f"{login} is available"
    resp.sts.status = True
    return resp


def fetch_forgot_staging_record(eng: Engine, forgot_pswd: ForgotPasswordGenerateOTPRq) -> int:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING, echo=False)
    metadata = MetaData(DatabaseDetails.DEFAULT_SCHEMA)
    forgot_pswd_staging_table = Table(Tables.FORGOT_PASSWORD_OTP_STAGING_TABLE, metadata, autoload_with=engine)
    max_id_stmt = select(
        sqlalchemy.func.count(forgot_pswd_staging_table.c.id).label('count')
    ).where(and_(forgot_pswd_staging_table.c.user_category_id == forgot_pswd.userid.user_cat_id,
                 forgot_pswd_staging_table.c.user_id == forgot_pswd.userid.user_id,
                 forgot_pswd_staging_table.c.email == forgot_pswd.email))
    with eng.begin() as connection:
        count = pandas.read_sql(max_id_stmt, connection).to_dict('records')
    if not count or len(count) <= 0 or not count[0]['count'] or int(count[0]['count']) <= 0:
        return 0
    return int(count[0]['count'])


def update_user_info_in_staging_tbl(eng: Engine, forgot_pswd: ForgotPasswordGenerateOTPRq):
    resp = ForgotPasswordRs(
        status=Status(),
        userid=forgot_pswd.userid
    )
    email_otp = generateOTP()
    user_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    forgot_pswd_staging_table = Table(Tables.FORGOT_PASSWORD_OTP_STAGING_TABLE, user_metadata, autoload_with=eng)
    count = fetch_forgot_staging_record(eng, forgot_pswd)
    if count == 0:
        forgot_staging_query = forgot_pswd_staging_table.insert().values(
            category=forgot_pswd.userid.user_category,
            user_id=forgot_pswd.userid.user_id,
            user_category_id=forgot_pswd.userid.user_cat_id,
            email=forgot_pswd.email,
            email_otp=email_otp
        )
    else:
        forgot_staging_query = forgot_pswd_staging_table.update().values(
            category=forgot_pswd.userid.user_category,
            user_id=forgot_pswd.userid.user_id,
            user_category_id=forgot_pswd.userid.user_cat_id,
            email=forgot_pswd.email,
            email_otp=email_otp
        ).where(and_(forgot_pswd_staging_table.c.user_category_id == forgot_pswd.userid.user_cat_id,
                     forgot_pswd_staging_table.c.user_id == forgot_pswd.userid.user_id,
                     forgot_pswd_staging_table.c.email == forgot_pswd.email))

    with eng.begin() as connection:
        result = connection.execute(forgot_staging_query)
        resp.status = True
        resp.userid = forgot_pswd.userid
    if result.rowcount != 1:
        logger.error('Failed to insert user information into forgot password staging table')
        logger.error("The details are as follows:")
        logger.info(str(forgot_staging_query))
        resp.status.error = f"Failed to generate OTP"
        resp.status.message = ""
        resp.status.status = False
    return resp


def verify_forgot_password_email_otp(eng: Engine, forgot_pswd: ForgotPasswordVerifyEmailRq):
    resp = ForgotPasswordRs(
        sts=Status(),
        userid=forgot_pswd.userid
    )
    user_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    forgot_pswd_staging_table = Table(Tables.FORGOT_PASSWORD_OTP_STAGING_TABLE, user_metadata, autoload_with=eng)
    select_query = select(
        forgot_pswd_staging_table.c.user_category_id,
        forgot_pswd_staging_table.c.category,
        forgot_pswd_staging_table.c.email,
        forgot_pswd_staging_table.c.email_otp
    ).where(
        and_(
            forgot_pswd_staging_table.c.user_category_id == forgot_pswd.userid.user_cat_id,
            forgot_pswd_staging_table.c.category == forgot_pswd.userid.user_category,
            forgot_pswd_staging_table.c.email == forgot_pswd.email,
            forgot_pswd_staging_table.c.email_otp == forgot_pswd.email_otp,
        ))
    with eng.begin() as connection:
        result = pandas.read_sql(select_query, connection).to_dict('records')
    if not result or len(result) != 1:
        logger.error('Failed to fetch user information from forgot password staging table')
        logger.error("The details are as follows:")
        logger.info(str(select_query))
        resp.status.error = "Might be OTP mismatch"
        resp.status.message = ""
        resp.status.status = False
        return resp
    resp.status.status = True
    resp.status.error = ""
    resp.status.message = "Successfully verified OTP"
    return resp


def forgot_password_information(eng: Engine, forgot_pswd: ForgotPasswordRq) -> ForgotPasswordRs:
    resp = ForgotPasswordRs(
        status=Status(),
        user=forgot_pswd.userid
    )
    user_metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    forgot_pswd_staging_table = Table(Tables.FORGOT_PASSWORD_OTP_STAGING_TABLE, user_metadata, autoload_with=eng)
    role_table = Table(Views.USER_TYPE_TO_PERSONAL_DETAILS[forgot_pswd.userid.user_category], user_metadata, autoload_with=eng)
    select_user_query = select(
        role_table.c.password
    ).where(and_(role_table.c.id == forgot_pswd.userid.user_cat_id,
                 role_table.c.email == forgot_pswd.email))
    with eng.begin() as connection:
        select_user_result = connection.execute(select_user_query).fetchone()[0]
    if len(select_user_result) <= 0:
        logger.error("failed to fetch previous password from user login table")
        resp.sts.err = ""
        resp.sts.war = "Failed to fetch previous password.user login table error."
        resp.sts.msg = ""
        resp.sts.sts = False
        return resp

    select_role_query = select(
        role_table.c.previous_passwords
    ).where(and_(role_table.c.id == forgot_pswd.userid.user_cat_id,
                 role_table.c.email == forgot_pswd.email))
    with eng.begin() as connection:
        select_role_result = connection.execute(select_role_query).fetchone()[0]
    if not select_role_result or len(select_role_result) <= 0:
        pass
    else:
        previous_pswds = select_role_result.split('~~~')
        if forgot_pswd.new_pswd in previous_pswds:
            resp.sts.err = ""
            resp.sts.war = "Existing Password"
            resp.sts.msg = ""
            resp.sts.sts = False
            return resp

    updated_user_query = role_table.update().values(
        password=forgot_pswd.new_password
    ).where(and_(
        # role_table.c.user_category_id == forgot_pswd.userid.user_cat_id,
        role_table.c.email == forgot_pswd.email
    ))
    with eng.begin() as connection:
        reset_result = connection.execute(updated_user_query)
    if reset_result.rowcount != 1:
        logger.error("failed to update new password details in user login table")
        resp.status.warning = 'failed to update forgot password'
        resp.status.status = False
        resp.status.error = ""
        resp.status.message = ""
        return resp

    select_role_query = select(
        role_table.c.previous_passwords
    ).where(and_(role_table.c.id == forgot_pswd.userid.user_cat_id,
                 role_table.c.email == forgot_pswd.email))
    with eng.begin() as connection:
        select_role_result = connection.execute(select_role_query).fetchone()[0]
    if not select_role_result or len(select_role_result) <= 0:
        update_role_query = role_table.update().values(
            prev_passwords=select_user_result
        ).where(and_(
            role_table.c.id == forgot_pswd.userid.user_cat_id,
            role_table.c.email == forgot_pswd.email
        ))
    else:
        update_role_query = role_table.update().values(
            prev_passwords=f"{select_role_result}~~~{select_user_result}"
        ).where(and_(
            role_table.c.id == forgot_pswd.userid.user_cat_id,
            role_table.c.email == forgot_pswd.email
        ))

        with eng.begin() as connection:
            update_role_result = connection.execute(update_role_query)
        if update_role_result.rowcount != 1:
            logger.error("failed to update previous passwords details in personal details  table")
            resp.status.warning = 'failed to update previous passwords into developer personal details table'
            resp.status.status = False
            resp.status.error = ""
            resp.status.message = ""
            return resp

    forgot_pswd_staging_query = forgot_pswd_staging_table.delete().where(
        and_(
            # forgot_pswd_staging_table.c.usr_category_id == forgot_pswd.userid.user_cat_id,
            forgot_pswd_staging_table.c.email == forgot_pswd.email,
        ))
    with eng.begin() as connection:
        staging_result = connection.execute(forgot_pswd_staging_query)
    if staging_result.rowcount != 1:
        logger.error('Failed to delete forgot password information from staging table')
        logger.error("The details are as follows:")
        logger.info(str(forgot_pswd_staging_query))
        resp.status.error = ""
        resp.status.warning = "Failed to finish forgot password. staging table delete error."
        resp.status.message = ""
        return resp

    resp.status.status = True
    resp.status.error = ""
    resp.status.message = "successfully updated forgot password"
    return resp