from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_user():
    response = client.get("/users/")
    assert response.status_code == 200

    assert response.json()[0] ==  {
    "user_id": 0,
    "user_name": "Pata_Data",
    "is_admin": True,
    "created_at": "2023-05-07T17:30:11+00:00"
  }
    
def test_add_user():
    test_user = {
        "user_name": "unitTest01",
        "is_admin": False
    }
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
