from fastapi.testclient import TestClient

from src.api.server import app

import json
import src.database as db
import sqlalchemy

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

    with db.engine.begin() as conn:

        prev_subq = """
            select player_position, irl_team_name
            from players
            where player_id = 1
        """

        prev = conn.execute(sqlalchemy.text(prev_subq)).fetchone()


    response = client.put("/players/1/info?position=LW&irl_team_name=Manchester City")
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            update players
            set player_position = (:prev_pos), 
                irl_team_name = (:prev_team)
            where player_id = 1
            """
        conn.execute(sqlalchemy.text(sql),{'prev_pos':prev.player_position, 'prev_team': prev.irl_team_name})


def test_add_player():
    response = client.post("/players/?name=Johnny&irl_team_name=Arsenal&position=GK")
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            DELETE FROM players
            WHERE player_id = (SELECT MAX(player_id) 
            FROM players) 
            """
        conn.execute(sqlalchemy.text(sql))
    
