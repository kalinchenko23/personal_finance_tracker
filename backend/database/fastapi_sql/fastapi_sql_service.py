import sys
import pathlib
sys.path.insert(0,f'{pathlib.Path.cwd().parents[0]}/database')
sys.path.insert(0,f'{pathlib.Path.cwd().parents[0]}/database/sql_service')
import sqlalchemy
from sqlalchemy import select
from pydantic_models import User
from session_sql import Session_aws, engine_aws
from db_tables import Users, base


def get_user(session: sqlalchemy.orm.session, username: str):
    stmt=select(Users).where(Users.username==username)
    result=session.scalars(stmt).first()
    return result

def create_user(session: sqlalchemy.orm.session, user: User):
   session.add(Users(**user.dict()))
   session.commit()

