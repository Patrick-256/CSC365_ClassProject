from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from src import database as db
import sqlalchemy
from src.api import datatypes
from sqlalchemy import func
import hashlib

router = APIRouter()


@router.post("/users/", tags=["users"])
def add_user(new_user: datatypes.User):
    """
    This endpoint adds a user to the database
    `user_name`: desired username (must be unique)
    `is_admin`: wether this user is admin or not
    `password`: password

    returns the id of the user created
    """

    check_user_exists = """
                select user_name from users
                where user_name = (:username)
                """
    with db.engine.begin() as conn:   
        user_exists = conn.execute(sqlalchemy.text(check_user_exists),{"username":new_user.user_name}).fetchone()

        if user_exists is not None:
            raise HTTPException(422, "user_name already exists.")

        insert_statement = """
        INSERT INTO users (user_name, is_admin, password)
        VALUES ((:user_name), (:is_admin), (:password))
        returning user_id
        """
        params = {'user_name':new_user.user_name,
                'is_admin':new_user.is_admin,
                'password': hash_password(new_user.password)
                }

        try:
            new_user_id = conn.execute(sqlalchemy.text(insert_statement),params).scalar_one()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
    return {"Added user id {} to the database!".format(new_user_id)}



@router.get("/users/",tags=["users"])
def list_users(user_name: str = "",
               limit: int = Query(50, ge=1, le=250),
               offset: int = Query(0, ge=0)):
    """
    Lists users from the database
    `user_name` - show users whose user_name matches the given string
    `limit`  - how many users to show
    `offset` - how many users to skip over

    returns a list of users
    """

    users_query = """
    SELECT *
    FROM users
    WHERE (:user_name = '' OR user_name LIKE '%' || :user_name || '%')
    OFFSET (:offset)
    LIMIT (:limit)
    """
    params = {
          'user_name': user_name,
          'limit': limit,
          'offset': offset
        }
    
    with db.engine.connect() as conn:
        res_json = []
        try:
            result = conn.execute(sqlalchemy.text(users_query),params).fetchall()

            if result is None:
                raise HTTPException(422, "No users found.")
            
            for row in result:
                res_json.append({
                    "user_id":row.user_id,
                    "user_name":row.user_name,
                    "is_admin":row.is_admin,
                    "created_at":row.created_at,
                })
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
        return res_json
    

@router.post("/users/login",tags=["users"])
def login(userLogin:datatypes.UserLogin):
    """
    authorizes a user by username and password

    returns login successful or login failed depending on if password matches
    """

    sql = """
        select password
        from users
        where user_name = (:username)
    """

    with db.engine.connect() as conn:

        user_subq = """
            select user_name from users
            where user_name = (:username)
            """
        
        user_result = conn.execute(sqlalchemy.text(user_subq),{"username":userLogin.user_name}).fetchone()

        if user_result is None:
            raise HTTPException(422, "User not found.")

        pwd = conn.execute(sqlalchemy.text(sql), {'username': userLogin.user_name}).scalar_one()

    if hash_password(userLogin.password) == pwd:

        return {"Login successful."}
    
    return {"Login failed."}


def hash_password(pwd: str):
    hash_object = hashlib.sha256()

    hash_object.update(pwd.encode('utf-8'))

    hashed_password = hash_object.hexdigest()

    return hashed_password

