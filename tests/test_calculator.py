from fastapi.testclient import TestClient
from app.main import app
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_add():
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_subtract():
    response = client.get("/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 6

def test_multiply():
    response = client.get("/multiply?a=6&b=7")
    assert response.status_code == 200
    assert response.json()["result"] == 42

def test_divide():
    response = client.get("/divide?a=8&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 4

def test_divide_by_zero():
    response = client.get("/divide?a=8&b=0")
    assert response.status_code == 400
