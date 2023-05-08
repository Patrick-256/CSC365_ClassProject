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
    #figure out friend id to assign
    lastFriendId_query = sqlalchemy.select(db.friends.c.friendship_id).order_by(sqlalchemy.desc(db.friends.c.friendship_id))

    new_user_id = None
    with db.engine.connect() as conn:
        lastUserId_result = conn.execute(lastFriendId_query)      
        lastUserId = lastUserId_result.fetchone()
        if lastUserId is None:
            new_user_id = 0
        else:
            new_user_id = lastUserId.friendship_id + 1

    #Should probably check the user_id's to make sure they exist and they
    #are not already friends before adding the friendship between them

    insert_statement = """
    INSERT INTO friends (friendship_id,user1_id, user2_id)
    VALUES ({}, {}, {})
    """.format(new_user_id,new_friend.user1_id,new_friend.user2_id)

    with db.engine.begin() as conn:
        addFriendResult = conn.execute(sqlalchemy.text(insert_statement))

        print(addFriendResult)
    return {"Added friend to the database!"}


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
                "friendship_id":row.friendship_id,
                "user1_id":row.user1_id,
                "user2_id":row.user2_id,
                "created_at":row.created_at,
            })
        return res_json