import sys
import pathlib
sys.path.insert(0,f'{pathlib.Path(__file__).parents[1]}/fastapi')
from fastapi.testclient import TestClient
from api_service import app

client = TestClient(app)

class TestEndpoiints:
    def test_connection(self):
        response=client.get("/")
        assert response.status_code == 200
        assert response.json()=={"message": "It's working!"}

    def test_loging_with_incorrect_credash(self):
        response=client.post("/login?username=some&password=some")
        assert response.status_code == 404

    def test_loging_with_incorrect_credentials(self):
        response = client.post("/login?username=some&password=some")
        assert response.status_code == 404

    def test_creating_user(self):
        response=client.post("/user_create", json= {"userame":"some@gmail.com",
                                                    "password":"some",
                                                    "first_name":"myname",
                                                    "last_name":"mylastname"})
        response.status_code == 201
