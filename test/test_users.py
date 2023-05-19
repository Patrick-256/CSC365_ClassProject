from fastapi.testclient import TestClient

from src.api.server import app

import json
import src.database as db
import sqlalchemy

client = TestClient(app)

def test_get_user():
    response = client.get("/users/")
    assert response.status_code == 200

    assert response.json()[0] ==  {
    "user_id": 0,
    "user_name": "Pata_Data",
    "is_admin": True,
  }
    
def test_add_user():
    test_user = {
        "user_name": "unitTest05-19",
        "is_admin": False,
        "password":"myPassword123"
    }
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            DELETE FROM users
            WHERE user_id = (SELECT MAX(user_id) 
            FROM users) 
            """
        conn.execute(sqlalchemy.text(sql))
