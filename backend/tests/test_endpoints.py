import sys
import pathlib
import pytest
from httpx import AsyncClient
sys.path.insert(0,f'{pathlib.Path(__file__).parents[1]}/fastapi')
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database/sql_service')
from fastapi.testclient import TestClient
from session_sql import Session_aws
from api_service import app, get_session

@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client




class TestEndpoiints:
    def test_connection(self,client):
        response=client.get("/")
        assert response.status_code == 200
        assert response.json()=={"message": "It's working!"}

    def test_loging_with_incorrect_credash(self,client):
        response=client.post("/login?username=some&password=some")
        assert response.status_code == 404


    def test_creating_user(self,client):
        response=client.post("/create_user/",
                             json= {"username":"some@gmail.com",
                                    "password":"some",
                                    "first_name":"myname",
                                    "last_name":"mylastname"})
        assert response.status_code == 201
