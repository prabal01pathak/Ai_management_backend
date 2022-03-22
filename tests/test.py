import requests
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

server_url = 'http://localhost:8000'

data = {
    "username": "johndoe",
    "password": "hello"
}

def get_access_token():
    result = client.post(server_url + '/auth/token', data=data)
    access_token = result.json()['access_token']
    return access_token
