from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()


@router.post("/fantasy_teams/", tags=["fantasy_teams"])
def create_fantasy_team(user_id: int, name: str):
    """Adds a new fantasy team with the
       specified user id
       """
    

@router.post("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def add_player_to_fantasy_team(player_id: int, fantasy_team_id: str):
    """adds a player to the specified fantasy team
    """


@router.delete("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def remove_player_from_fantasy_team(player_id: int, fantasy_team_id: str):
    """removes a player from the specified fantasy team
    """


@router.get("/fantasy_teams/{fantasy_team_id}/score", tags=["fantasy_teams"])
def get_fantasy_team_score(fantasy_team_id: int):
    """return the score of the specified fantasy team,
       which is a sum of the team's player scores"""
    

    




