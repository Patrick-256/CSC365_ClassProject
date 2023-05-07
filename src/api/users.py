from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from src import database as db
import sqlalchemy
import pydantic.dataclasses
router = APIRouter()

class Friend:
    user1_id: int
    user2_id: int

@pydantic.dataclasses.dataclass
class User:
    user_id: int
    user_name: str
    is_admin: bool
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
    fantasy_league_id: int


@router.post("/users/", tags=["users"])
def add_user(new_user: User):
    """
    This endpoint adds a user to the database
    """
    print(new_user)
    conn = db.engine.connect()

    sql = """
          INSERT INTO users (user_id, user_name, is_admin)
          VALUES ("""+new_user.new_id+", "+new_user.name+", "+new_user.is_admin+""")
    """

    conn.execute(sqlalchemy.text(sql))

    # insert_statment = sqlalchemy.insert(db.users).values(
    #     user_id = new_user.user_id
    #     user_name = new_user.user_name
    #     is_admin = new_user.is_admin
    #     friends = new_user.friends
    #     fantasy_team_id = new_user.fantasy_team_id
    #     fantast_league_id = new_user.fa
    # )
    # with db.engine.begin() as conn:
    #     addConvoResult = conn.execute(insert_statment)

    #  print(addUserResult)
    return {"Added user to the database!"}


@router.post("/users/{fantasy_league_id}/join", tags=["users"])
def add_user_to_fantasy_league(id: int):
    """
    This endpoint adds a user to a fantasy league
    """
    print("id to join:",id)
    return {"nothering here yet!"}



