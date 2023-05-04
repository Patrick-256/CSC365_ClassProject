from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()

@router.post("/users/", tags=["users"])
def add_user(name: str):
    """
    This endpoint adds a user to the database
    """


@router.post("/users/{fantasy_league_id}/join", tags=["users"])
def add_user_to_fantasy_league(id: int):
    """
    """




