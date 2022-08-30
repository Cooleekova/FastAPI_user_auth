from fastapi import APIRouter, Depends, status
from auth import schema as auth_schema, crud as auth_crud
from users import schema as user_schema, crud as user_crud
from utils import jwt_util, crypto_util

from exceptions.business import BusinessException



router = APIRouter(
    prefix = "/api/v1"
)


@router.get("/user/profile")
async def get_user_profile(current_user: auth_schema.UserList = Depends(jwt_util.get_current_user)):
    return current_user
    

@router.patch("/user/profile")
async def update_user_profile(
    request: user_schema.UserUpdate,
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_user)
):

    # update user info
    await user_crud.update_user(request, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User updated successfully."
    }


@router.delete("/user/profile")
async def deactivate_account(
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):

    await user_crud.deactivate_user(current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User account has been deactivated successfully."
    }


@router.patch("/user/change-password")
async def change_password(
    change_password_object: user_schema.ChangePassword,
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
    # Check user existance
    result = await auth_crud.find_exist_user(current_user.email)
    if not result:
        raise BusinessException(status_code=404, detail="User not found.")

    # Verify current password
    user = auth_schema.UserCreate(**result)
    valid = crypto_util.verify_password(change_password_object.current_password, user.password)
    if not valid:
        raise BusinessException(status_code=401, detail="Current password is not valid.")

    # Check new password and confirm password match
    if change_password_object.new_password != change_password_object.confirm_password:
        raise BusinessException(status_code=401, detail="New password and confirmation should be equal")

    # Hashing password and saving into database
    change_password_object.new_password = crypto_util.hash_password(change_password_object.new_password)
    await user_crud.change_password(change_password_object, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Password has been changed successfully."
    }
