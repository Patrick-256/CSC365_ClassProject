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


