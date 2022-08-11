from pydantic import BaseModel, Field


# class UserCreate(BaseModel):
    # email: str = Field(..., example="example@example.com")
    # password : str = Field(..., example="********")
    # fullname: str = Field(..., example="Justin Biber")


class UserList(BaseModel):
    email: str
    fullname: str

class UserCreate(UserList):
    password : str = Field(..., example="********")

