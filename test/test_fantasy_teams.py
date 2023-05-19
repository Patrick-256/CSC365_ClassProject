from fastapi.testclient import TestClient

from src.api.server import app

import json
import src.database as db
import sqlalchemy

client = TestClient(app)

def test_get_team_score():
    response = client.get("/fantasy_teams/3/score")
    assert response.status_code == 200

    expected = {
            "team_id": 3,
            "Total_score": 10.65
    }

    assert response.json() == expected


def test_create_team():

    headers = {'Content-Type': 'application/json'}
    data = {
        "fantasy_team_name": "The Best Team",
        "user_id": 1,
        "fantasy_league_id": 0
        }
    response = client.post("/fantasy_teams/", headers=headers, data=json.dumps(data))
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            DELETE FROM fantasy_teams
            WHERE fantasy_team_id = (SELECT MAX(fantasy_team_id) 
            FROM fantasy_teams) 
            """
        conn.execute(sqlalchemy.text(sql))


def test_add_player_to_fantasy_team():
    headers = {'Content-Type': 'application/json'}
    data = {
        "player_id": 1,
        "fantasy_team_id": 3
        }
    response = client.post("/fantasy_teams/players", headers=headers, data=json.dumps(data))
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            DELETE FROM player_fantasy_team
            WHERE player_id = 1 and fantasy_team_id = 3 
            """
        conn.execute(sqlalchemy.text(sql))


def test_remove_player_from_fantasy_team():
    headers = {'Content-Type': 'application/json'}
    data = {
        "player_id": 1,
        "fantasy_team_id": 3
        }
    response = client.delete("/fantasy_teams/3/players", headers=headers, data=json.dumps(data))
    assert response.status_code == 200



def test_add_team_to_fantasy_league():

    with db.engine.begin() as conn:

        prev_subq = """
            select fantasy_league_id
            from fantasy_teams
            where fantasy_team_id = 30
        """

        prev = conn.execute(sqlalchemy.text(prev_subq)).scalar_one()

    response = client.put("/fantasy_teams/{fantasy_league_id}/join?team_id=30&league_id=7")
    assert response.status_code == 200

    #clean up
    with db.engine.begin() as conn:

        sql = """
            update fantasy_teams
            set fantasy_league_id = (:prev)
            where fantasy_team_id = 30
            """
        conn.execute(sqlalchemy.text(sql),{'prev':prev})

    