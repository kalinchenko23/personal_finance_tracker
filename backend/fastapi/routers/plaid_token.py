import sys
import plaid
import pathlib
import jwt
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/token_service')
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/plaid_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database/sql_service')
from fastapi import FastAPI, Query, Body, HTTPException, Depends, Body, APIRouter
from sqlalchemy import select
from dependencies import get_session,oauth2_scheme
from token_workflow import Token_dash
from token_service import create_access_token
from plaid_dashboard import plaid_service
from user_service import get_user, create_user, authenticate_user, get_current_user
from jwt_token_service import jwt_t_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from db_tables import Tokens
router = APIRouter()
#Token section of API

#To create a link token
@router.get("/api/link/token/create", status_code=201)
def link_token(jwt_token:str = Depends(oauth2_scheme)):
    jwt_t_service.decode_jwt_token(jwt_token)
    link_token=Token_dash().create_link()
    return {"detail":{"data":link_token,"message":"link token was created"}}

#To get an access token
@router.post("/api/access_token", status_code=201)
async def link_token(public_token:str = Body(embed=True), session: AsyncSession = Depends(get_session),
                     jwt_token: str = Depends(oauth2_scheme)):
        current_user=await get_current_user(session,jwt_token)
        try:
            token_dash=Token_dash()
            access_token=token_dash.access_token(public_token)
            inst_id = plaid_service.get_institutions_id(access_token)
            bank_name = plaid_service.get_institutions_name(inst_id)
        except plaid.exceptions.ApiException:
            raise HTTPException(status_code=400, detail={"message":"Invalid public token.","data":""})
        await create_access_token (session,access_token,current_user.id,bank_name)
        return {"detail":{"data":"","message":"access token was created"}}

# #TO CREATE LINK TOKEN IN UPDATE MODE
# @router.post("/api/access_token/update", status_code=200)
# async def access_token_update(session: AsyncSession = Depends(get_session), jwt_token: str = Depends(oauth2_scheme)):
#     current_user = await get_current_user(session, jwt_token)
#     stmt=select(Tokens).where(Tokens.user_id==current_user.id)
#     result=await session.execute(stmt)
#     expired_access_token=result.scalars().first().token
#     # link_token_update_mode = Token_dash(expired_access_token).create_link()
#     return {"msg":expired_access_token}
