from fastapi import APIRouter
from exceptions.business import BusinessException
from enums import otp
from otps import schema as otp_schema, crud as otp_crud
from utils import otp_util
import uuid


router = APIRouter(
    prefix = "/api/v1"
)


@router.post("/otp/send")
async def send_otp(
    type: otp.OTPType,
    request: otp_schema.CreateOTP
):
    # Check that OTP is not blocked
    otp_blocks = await otp_crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise BusinessException(status_code=403, detail="Sorry, this phone number is blocked for 5 minutes")

    # Generate otp_code and save to database
    otp_code = otp_util.random(6)
    session_id = str(uuid.uuid1())
    await otp_crud.save_otp(request, session_id, otp_code)

    return "OTP sent"


@router.post("/otp/verify")
async def verify_otp():
    return "put here your otp"