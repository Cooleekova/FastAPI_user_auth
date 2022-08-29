from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserList(BaseModel):
    id: int = None
    email: str = Field(..., example="example@example.com")
    fullname: str = Field(..., example="Justin Biber")
    created_on: Optional[datetime] = None
    status: str = None


class UserCreate(UserList):
    password : str = Field(..., example="********")


class ForgotPassword(BaseModel):
    email: str = Field(..., example="example@example.com")


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str

