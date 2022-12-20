import sys
import pathlib
import json
from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}')
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/sql_service')
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/fastapi')
from jwt_token_service import password_check
import sqlalchemy
from sqlalchemy import select
from pydantic_service.pydantic_models import Users_pydantic, Tokens_pydantic
from session_sql import Session_aws, engine_aws
from db_tables import Users,Tokens,base

#Token specific functions

async def create_access_token(session: AsyncSession, access_token:str,user_id:int,bank_name:str):
    token=Tokens_pydantic(**{"user_id":user_id,"token":access_token,"bank_name":bank_name})
    session.add(Tokens(**token.dict()))
    await session.commit()

