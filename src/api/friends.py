from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from src.api import datatypes

router = APIRouter()


@router.post("/friends/", tags=["users"])
def add_friend(new_friendship: datatypes.Friend):
    """
    adds a friendship between two user ids
    """
    #Should probably check the user_id's to make sure they exist and they
    #are not already friends before adding the friendship between them

    insert_statement = """
    INSERT INTO friends (user1_id, user2_id)
    VALUES ((:user1_id), (:user2_id))
    """

    params = {'user1_id':new_friendship.user1_id,'user2_id':new_friendship.user2_id}

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text(insert_statement),params)

    return {"Added friendship {}, {} to the database!".format(new_friendship.user1_id,new_friendship.user2_id)}


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