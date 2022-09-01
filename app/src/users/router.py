from fastapi import APIRouter, Depends, status, File, UploadFile
from auth import schema as auth_schema, crud as auth_crud
from users import schema as user_schema, crud as user_crud
from utils import jwt_util, crypto_util

from exceptions.business import BusinessException
import os
from PIL import Image


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



@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt_util.get_user_token),
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):

    # Saving used token to blacklist
    await user_crud.save_black_list_token(token, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User logged out successfully."
    }


@router.post("/user/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
    cwd = os.getcwd()
    path_image_dir = "upload_images/user/profile/" + str(current_user.id) + "/"
    full_image_path = os.path.join(cwd, path_image_dir, file.filename)

    # Create directory if does not exist
    if not os.path.exists(path_image_dir):
        os.makedirs(path_image_dir)

    # Rename file to 'profile.png'
    file_name = full_image_path.replace(file.filename, "profile.png")

    # Write file
    with open(file_name, 'wb+') as f:
        f.write(file.file.read())
        f.flush()
        f.close()

    return {
        "profile_image": os.path.join(path_image_dir, "profile.png")
    }



@router.get("/user/profile-image")
async def get_profile_image(
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
    cwd = os.getcwd()
    path_image_dir = "upload_images/user/profile/" + str(current_user.id) + "/"
    full_image_path = os.path.join(cwd, path_image_dir, "profile.png")

    # Check if the directory exists and resize profile picture with Pillow library
    if os.path.exists(full_image_path):
        with Image.open(full_image_path) as im:
            im.thumbnail((400, 400), Image.ANTIALIAS)
            im.save(path_image_dir + "profile_400x400.png")

    return {
        "profile_image": os.path.join(path_image_dir, "profile_400x400.png")
    }