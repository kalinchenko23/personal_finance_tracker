import sys
import pathlib
import json
from fastapi import Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}')
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/sql_service')
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/fastapi')
from jwt_token_service import password_check
import sqlalchemy
from sqlalchemy import select
from pydantic_models import Users_pydantic
from session_sql import Session_aws, engine_aws
from db_tables import Users, base

with open(f'{pathlib.Path(__file__).parents[2]}/classified.json') as secret_file:
    secrets = json.load(secret_file)
    secret_key, algorithm = secrets['jwt']['secret_key'], secrets['jwt']['algorithm']


async def get_user(session: AsyncSession, username: str):
    stmt = select(Users).where(Users.username == username)
    user = await session.scalars(stmt)
    return user.first()


async def create_user(session: AsyncSession, user: Users_pydantic):
    session.add(Users(**user.dict()))
    await session.commit()


async def authenticate_user(session: AsyncSession, username: str, password: str):
    stmt = select(Users).where(Users.username == username)
    obj = await session.scalars(stmt)
    user=obj.first()
    if not password_check(password, user.password) or not user:
        return False
    return True



async def get_current_user(session: AsyncSession, token:str):
    try:
        username = jwt.decode(token, secret_key, algorithm)["sub"]
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    user = await get_user(session, username)
    return user
