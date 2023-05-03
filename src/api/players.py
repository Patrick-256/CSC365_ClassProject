from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy

router = APIRouter()

@router.get("/players/{id}", tags=["players"])
def get_user(id: int):
    """
    This endpoint returns a single player by its identifier. For each player
    it returns:
    * `player_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `player_name`:
    * `player_position`:
    """
