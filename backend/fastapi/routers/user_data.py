import sys
import plaid
import pathlib
import jwt
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database/sql_service')
from fastapi import APIRouter, Depends
from dependencies import get_session,oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from user_data_service import get_user_accounts_info, update_access_token
from user_service import get_current_user
from plaid.exceptions import ApiException
router = APIRouter()

@router.get("/accounts/get", status_code=200)
async def link_token(session: AsyncSession = Depends(get_session),jwt_token: str = Depends(oauth2_scheme)):
    current_user_id= await get_current_user(session,jwt_token)
    try:
        response = await get_user_accounts_info(session,current_user_id.id)
        return {"detail": {"data": response, "message": f"available accounts"}}
    except ApiException:
        return update_access_token(session,current_user_id,bank_name)

