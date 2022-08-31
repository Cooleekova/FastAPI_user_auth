from os import access
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import uuid

from auth import schema, crud
from utils import crypto_util, jwt_util, constant_util, email_util
from exceptions.business import BusinessException



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
        #raise HTTPException(status_code=404, detail="User already registered.")
        raise BusinessException(status_code=409, detail="User already registered.")

    user.password = crypto_util.hash_password(user.password)
    await crud.save_user(user)
    return {**user.dict()}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Endpoint for login.
    Checks user existance,
    if there is a user with provided username in database, 
    it verifies the password and if provided password is correct, user logs in """
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
        "access_token": access_token,
        "token_type": "Bearer",
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    }


@router.post("/auth/forgot-password")
async def forgot_password(request: schema.ForgotPassword):
    """ Endpoint for restoring forgotten password.
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
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={reset_code}">Reset my password</a>
    """
    
    await email_util.send_email(subject, recepient, message)

    return {"message": "Password reset code was sent. Check your email"}


@router.patch("/auth/reset-password")
async def reset_password(request: schema.ResetPassword):
    """ Endpoint for setting new user's password instead of forgotten one.
    User needs to provide unique reset password token and create a new password. """

    # Token validation
    reset_token = await crud.check_reset_password_token(request.reset_password_token)
    if not reset_token:
        raise HTTPException(status_code=404, detail='Reset password token has expired, please request a new one')

    # Checking new password and confirm password values to match
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=404, detail='Password and Confirm password should match, please try again.')

    # Saving new password in database
    forgot_password_user = schema.ForgotPassword(**reset_token)
    new_hashed_password = crypto_util.hash_password(request.new_password)
    await crud.reset_password(new_hashed_password, forgot_password_user.email)

    # Disabling used reset code
    await crud.disable_reset_code(request.reset_password_token, forgot_password_user.email)

    return {
        "code": 200,
        "message": "Password has been reset successfully."
    }