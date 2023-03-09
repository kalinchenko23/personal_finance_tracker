import sys
import plaid
import pathlib
import jwt
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database/sql_service')
from fastapi import APIRouter, Depends
from dependencies import get_session,oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from user_data_service import get_user_accounts_info, get_user_banks
from user_service import get_current_user
router = APIRouter()


@router.get("/api/connected_banks/get", status_code=200)
async def get_registered_banks(session:AsyncSession = Depends(get_session),jwt_token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(session, jwt_token)
    result= await get_user_banks(session,current_user.id)
    return {"detail": {"data": result, "message": "List of connected banks"}}



@router.get("/api/accounts/get", status_code=200)
async def link_token(session: AsyncSession = Depends(get_session),jwt_token: str = Depends(oauth2_scheme)):
    current_user_id= await get_current_user(session,jwt_token)
    response = await get_user_accounts_info(session,current_user_id.id)
    return {"detail":{"data":response, "message": "List of all connected banks and accounts"}}