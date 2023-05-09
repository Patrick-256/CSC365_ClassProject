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
    # fantasy_team_id: int
    # fantast_league_id: int
    
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

@pydantic.dataclasses.dataclass
class Friend:
    user1_id: int
    user2_id: int

@pydantic.dataclasses.dataclass
class PlayerTeam:
    player_id: int
    fantasy_team_id: int


@router.post("/fantasy_leagues/", tags=["fantasy_leagues"])
def create_fantasy_league(new_fantasy_league_name: str):
    """Adds a new fantasy league with the
       specified name, adds user to league
       """
    # Figure out what id to assign this new fantasy league
    conn = db.engine.connect()
    max_id = conn.execute(sqlalchemy.select(func.max(db.fantasy_leagues.c.fantasy_league_id))).scalar()
    new_id = (max_id or 0) + 1

    insert_statement = """
    INSERT INTO fantasy_leagues (fantasy_league_id, fantasy_league_name)
    VALUES ({}, '{}')
    """.format(new_id,new_fantasy_league_name)

    with db.engine.begin() as conn:
        addUserResult = conn.execute(sqlalchemy.text(insert_statement))

        print(addUserResult)
    return {"Added fantasy league to the database!"}
    
@router.get("/fantasy_leagues/", tags=["fantasy_leagues"])
def list_fantasy_leagues():
    """lists the fantasy leagues from the table
    """

    sql = """select * from fantasy_leagues"""
    
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))
        res_json = []
        for row in result:
            res_json.append({
                "fantasy_league_id":row.fantasy_league_id,
                "fantasy_league_name":row.fantasy_league_name,
                "created_at":row.created_at,
            })
        return res_json


@router.get("/fantasy_leagues/{fantasy_league_id}", tags=["fantasy_leagues"])
def get_fantasy_leagues(id: int):
    """lists teams in the specified league in order of points
    """
    conn = db.engine.connect()

    sql = """select fantasy_team_id,
            SUM(games.num_goals) as total_goals
            from dantasy_teams
            join player_fantasy_teams on fantasy_teams.fantasy_team_id = player_fantasy_teams.fantasy_team_id
            join games on player_fantasy_teams.player_id = games.player_id
            where fantasy_teams.fantasy_league_id = """+id+"""
            group by fantasy_teams.team_id 
            order by total_goals DESC
    """
    
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))
        res_json = []
        for row in result:
            res_json.append({
                "fantasy_team_id":row.fantasy_league_id,
                "total_goals":row.fantasy_league_name,
            })
        return res_json


    

@router.get("/fantasy_leagues/{fantasy_league_id}/leaderboard", tags=["fantasy_leagues"])
def get_top_fantasy_leagues(limit: int):
    """lists fantasy leagues by score of the highest scoring team in the league"""


