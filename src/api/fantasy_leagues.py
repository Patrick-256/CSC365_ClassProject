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
def get_fantasy_leagues(fantasy_league_id: int):
        """lists teams in the specified league in order of points
        """

    

@router.get("/fantasy_leagues/{fantasy_league_id}/leaderboard", tags=["fantasy_leagues"])
def get_top_fantasy_leagues(limit: int):
    """lists fantasy leagues by score of the highest scoring team in the league"""


