from fastapi import FastAPI,Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .db import dbSession
from .model.user import User
from .api.users.router import router as userRouter

app = FastAPI()

app.include_router(userRouter)

@app.get("/")
async def get(db: dbSession):
    # user = User(id=0,username='miz',password="qwe")
    # db.add(user)
    # await db.commit()
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users