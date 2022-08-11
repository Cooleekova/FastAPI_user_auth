from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import schema, crud
from utils import crypto_util, jwt_util


router = APIRouter(
    prefix = "/api/v1"
)

@router.post("/auth/register", response_model=schema.UserList)
async def register(user: schema.UserCreate):
    """Endpoint for registering users.
    Checks user existance in database,
    if there is no user with provided email, creates new user"""
    result = await crud.find_exist_user(user.email)
    if result:
        raise HTTPException(status_code=404, detail="User already registered.")

    user.password = crypto_util.hash_password(user.password)
    await crud.save_user(user)
    return {**user.dict()}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Endpoint for login.
    Checks user existance,
    if there is a user with provided username in database, 
    it verufies the password and if provided password is correct, user logs in """
    result = await crud.find_exist_user(form_data.username)
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")
    user = schema.UserCreate(**result)

    # password verification
    password_match = crypto_util.verify_password(form_data.password, user.password)
    if not password_match:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    # Token creation


    return user

