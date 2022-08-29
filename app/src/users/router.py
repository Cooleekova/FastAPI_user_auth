from fastapi import APIRouter, Depends
from auth import schema
from utils import jwt_util



router = APIRouter(
    prefix = "/api/v1"
)


@router.get("/user/profile")
async def get_user_profile(current_user: schema.UserList = Depends(jwt_util.get_current_user)):
    return current_user
    
