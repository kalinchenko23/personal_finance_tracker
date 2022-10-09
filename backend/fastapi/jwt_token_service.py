import sys
import pathlib
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database')
import bcrypt
import datetime
import json
import jwt
from fastapi import HTTPException
from pydantic_service.pydantic_models import Users_pydantic

with open(f'{pathlib.Path(__file__).parents[1]}/classified.json') as secret_file:
    secrets = json.load(secret_file)
    secret_key,algorithm = secrets['jwt']['secret_key'],secrets['jwt']['algorithm']


def password_check(password: str, hasshed_password: bytes):
    return bcrypt.checkpw(password.encode(), hasshed_password)


def create_jwt_token(user: Users_pydantic, secret_key= secret_key):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode = {"sub":user.username,"exp":expiration}
    jwt_token=jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return jwt_token

def decode_jwt_token(jwt_token: str):
    with open(f'{pathlib.Path(__file__).parents[1]}/classified.json') as secret_file:
        secrets = json.load(secret_file)
        secret_key, algorithm = secrets['jwt']['secret_key'], secrets['jwt']['algorithm']
    try:
        token_info = jwt.decode(jwt_token, secret_key, algorithm)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Your session has expired")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Please provide valid jwt token")
    return token_info