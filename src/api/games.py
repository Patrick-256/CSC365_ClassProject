from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()


@router.post("/games/", tags=["games"])
def add_game():
        """"""
        


@router.get("/games/{game_id}", tags=["games"])
def get_game_info(game_id: int):
        """returns information about the specified game
        """