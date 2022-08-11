from init_database import async_session
from sqlalchemy import text
from auth import schema

async def find_exist_user(email: str):
    async with async_session() as session:
        async with session.begin():
            query = "select * from users where status='1' and email=:email"
            result = await session.execute(text(query), {'email': email})
            return result.fetchone()

async def save_user(user: schema.UserCreate):
    async with async_session() as session:
        async with session.begin():
            query = "INSERT INTO users (email, password, fullname, created_on, status) VALUES (:email, :password, :fullname, now() at time zone 'UTC', '1')"
            result = await session.execute(text(query), {"email": user.email, "password": user.password, "fullname": user.fullname})
            return result
    