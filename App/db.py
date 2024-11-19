from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Annotated
from fastapi import Depends

# Create an async engine for SQLite
async_engine = create_async_engine(
    "sqlite+aiosqlite:///database.db",
    echo=True,
)


asyncSession = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)   

async def get_session():
    async with asyncSession() as session:
        yield session

dbSession = Annotated[AsyncSession, Depends(get_session)]