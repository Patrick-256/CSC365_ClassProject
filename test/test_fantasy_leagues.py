from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_create_fantasy_league():
    response = client.post("/fantasy_leagues/?new_fantasy_league_name=testCaseFantasyLeague01")
    assert response.status_code == 200



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
    "total_points": 51.2
  },
  {
    "fantasy_team_id": 0,
    "total_points": 24.35
  }
]
