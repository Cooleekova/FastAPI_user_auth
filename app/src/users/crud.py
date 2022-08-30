from users import schema as user_schema
from auth import schema as auth_schema
from init_database import async_session
from sqlalchemy import text


async def update_user(
    request: user_schema.UserUpdate,
    current_user: auth_schema.UserList
):
    """ Function takes new user's credentials 
    and makes update type of query to database table "Users" updating user info with provided data. """ 
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE users SET fullname=:fullname WHERE email=:email"
            return await session.execute(text(query), {"fullname": request.fullname, "email": current_user.email})


async def deactivate_user(current_user: auth_schema.UserList):
    """ Function takes current user's credentials 
    and makes update type of query to database table "Users" changing user's status for 9 (what makes the account inactive)""" 
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE users SET status='9' WHERE status='1' AND email=:email"
            return await session.execute(text(query), {"email": current_user.email})


async def change_password(
    change_password_object: user_schema.ChangePassword,
    current_user: auth_schema.UserList
):
    """ Function takes current user's password and verifies it,
    if the current password is correct, it checks if two fields wth new password match  
    and makes update type of query to database table "Users" updating user's password""" 
    async with async_session() as session:
        async with session.begin():
            query = "UPDATE users SET password=:password WHERE status='1' AND email=:email"
            return await session.execute(text(query), {"password": change_password_object.new_password, "email": current_user.email})