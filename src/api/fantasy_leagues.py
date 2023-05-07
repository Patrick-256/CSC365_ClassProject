from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()


@router.post("/fantasy_leagues/", tags=["fantasy_leagues"])
def create_fantasy_league(user_id: int, name: str):
    """Adds a new fantasy league with the
       specified name, adds user to league
       """
    
    

@router.get("/fantasy_leagues/{fantasy_league_id}", tags=["fantasy_leagues"])
def get_fantasy_leagues(id: int):
    """lists teams in the specified league in order of points
    """
    conn = db.engine.connect()

    sql = """select 
            fantasy_team_id,
            ????POINTS???? as Points
            from players
            join games on players.player_id = games.player_id
            join fantasy_leauges on fantasy_teams.fantasy_league_id = fantasy_leagues.fantasy_league_id
            where fantasy_leagues.fantasy_league_id = """+id+""" 
            order by Points desc
    """
    

    conn.execute(sqlalchemy.text(sql))

    return id


    

@router.get("/fantasy_leagues/{fantasy_league_id}/leaderboard", tags=["fantasy_leagues"])
def get_top_fantasy_leagues(limit: int):
    """lists fantasy leagues by score of the highest scoring team in the league"""


