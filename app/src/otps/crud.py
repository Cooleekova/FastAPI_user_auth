from init_database import async_session
from sqlalchemy import text
from otps import schema



async def find_block_otp(recipient_id: str):
    """ Function takes user's phone number as an argument 
    and makes a query to the database table otp_blocks to check if provided number is in blacklist. """
    async with async_session() as session:
        async with session.begin():
            query = "SELECT * FROM otp_blocks \
                WHERE recipient_id=:recipient_id AND created_on >= now() at time zone 'UTC' - interval '5 minutes'"
            result = await session.execute(text(query), {'recipient_id': recipient_id})
            return result.fetchone()


async def save_otp(
    request: schema.CreateOTP,
    session_id: str,
    otp_code: str
):
    """ Function saves otp_code into database
    making  insert query to database table "OTPs" """
    async with async_session() as session:
        async with session.begin():
            query = "INSERT INTO otps (recipient_id, session_id, otp_code, status, created_on, otp_failed_count) \
            VALUES (:recipient_id, :session_id, :otp_code, '1', now() AT TIME ZONE 'UTC', 1)"
            return await session.execute(
                text(query), 
                {
                    'recipient_id': request.recipient_id, 
                    "session_id": session_id,
                    "otp_code": otp_code, 
                    }
                )


async def find_otp_lifetime(
    request: schema.VerifyOTP
):
    """ Function takes otp code and session id as the arguments
    and makes a query to the database to check if provided otp code is not expired (code expires in 60 seconds). """
    async with async_session() as session:
        async with session.begin():
            query = "SELECT * FROM otps \
                WHERE recipient_id=:recipient_id \
                AND session_id=:session_id \
                AND created_on >= now() at time zone 'UTC' - interval '1 minutes'"
            result = await session.execute(text(query), {'recipient_id': request.recipient_id, "session_id": request.session_id})
            return result.fetchone()


async def update_otp_failed_count(request: schema.OTPList):
    """ Function for incrementing failed otp code counter, 
    it changes otp_failed_count field in the database table OTPs
    when the user provides incorrect otp_code """
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE otps SET otp_failed_count=otp_failed_count+1 \
                WHERE recipient_id=:recipient_id \
                AND session_id=:session_id \
                AND otp_code=:otp_code"
            return await session.execute(
                text(query), 
                {
                    'recipient_id': request.recipient_id, 
                    "session_id": request.session_id,
                    "otp_code": request.otp_code, 
                    }
                )
    

async def block_otp_code(request: schema.OTPList):
     """ Function saves recipient contact to the database table OTP_blocks """
     async with async_session() as session:
        async with session.begin():
            query = "INSERT INTO otp_blocks (recipient_id, created_on) \
            VALUES (:recipient_id, now() AT TIME ZONE 'UTC')"
            return await session.execute(
                text(query), {'recipient_id': request.recipient_id,})


async def disable_otp_code(request: schema.OTPList):
    """Function changes OTP code 'status' field after the code was successfully verified
    so that it can not be used again"""
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE otps SET status='9' \
            WHERE recipient_id=:recipient_id \
            AND status='1' AND session_id=:session_id \
            AND otp_code=:otp_code"
            return await session.execute(
                text(query), 
                {'recipient_id': request.recipient_id, "session_id": request.session_id, "otp_code": request.otp_code}
                )