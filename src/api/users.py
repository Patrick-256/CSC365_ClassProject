from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from src import database as db
import sqlalchemy
from src.api import datatypes
from sqlalchemy import func
from sqlalchemy import select


router = APIRouter()


@router.post("/users/", tags=["users"])
def add_user(new_user: datatypes.User):
    """
    This endpoint adds a user to the database
    """

    insert_statement = """
    INSERT INTO users (user_name, is_admin)
    VALUES ((:user_name), (:is_admin))
    """
    params = {'user_name':new_user.user_name,'is_admin':new_user.is_admin}

    with db.engine.begin() as conn:
        new_user_id = conn.execute(sqlalchemy.text(insert_statement),params)

    return {"Added user {} to the database!".format(new_user_id.user_id)}



@router.get("/users/",tags=["users"])
def list_users(
    user_name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
):
    """
    Lists users from the database
    `user_name` - show users whose user_name matches the given string
    `limit`  - how many users to show
    `offset` - how many users to skip over
    """

    users_query = """
    SELECT *
    FROM users
    WHERE user_name LIKE '%(:user_name)%'
    OFFSET (:offset)
    LIMIT (:limit)
    """
    params = {
          'user_name': user_name,
          'limit': limit,
          'offset': offset
        }
    
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(users_query),params)
        res_json = []
        for row in result:
            res_json.append({
                "user_id":row.user_id,
                "user_name":row.user_name,
                "is_admin":row.is_admin,
                "created_at":row.created_at,
            })
        return res_json


