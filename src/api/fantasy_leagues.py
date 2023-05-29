from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
from src.api import datatypes

router = APIRouter()


@router.post("/fantasy_leagues/", tags=["fantasy_leagues"])
def create_fantasy_league(new_fantasy_league: datatypes.fantasy_league):
    """
    Adds a new fantasy league with a specified name
    Minimum league budget is $1,000,000. League budget is set to this value
    if input is less.
    """

    if new_fantasy_league.fantasy_league_budget < 1000000:
        new_fantasy_league.fantasy_league_budget = 1000000

    insert_statement = """
    INSERT INTO fantasy_leagues (fantasy_league_name,fantasy_league_budget)
    VALUES ((:new_name), (:budget))
    returning fantasy_league_id
    """

    params = {
                'new_name':new_fantasy_league.fantasy_league_name,
                'budget':new_fantasy_league.fantasy_league_budget
              }

    with db.engine.begin() as conn:
        try:
            new_league_id = conn.execute(sqlalchemy.text(insert_statement),params).scalar_one()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
    return {"Added fantasy league id {} to the database!".format(new_league_id)}



@router.get("/fantasy_leagues/", tags=["fantasy_leagues"])
def list_fantasy_leagues(fantasy_league_name: str = "",
                         limit: int = Query(50, ge=1, le=250),
                         offset: int = Query(0, ge=0)):
    """
    lists the fantasy leagues from the table
    `fantasy_league_name` - show leagues whose league name matches the given string
    `limit`  - how many leagues to show
    `offset` - how many leagues to skip over

    returns an array of fantasy leagues
    """

    sql = """
    SELECT * 
    FROM fantasy_leagues
    WHERE (:fantasy_league_name = '' OR fantasy_league_name LIKE '%' || :fantasy_league_name || '%')
    OFFSET (:offset)
    LIMIT (:limit)
    """
    params = {
          'fantasy_league_name': fantasy_league_name,
          'limit': limit,
          'offset': offset
        }
    
    with db.engine.connect() as conn:
        try:
            result = conn.execute(sqlalchemy.text(sql),params)
            res_json = []
            for row in result:
                res_json.append({
                    "fantasy_league_id":row.fantasy_league_id,
                    "fantasy_league_name":row.fantasy_league_name,
                    "fantasy_league_budget":row.fantasy_league_budget
                })
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
    
    return res_json


@router.get("/fantasy_leagues/{fantasy_league_id}", tags=["fantasy_leagues"])
def get_top_teams_in_fantasy_league(id: int):
    """
    Lists teams in the specified league in order of total points.
    Total points is calculated based on the following formula:
    total_points = num_goals*5 + num_assists*3 + num_passes*0.05 + num_shots_on_goal*0.2 - num_turnovers*0.2

    returns an array of fantasy leagues
    """


    sql = """SELECT 
                fantasy_teams.fantasy_team_id,
                SUM(games.num_goals * 5 + games.num_assists * 3 + games.num_passes * 0.05 + games.num_shots_on_goal * 0.2 - games.num_turnovers * 0.2) AS total_points
            FROM fantasy_teams
            JOIN player_fantasy_team ON fantasy_teams.fantasy_team_id = player_fantasy_team.fantasy_team_id
            JOIN games ON player_fantasy_team.player_id = games.player_id
            WHERE fantasy_teams.fantasy_league_id = :id
            GROUP BY fantasy_teams.fantasy_team_id
            ORDER BY total_points DESC
            """
    params = {'id': id}

    with db.engine.connect() as conn:
        try:
            result = conn.execute(sqlalchemy.text(sql), params)
            res_json = []
            for row in result:
                res_json.append({
                    "fantasy_team_id": row.fantasy_team_id,
                    "total_points": row.total_points,
                })
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
    
    return res_json