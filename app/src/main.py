from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from auth import router as auth_router
from users import router as user_router
from otps import router as otp_router
from exceptions.business import BusinessException


#imports to check db connection begin >>>>>
from sqlalchemy import text
from init_database import async_session
#imports to check db connection end <<<<<

def get_application() -> FastAPI:
    application = FastAPI(
        debug=False,
        title='FastAPI',
        version='0.0.1',
    )
    origins = [
        "http://localhost:3000",
        "http://localhost:8006",
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

#code to check db connection begin >>>>>
@app.get("/test")
async def read_root():
    return await get_time_service()


async def get_time_service():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text("SELECT now()"))
            timeResult = result.scalars().first()
            return str(timeResult)

#code to check db connection end <<<<<


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """Documentation: https://fastapi.tiangolo.com/tutorial/handling-errors/"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "detail": exc.detail},
    )


app.include_router(auth_router.router, tags = ["Auth"])
app.include_router(user_router.router, tags = ["Users"])
app.include_router(otp_router.router, tags = ["OTPs"])
