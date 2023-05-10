from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_player():
    response = client.get("/players/2")
    assert response.status_code == 200

    expected = {
        "player_id": 2,
        "player_name": "Lucas",
        "player_position": "RB",
        "irl_team_name": "Seattle Sounders",
        "total_num_goals": 5,
        "total_num_assists": 4,
        "total_num_passes": 43,
        "total_num_shots_on_goal": 8,
        "total_num_turnovers": 1  
    }

    assert response.json() == expected


def test_get_players():
    response = client.get("/players/?sort=num_goals&limit=5")
    assert response.status_code == 200

    with open("test/players/sort=num_goals&limit=5.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_edit_player():
    response = client.put("/players/1/info?position=ST&irl_team_name=Manchester City")
    assert response.status_code == 200


def test_add_player():
    response = client.post("/players/?name=Johnny&irl_team_name=Arsenal&position=GK")
    assert response.status_code == 200