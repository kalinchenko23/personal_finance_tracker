import sys
import pathlib
import json
from fastapi import Depends
import jwt
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/sql_service')
import sqlalchemy
from sqlalchemy import select
from db_tables import Accounts, Users, Tokens
from plaid_functionality_service import DB_service

async def get_user_accounts_info(session, user_id):
    access_token = await session.execute(select(Tokens).filter(Tokens.user_id == user_id))
    access_token = access_token.scalars().first().token
    await DB_service(session, access_token).insertORupdate_account_info(user_id)
    result = await session.execute(select(Accounts).filter(Accounts.user_id == user_id))
    return result.scalars().all()
