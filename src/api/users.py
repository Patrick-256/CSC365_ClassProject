from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()

class Friend:
    user1_id: int
    user2_id: int

class User:
    user_id: int
    user_name: str
    is_admin: bool
    friends: list[Friend]
    fantasy_team_id: int
    fantast_league_id: int

class Player:
    player_id: int
    player_name: str
    player_position: str
    irl_team_name: str

class Fantasy_Team:
    fantasy_team_id: int
    fantasy_team_name: str
    players: list[Player]
    fantasy_league_id: int


@router.post("/users/", tags=["users"])
def add_user(new_user: User):
    """
    This endpoint adds a user to the database
    """
    print(new_user)

    #  print(addUserResult)
    return {"Added user to the database!"}


@router.post("/users/{fantasy_league_id}/join", tags=["users"])
def add_user_to_fantasy_league(id: int):
    """
    This endpoint adds a user to a fantasy league
    """




