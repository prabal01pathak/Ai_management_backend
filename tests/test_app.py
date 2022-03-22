from fastapi.testclient import TestClient
from app import app
import requests
from .test import get_access_token

client = TestClient(app)

def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper

def test_get_access_token():
    access_token = get_access_token()
    assert access_token is not None

def get_token():
  access_token = get_access_token()
  return access_token

@memoize
def get_token_header():
  return {"Authorization": "Bearer " + get_token()}

def test_root():
    headers = get_token_header()
    #headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_projects():
    headers = get_token_header()
    response = client.get("/projects", headers=headers)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_get_project():
    headers = get_token_header()
    response = client.get("/images/1", headers=headers)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_get_image_file():
    headers = get_token_header()
    response = client.get("/images/1/1", headers=headers)
    assert response.status_code == 200
    assert type(response.content) == bytes
    assert response.headers["Content-Type"] == "image/jpeg"

def test_get_annotations():
    headers = get_token_header()
    response = client.get("images/annotations/1/1", headers=headers)
    assert response.status_code == 200

def test_image_annotation_save():
    headers = get_token_header()
    with open('test.py', 'rb') as f:
        file = f.read()
        response = client.post("/images/annotations/1", headers=headers, files = {"file": file})
    assert response.status_code == 200
    assert response.json() == {"message": "File saved"}
