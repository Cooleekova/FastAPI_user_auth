from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str = Field(..., example="example@example.com")
    fullname: str = Field(..., example="Justin Biber")


class UserCreate(UserList):
    password : str = Field(..., example="********")


class ForgotPassword(BaseModel):
    email: str = Field(..., example="example@example.com")


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str

