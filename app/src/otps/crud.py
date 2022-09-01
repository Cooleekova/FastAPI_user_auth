from init_database import async_session
from sqlalchemy import text
from otps import schema



async def find_block_otp(recipient_id: str):
    """ Function takes user's JWT token as an argument 
    and makes a query to the database table blacklist to check if provided token is in blacklist. """
    async with async_session() as session:
        async with session.begin():
            query = "SELECT * FROM otp_blocks WHERE recipient_id=:recipient_id AND created_on >= now() at time zone 'UTC' - interval '5 minutes'"
            result = await session.execute(text(query), {'recipient_id': recipient_id})
            return result.fetchone()
