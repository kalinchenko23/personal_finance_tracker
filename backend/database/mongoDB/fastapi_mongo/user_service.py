import sys
import pathlib
# sys.path.insert(0,pathlib.Path(__file__).parents[1])
from mongoDB.mongo_connection_service import connection_mongo
from pydantic_service.pydantic_models import Users_pydantic, Tokens_pydantic
from mongoDB.documents import Users
con =connection_mongo()

class User ():
    def __init__(self,engine):
        self.engine=engine

    def create_user(self,obj):
        user=Users(**obj.dict())
        user.save()
        return user
user_mongo=User(con)
