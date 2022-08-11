import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import db_settings
from models import metadata

engine = create_async_engine(db_settings.data_source_name, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_all():
    async with async_session() as session:
        async with session.begin():
            return await session.run_sync(metadata.create_all)