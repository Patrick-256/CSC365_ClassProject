from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
import pydantic.dataclasses

router = APIRouter()

@pydantic.dataclasses.dataclass
class Friend:
    user1_id: int
    user2_id: int

@router.post("/friends/", tags=["users"])
def add_friend(new_friend: Friend):
    """adds a friend to the users friends
    """
    #Should probably check the user_id's to make sure they exist and they
    #are not already friends before adding the friendship between them

    insert_statement = """
    INSERT INTO friends (user1_id, user2_id)
    VALUES ({}, {})
    """.format(new_friend.user1_id,new_friend.user2_id)

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text(insert_statement))

    return {"Added friendship to the database!"}


@router.get("/friends/",tags=["users"])
def list_users():
    """
    At the moment, this endpoint just lists to first 10 friendships in the table
    """

    friends_query = """
    SELECT *
    FROM friends
    LIMIT 10
    """

    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(friends_query))
        res_json = []
        for row in result:
            res_json.append({
                "user1_id":row.user1_id,
                "user2_id":row.user2_id,
                "created_at":row.created_at,
            })
        return res_json