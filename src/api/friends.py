from fastapi import APIRouter, HTTPException
from typing import Optional
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
    adds a friendship between two user ids.
    user ids must exist in the Users table and there must not 
    be an existing friendship between them.

    returns the user id's if successful
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
        try:
            friendship_result = conn.execute(sqlalchemy.text(user1_query_statement),params).fetchone()
            if friendship_result == None:
                raise HTTPException(423, "User_id1 {} does not exist in users table!".format(new_friendship.user1_id))

            user2_query_statement = """
            SELECT *
            FROM users
            WHERE user_id = (:user2_id)
            """
        
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

            friendship_result = conn.execute(sqlalchemy.text(query_statement),params).fetchone()
            if friendship_result != None:
                raise HTTPException(423, "Friendship already exists.")

            insert_statement = """
            INSERT INTO friends (user1_id, user2_id)
            VALUES ((:user1_id), (:user2_id))
            """

            conn.execute(sqlalchemy.text(insert_statement),params)
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)

    return {"Added friendship {}, {} to the database!".format(new_friendship.user1_id,new_friendship.user2_id)}


@router.get("/friends/",tags=["friends"])
def list_friends(user_id: Optional[int] = Query(None),
                 limit: int = Query(50, ge=1, le=250),
                 offset: int = Query(0, ge=0)):
    """
    Lists out existing friendships between user ids.
    `user_id` - show the friendships this user_id is a part of.
    `limit`  - how many users to show
    `offset` - how many users to skip over

    returns a list of friendships represented as:
    user1_id,user2_id where each user id are friends with each other
    """

    friends_query = """
    SELECT *
    FROM friends
    WHERE (:user_id IS NULL OR user1_id = (:user_id) OR user2_id = (:user_id))
    OFFSET (:offset)
    LIMIT (:limit)
    """
    params = {
          'user_id': user_id,
          'limit': limit,
          'offset': offset
        }

    with db.engine.connect() as conn:
        res_json = []
        try:
            result = conn.execute(sqlalchemy.text(friends_query),params)
            
            for row in result:
                res_json.append({
                    "user1_id":row.user1_id,
                    "user2_id":row.user2_id,
                    "created_at":row.created_at,
                })
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
        return res_json