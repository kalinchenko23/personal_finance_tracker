import sys
import plaid
import pathlib
import jwt
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/token_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database/fastapi_sql')
from fastapi import FastAPI, Query, Body, HTTPException, Depends, Body, APIRouter
from dependencies import get_session,oauth2_scheme
from token_workflow import Token_dash
from token_service import create_access_token
from user_service import get_user, create_user, authenticate_user, get_current_user
from jwt_token_service import jwt_t_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
router = APIRouter()

#Token section of API

@router.get("/link_token", status_code=201)
def link_token(jwt_token:str = Depends(oauth2_scheme)):
    jwt_t_service.decode_jwt_token(jwt_token)
    link_token=Token_dash().create_link()
    return {"detail":{"data":link_token,"message":"link token was created"}}


@router.post("/access_token", status_code=201)
async def link_token(public_token:str=Body(embed=True), session: AsyncSession = Depends(get_session),
                     jwt_token: str = Depends(oauth2_scheme)):
        current_user=await get_current_user(session,jwt_token)
        try:
            access_token=Token_dash(public_token=public_token).access_token()
        except plaid.exceptions.ApiException:
            raise HTTPException(status_code=400, detail={"message":"Invalid public token.","data":""})
        await create_access_token (session,access_token,current_user.id)
        return {"detail":{"data":"","message":"access token was created"}}

