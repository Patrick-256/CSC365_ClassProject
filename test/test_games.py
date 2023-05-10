from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_game_info():
    response = client.get("/games/0")
    assert response.status_code == 200


    with open("test/games/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)




def test_add_game():

    headers = {'Content-Type': 'application/json'}
    data = {
        "game_id": 4,
        "player_id": 1,
        "num_goals": 0,
        "num_assists": 0,
        "num_passes": 0,
        "num_shots_on_goal": 0,
        "num_turnovers": 0
    }
    response = client.post("/games/", headers=headers, data=json.dumps(data))
    assert response.status_code == 200