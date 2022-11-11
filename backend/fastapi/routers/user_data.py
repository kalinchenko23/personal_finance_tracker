import sys
import plaid
import pathlib
import jwt
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database/sql_service')
from fastapi import APIRouter, Depends
from dependencies import get_session,oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from user_data_service import get_user_accounts_info
from user_service import get_current_user
router = APIRouter()

@router.get("/accounts/get", status_code=200)
async def link_token(session: AsyncSession = Depends(get_session),jwt_token: str = Depends(oauth2_scheme)):
    current_user_id= await get_current_user(session,jwt_token)
    accounts, bank_name = await get_user_accounts_info(session,current_user_id.id)
    return {"detail": {"data": {bank_name : accounts}, "message": f"available accounts for {bank_name}"}}
