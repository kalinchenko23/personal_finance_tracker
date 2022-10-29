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

class JWT():
    def __init__(self,secret_key=secret_key,algorithm=algorithm):
        self.secret_key=secret_key
        self.algorithm=algorithm

    def create_jwt_token(self,user: Users_pydantic):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode = {"username":user.username,"first":user.first_name,"last":user.last_name,"exp":expiration}
        jwt_token=jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return jwt_token

    def decode_jwt_token(self, jwt_token: str):
        try:
            token_info = jwt.decode(jwt_token, self.secret_key, self.algorithm)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail={"message":"Your session has expired","data":""})
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail={"message":"Please provide valid jwt token","data":""})
        return token_info

jwt_t_service=JWT()