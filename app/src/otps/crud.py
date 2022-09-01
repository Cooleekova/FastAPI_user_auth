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
            query = "INSERT INTO otps (recipient_id, session_id, otp_code, status, created_on) \
            VALUES (:recipient_id, :session_id, :otp_code, '1', now() AT TIME ZONE 'UTC')"
            return await session.execute(
                text(query), 
                {
                    'recipient_id': request.recipient_id, 
                    "session_id": session_id,
                    "otp_code": otp_code, 
                    }
                )