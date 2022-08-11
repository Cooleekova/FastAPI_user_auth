import jwt
from datetime import datetime, timedelta
from utils import constant_util

async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constant_util.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constant_util.SECRET_KEY, algorithm=constant_util.ALGORITHM_HS256)
