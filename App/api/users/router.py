from fastapi import APIRouter, Depends, HTTPException, status
from app.db import dbSession
from app.schema.user import UserLogin, UserSchema
from app.schema.token import Token
from app.model.user import User
from typing import Annotated
from sqlalchemy import select
from app.utils.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/login")
async def login( db: dbSession, form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/signup")
async def signup(user_data: UserSchema, db: dbSession):
    user = User(**user_data.model_dump())
    user.password = get_password_hash(user.password)
    db.add(user)
    await db.commit()
    return {"msg":"success"}

@router.get("/", response_model=list[UserSchema])
async def get(db:dbSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/auth", response_model=list[UserSchema])
async def getauth(db:dbSession, current_user: Annotated[UserSchema,get_current_user]):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users