from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from src.api import datatypes

router = APIRouter()


@router.post("/friends/", tags=["friends"])
def add_friend(new_friendship: datatypes.Friend):
    """
    adds a friendship between two user ids
    """

    #check that the user ids are not the same
    if new_friendship.user1_id == new_friendship.user2_id:
        raise HTTPException(423, "A user cannot be friends with themself!")
    
    #Check the user_id's to make sure they exist in the users table
    params = {'user1_id':new_friendship.user1_id,'user2_id':new_friendship.user2_id}

    user1_query_statement = """
    SELECT *
    FROM users
    WHERE user_id = (:user1_id)
    """
    with db.engine.begin() as conn:
        friendship_result = conn.execute(sqlalchemy.text(user1_query_statement),params).fetchone()
        if friendship_result == None:
            raise HTTPException(423, "User_id1 {} does not exist in users table!".format(new_friendship.user1_id))

    user2_query_statement = """
    SELECT *
    FROM users
    WHERE user_id = (:user2_id)
    """
    with db.engine.begin() as conn:
        friendship_result = conn.execute(sqlalchemy.text(user2_query_statement),params).fetchone()
        if friendship_result == None:
            raise HTTPException(423, "User_id2 {} does not exist in users table!".format(new_friendship.user2_id))

    #check that they are not already friends before adding the friendship between them
    query_statement = """
    SELECT *
    FROM friends
    WHERE (user1_id = (:user1_id) AND user2_id = (:user2_id)) OR
          (user2_id = (:user1_id) AND user1_id = (:user2_id))
    """
    with db.engine.begin() as conn:
        friendship_result = conn.execute(sqlalchemy.text(query_statement),params).fetchone()
        if friendship_result != None:
            raise HTTPException(423, "Friendship already exists.")

    insert_statement = """
    INSERT INTO friends (user1_id, user2_id)
    VALUES ((:user1_id), (:user2_id))
    """

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text(insert_statement),params)

    return {"Added friendship {}, {} to the database!".format(new_friendship.user1_id,new_friendship.user2_id)}


@router.get("/friends/",tags=["friends"])
def list_friends(
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
):
    """
    At the moment, this endpoint just lists to first 10 friendships in the table
    `limit`  - how many users to show
    `offset` - how many users to skip over
    """

    friends_query = """
    SELECT *
    FROM friends
    OFFSET (:offset)
    LIMIT (:limit)
    """
    params = {
          'limit': limit,
          'offset': offset
        }

    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(friends_query),params)
        res_json = []
        for row in result:
            res_json.append({
                "user1_id":row.user1_id,
                "user2_id":row.user2_id,
                "created_at":row.created_at,
            })
        return res_json