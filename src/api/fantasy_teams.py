from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
import pydantic.dataclasses

router = APIRouter()

@pydantic.dataclasses.dataclass
class User:
    # user_id: int
    user_name: str
    is_admin: bool
    
    
@pydantic.dataclasses.dataclass
class Player:
    player_id: int
    player_name: str
    player_position: str
    irl_team_name: str

@pydantic.dataclasses.dataclass
class Fantasy_Team:
    fantasy_team_id: int
    fantasy_team_name: str
    user_id: int
    fantasy_league_id: int 

@pydantic.dataclasses.dataclass
class Friend:
    user1_id: int
    user2_id: int

@pydantic.dataclasses.dataclass
class PlayerTeam:
    player_id: int
    fantasy_team_id: int

@router.post("/fantasy_teams/", tags=["fantasy_teams"])
def create_fantasy_team(team: Fantasy_Team):
    """Adds a new fantasy team with the
       specified user id
       """
    
    conn = db.engine.connect()

    max_id = conn.execute(sqlalchemy.select(func.max(db.fantasy_teams.c.fantasy_team_id))).scalar()
    new_id = (max_id or 0) + 1

    sql = """
          INSERT INTO fantasy_teams (fantasy_team_id, fantasy_team_name, user_id)
          VALUES ({},{},{})""".format(new_id, team.fantasy_team_name, team.user_id)

    conn.execute(sqlalchemy.text(sql))

    return new_id
    

@router.post("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def add_player_to_fantasy_team(player_team: PlayerTeam):
    """adds a player to the specified fantasy team
    """

    conn = db.engine.connect()


    sql = """
          INSERT INTO player_fantasy_team (player_id, fantasy_team_id)
          VALUES ({},{})""".format(player_team.player_id, player_team.fantasy_team_id)

    conn.execute(sqlalchemy.text(sql))

    return {"Added player to team"}


@router.delete("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def remove_player_from_fantasy_team(player_team: PlayerTeam):
    """removes a player from the specified fantasy team
    """

    conn = db.engine.connect()


    sql = """
          delete from player_fantasy_team
          where player_id = {} and fantasy_team_id = {}
          """.format(player_team.player_id, player_team.fantasy_team_id)

    conn.execute(sqlalchemy.text(sql))

    return {"Removed player from team"}



@router.get("/fantasy_teams/{fantasy_team_id}/score", tags=["fantasy_teams"])
def get_fantasy_team_score(fantasy_team_id: int):
    """return the score of the specified fantasy team,
       which is a sum of the team's player scores"""
    
    conn = db.engine.connect()
        
    sql = """
            SELECT player_fantasy_team.fantasy_team_id, SUM(player_score) AS total_team_score
        FROM (
        SELECT player_fantasy_team.player_id, SUM(num_goals*5 + num_assists*3 + num_passes*0.05 + num_shots_on_goal*0.2 - num_turnovers*0.2) AS player_score
        FROM player_fantasy_team
        JOIN games ON games.player_id = player_fantasy_team.player_id
        WHERE player_fantasy_team.fantasy_team_id = {}
        GROUP BY player_fantasy_team.player_id
        ) AS subquery
        JOIN player_fantasy_team ON player_fantasy_team.player_id = subquery.player_id
        GROUP BY player_fantasy_team.fantasy_team_id
        """.format(fantasy_team_id)

    result = conn.execute(sqlalchemy.text(sql)).fetchone()

    return {
        "player_id": result.fantasy_team_id,
        "Total_score": result.total_team_score
    }
    


@router.put("/users/{fantasy_league_id}/join", tags=["users"])
def add_team_to_fantasy_league(team: Fantasy_Team):
    """
    This endpoint adds a user to a fantasy league
    It sets the league_id column of a team
    """

    conn = db.engine.connect()

    sql = """
          update fantasy_teams
          set fantasy_league_id = {}
          where team_id = {}
          """.format(team.fantasy_league_id, team.fantasy_team_id)
        

    conn.execute(sqlalchemy.text(sql))

    return ("Team addded to fantasy league")
