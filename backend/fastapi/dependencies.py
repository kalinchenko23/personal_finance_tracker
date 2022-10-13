import sys
import pathlib
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database/sql_service')
import pathlib
from fastapi.security import OAuth2PasswordBearer
from session_sql import Session_aws

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_session():
    async with Session_aws() as sess:
        yield sess
