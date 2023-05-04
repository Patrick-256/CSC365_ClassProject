from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()

@router.post("/players/", tags=["players"])
def add_player(name: str):
    """
    This endpoint adds a player to the database
    * `player_id`: the internal id of the player. 
    * `player_name`:
    * `player_position`:
    """
    
@router.put("/players/{id}/statistics", tags=["players"])
def edit_player(id: int):
    """
    This endpoint edits player statistics in the database
    * `player_id`: the internal id of the player. 
    * `player_name`:
    * `player_position`:
    """


@router.get("/players/{id}", tags=["players"])
def get_player(id: int):
    """
    This endpoint returns a single player by its identifier. For each player
    it returns:
    * `player_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `player_name`:
    * `player_position`:
    """

class player_sort_options(str, Enum):
    goals = "goals"
    assists = "assists"
    shots = "shots"
    shots_on_goal = "shots_on_goal"
    games_played = "games_played"


@router.get("/players/top?statistic={statistic}", tags=["players"])
def get_players(statistic: str, 
               limit: int = Query(50, ge=1, le=250),
               sort: player_sort_options = player_sort_options.goals):
    """
    """



