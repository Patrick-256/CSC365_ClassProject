from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from src import database as db
import sqlalchemy
import pydantic.dataclasses
from sqlalchemy import func
from sqlalchemy import select
import datetime


router = APIRouter()

class Friend:
    user1_id: int
    user2_id: int

@pydantic.dataclasses.dataclass
class User:
    # user_id: int
    user_name: str
    is_admin: bool
    # fantasy_team_id: int
    # fantast_league_id: int
    
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

    #figure out user id to assign
    lastUserId_query = sqlalchemy.select(db.users.c.user_id,db.users.c.user_name,db.users.c.is_admin,db.users.c.created_at).order_by(sqlalchemy.desc(db.users.c.user_id))

    new_user_id = None

    with db.engine.connect() as conn:
        lastUserId_result = conn.execute(lastUserId_query)
        
        lastUserId = lastUserId_result.fetchone()

        print("last user_id is:")
        print(lastUserId.user_id)
        print(lastUserId.user_name)
        print(lastUserId.is_admin)
        print(lastUserId.created_at)

        new_user_id = lastUserId.user_id + 1

        
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    insert_statement = """
    INSERT INTO users (user_id, user_name, is_admin, created_at)
    VALUES ({}, '{}', {}, '{}')
    """.format(new_user_id,new_user.user_name,new_user.is_admin,now_str)

    with db.engine.begin() as conn:
        addUserResult = conn.execute(sqlalchemy.text(insert_statement))

        print(addUserResult)
    return {"Added user to the database!"}


@router.post("/users/{fantasy_league_id}/join", tags=["users"])
def add_user_to_fantasy_league(id: int):
    """
    This endpoint adds a user to a fantasy league
    """
    print("id to join:",id)
    return {"nothering here yet!"}

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


