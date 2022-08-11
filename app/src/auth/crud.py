from init_database import async_session
from sqlalchemy import text
from auth import schema

async def find_exist_user(email: str):
    """ Function takes email as an argument 
    and makes a query to database looking for a user registered with such an email.
    Returns user instance or None """
    async with async_session() as session:
        async with session.begin():
            query = "SELECT * FROM users WHERE status='1' AND email=:email"
            result = await session.execute(text(query), {'email': email})
            return result.fetchone()


async def save_user(user: schema.UserCreate):
    """ Function takes user's information 
    and makes insert query to database table "Users" creating new user with provided credentials. """
    async with async_session() as session:
        async with session.begin():
            query = "INSERT INTO users (email, password, fullname, created_on, status) VALUES (:email, :password, :fullname, now() at time zone 'UTC', '1')"
            return await session.execute(text(query), {"email": user.email, "password": user.password, "fullname": user.fullname})
            


async def create_reset_code(email: str, reset_code: str):
    """ Function takes email and reset_code
    and makes insert query to database table "Codes" creating new unique set of data which includes email and reset_code """
    async with async_session() as session:
        async with session.begin():
            query = "INSERT INTO codes (email, reset_code, status, expired_in) VALUES (:email, :reset_code, '1', now() at time zone 'UTC')"
            return await session.execute(text(query), {'email': email, "reset_code": reset_code})

    