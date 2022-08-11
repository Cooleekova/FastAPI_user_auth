from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from auth import router as auth_router


#imports to check db connection begin >>>>>
from sqlalchemy import text
from init_database import async_session
#imports to check db connection end <<<<<

def get_application() -> FastAPI:
    application = FastAPI(
        debug=False,
        title='Betuple',
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





app.include_router(auth_router.router, tags = ["Auth"])