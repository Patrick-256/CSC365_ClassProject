from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from src import database as db
import sqlalchemy
import pydantic.dataclasses
from sqlalchemy import func
from sqlalchemy import select


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

@router.post("/users/", tags=["users"])
def add_user(new_user: User):
    """
    This endpoint adds a user to the database
    """

    insert_statement = """
    INSERT INTO users (user_name, is_admin)
    VALUES ((:user_name), (:is_admin))
    """
    params = {'user_name':new_user.user_name,'is_admin':new_user.is_admin}

    with db.engine.begin() as conn:
        addUserResult = conn.execute(sqlalchemy.text(insert_statement),params)

        print(addUserResult)
    return {"Added user to the database!"}



@router.get("/users/",tags=["users"])
def list_users():
    """
    At the moment, this endpoint just lists to first 10 users in the table
    """

    users_query = """
    SELECT *
    FROM users
    LIMIT 10
    """
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(users_query))
        res_json = []
        for row in result:
            res_json.append({
                "user_id":row.user_id,
                "user_name":row.user_name,
                "is_admin":row.is_admin,
                "created_at":row.created_at,
            })
        return res_json


