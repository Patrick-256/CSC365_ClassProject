from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_user():
    response = client.get("/users/")
    assert response.status_code == 200

    assert response.json() == [ # Need to figure out a way to just get first 2 users
  {
    "user_id": 0,
    "user_name": "Pata_Data",
    "is_admin": True,
    "created_at": "2023-05-07T17:30:11+00:00"
  },
  {
    "user_id": 1,
    "user_name": "Darth Vader",
    "is_admin": False,
    "created_at": "2023-05-07T20:30:21+00:00"
  },
  {
    "user_id": 2,
    "user_name": "testUser",
    "is_admin": False,
    "created_at": "2023-05-08T07:06:30+00:00"
  },
  {
    "user_id": 3,
    "user_name": "testUser2",
    "is_admin": False,
    "created_at": "2023-05-08T21:19:13.996993+00:00"
  },
  {
    "user_id": 4,
    "user_name": "testUser0508_0",
    "is_admin": False,
    "created_at": "2023-05-09T04:19:09.651197+00:00"
  }
]