import sys
import pathlib
import json
from fastapi import Depends
import jwt

sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/sql_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/token_service')
import sqlalchemy
from sqlalchemy import select
from db_tables import Accounts, Users, Tokens
from plaid_functionality_service import DB_service
from plaid.exceptions import ApiException
from token_workflow import Token_dash


async def get_user_banks(session,user_id):
    res=await session.execute(select(Tokens).filter(Tokens.user_id == user_id))
    obj = res.scalars().all()
    result={}
    for bank in obj:
        result[bank.id] = bank.bank_name
    return result



async def get_user_accounts_info(session, user_id):
    res = await session.execute(select(Tokens).filter(Tokens.user_id == user_id))
    obj = res.scalars().all()
    response={}
    for bank in obj:
        access_token = bank.token
        bank_name=bank.bank_name
        bank_id=bank.id
        try:
            await DB_service(session, access_token).insertORupdate_account_info(user_id,bank_name,bank_id)
            result = await session.execute(select(Accounts).filter((Accounts.user_id == user_id) &
                                                               (Accounts.bank_id == bank_id)))
            response[bank_id]={"bank_name":bank_name,"accounts":result.scalars().all(),"link_in_update_mode": None, "status":True}
        except ApiException as e:
            if "ITEM_LOGIN_REQUIRED" in e.body:
                token_dash=Token_dash()
                link_in_update_mode = token_dash.update_mode(access_token)
                response[bank_id] = {"bank_name":bank_name,"accounts":[], "link_in_update_mode": link_in_update_mode, "status":False}
            else:
                response[bank.bank_name] = e
    return response


#
# async def update_access_token(session, user_id, bank_name):
#     stmt = select(Tokens).where(Tokens.user_id == user_id and Tokens.bank_name == bank_name)
#     result = session.execute(stmt)
#     return {"token": result.scalars().first()}
