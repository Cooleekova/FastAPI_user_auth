from fastapi import APIRouter, status
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

    return {
        "recipient_id": request.recipient_id,
        "session_id": session_id,
        "otp_code": otp_code
    }


@router.post("/otp/verify")
async def verify_otp(
    request: otp_schema.VerifyOTP
):
    # Check that OTP is not blocked
    otp_blocks = await otp_crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise BusinessException(status_code=403, detail="Sorry, this phone number is blocked for 5 minutes")
    
    # Check OTP code lifetime (code expires in 60 seconds)
    lifetime_result = await otp_crud.find_otp_lifetime(request)
    
    if not lifetime_result:
        raise BusinessException(status_code=403, detail="The OTP code has expired, please request a new one")
    # If OTP code is not expired, we use it further as 'current_otp_oject' variable
    
    current_otp_oject = otp_schema.OTPList(**lifetime_result)
    
    # Check if OTP code is already used
    if current_otp_oject.status == "9":
        raise BusinessException(status_code=403, detail="This OTP code has already been used, please request a new one")
    
    # Verify OTP code provided by user
    # If OTP does not match, increment otp_failed_times counter
    # If OTP have not matched for 5 times, block OTP code
    if current_otp_oject.otp_code != request.otp_code:
        await otp_crud.update_otp_failed_count(current_otp_oject)
        if current_otp_oject.otp_failed_count >= 5:
            await otp_crud.block_otp_code(current_otp_oject)
            raise BusinessException(status_code=403, detail="Sorry, this phone number is blocked for 5 minutes")
        raise BusinessException(status_code=404, detail="The OTP code you've entered is incorrect")

    # Disable OTP code after successful verification
    await otp_crud.disable_otp_code(current_otp_oject)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "OTP Verified successfully"
    }