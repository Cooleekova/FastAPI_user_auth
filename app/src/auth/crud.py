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
            query = "INSERT INTO codes (email, reset_code, status, expired_in) VALUES (:email, :reset_code, '1', now() AT TIME ZONE 'UTC')"
            return await session.execute(text(query), {'email': email, "reset_code": reset_code})


async def check_reset_password_token(reset_password_token: str):
    """ Function takes reset_code_token
    and checks if it exists in database and not expired """
    async with async_session() as session:
        async with session.begin():
            query = "SELECT * FROM codes WHERE status='1' AND reset_code=:reset_password_token \
                AND expired_in >= now() AT TIME ZONE 'UTC' - INTERVAL '10 minutes'"
            result =  await session.execute(text(query), {'reset_password_token': reset_password_token})
            return result.fetchone()


async def reset_password(new_hashed_password: str, email: str):
    """ Function takes new password entered by user and user's email
    and saves new password into database """
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE users SET password=:password WHERE email=:email"
            return await session.execute(text(query), {'password': new_hashed_password, "email": email})


async def disable_reset_code(reset_password_token: str, email: str):
    """ Function takes reset password code and user's email
    and disables this code in database by changing its status so the code cannot be used again """
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE codes SET status='9' WHERE status='1' AND reset_code=:reset_code AND email=:email"
            return await session.execute(text(query), {'reset_code': reset_password_token, "email": email})

    