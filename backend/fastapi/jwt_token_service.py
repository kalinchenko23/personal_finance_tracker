import sys
import pathlib
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database')
import bcrypt
import datetime
import json
import jwt
from pydantic_models import Users_pydantic

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

# print(password_check('kalina','JDJiJDEyJEVrQzhic3hwV0hwbzMuSnI3WEpJQXVkUzBOS1I2ak83ZnpjTC55OVVJamtiQktHbnMuaG11'))