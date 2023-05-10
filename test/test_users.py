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
