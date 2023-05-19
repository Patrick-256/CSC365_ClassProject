from fastapi.testclient import TestClient

from src.api.server import app

import json
import src.database as db
import sqlalchemy

client = TestClient(app)


def test_create_fantasy_league():
    test_league = {
        "fantasy_league_name": "testCaseFantasyLeague05-19"
    }
    response = client.post("/fantasy_leagues/",test_league)
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            DELETE FROM fantasy_leagues
            WHERE fantasy_leagues_id = (SELECT MAX(fantasy_leagues_id) 
            FROM fantasy_leagues) 
            """
        conn.execute(sqlalchemy.text(sql))



def test_list_fantasy_league():
    response = client.get("/fantasy_leagues/")
    assert response.status_code == 200

    assert response.json()[0] ==  {
    "fantasy_league_id": 1,
    "fantasy_league_name": "Cal Poly Soccer",
    "created_at": "2023-05-09T01:45:46.363565+00:00"
  }
    
def test_get_top_teams_in_fantasy_league():
    response = client.get("/fantasy_leagues/{fantasy_league_id}?id=1")
    assert response.status_code == 200

    assert response.json() ==  [ #might change later
  {
    "fantasy_team_id": 1,
    "total_points": 54.25
  },
  {
    "fantasy_team_id": 3,
    "total_points": 40.55
  },
  {
    "fantasy_team_id": 0,
    "total_points": 24.35
  }
]
