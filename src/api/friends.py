from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
router = APIRouter()


@router.post("/friends/{user_id}{friend_id}/friends", tags=["users"])
def add_friend(user_id: int, friend_id: int):
    """adds a friend to the users friends
    """

    conn = db.engine.connect()


    sql = """
          INSERT INTO friends (user_id, friend_id)
          VALUES ("""+user_id+""", """+friend_id+""")
    """

    conn.execute(sqlalchemy.text(sql))

    return (user_id, friend_id)