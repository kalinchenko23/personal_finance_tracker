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
    res = await session.execute(select(Tokens).filter(Tokens.user_id == user_id))
    obj = res.scalars().all()
    response={}
    for bank in obj:
        access_token = bank.token
        bank_name=bank.bank_name
        await DB_service(session, access_token).insertORupdate_account_info(user_id,bank_name)
        result = await session.execute(select(Accounts).filter((Accounts.user_id == user_id) &
                                                               (Accounts.bank_name == bank.bank_name)))
        response[bank.bank_name]=result.scalars().all()
    return response



async def update_access_token(session, user_id, bank_name):
    stmt = select(Tokens).where(Tokens.user_id == user_id and Tokens.bank_name == bank_name)
    result = session.execute(stmt)
    return {"token": result.scalars().first()}
