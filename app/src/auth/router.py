from os import access
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import uuid

from auth import schema, crud
from utils import crypto_util, jwt_util, constant_util, email_util



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
    access_token_expires = jwt_util.timedelta(minutes=constant_util.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt_util.create_access_token(
        data = {"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return {
        "acess_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    }

@router.post("/auth/reset-password")
async def reset_password(request: schema.ResetPassword):
    """ Endpoint for resetting user's password.
    Checks user existance,
    if there is a user with such an email in database,
    it forms reset_code and sends it directly to the provided email.
     """
    result = await crud.find_exist_user(request.email)
    if not result:
        raise HTTPException(status_code=404, detail="There is no account registered with provided email")

    # Reset code creation
    reset_code = str(uuid.uuid1())
    await crud.create_reset_code(request.email, reset_code)

    # Sending email
    subject = "FastAPI password reset"
    recepient = [request.email]
    message = f"""
        <h1>Hello, {request.email}!</h1>
        <p>Here is the link to reset your password: </p>
        <a href="http://127.0.0.1:8000/user/reset-password?reset_password_token={reset_code}></a>
    """

    await email_util.send_email(subject, recepient, message)

    return {"message": "Password reset code was sent. Check your email"}