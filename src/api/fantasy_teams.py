from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
from src.api import datatypes

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation


router = APIRouter()


@router.post("/fantasy_teams/", tags=["fantasy_teams"])
def create_fantasy_team(team: datatypes.Fantasy_Team):
    """
    Adds a new fantasy team with the
    specified name and user id. If no league id is provided,
    the league id will be set to null
    """
    
    with db.engine.begin() as conn:

        
        league_subq = """
            Select (:league) from fantasy_leagues
        """
        league_result = conn.execute(sqlalchemy.text(league_subq),{"league":team.fantasy_league_id})

        if league_result is None:
            team.fantasy_league_id = None

        sql = """
            INSERT INTO fantasy_teams (fantasy_team_name, user_id, fantasy_league_id, fantasy_team_balance)
            VALUES ((:name),(:user_id), (:fantasy_league_id), 10000000)
            returning fantasy_team_id"""
        
        params = {
                  'name': team.fantasy_team_name, 
                  'user_id': team.user_id,
                  'fantasy_league_id': team.fantasy_league_id
                  }

        try:
            new_team_id = conn.execute(sqlalchemy.text(sql),params).scalar_one()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)


    return {"Team {} added".format(new_team_id)}
    

@router.post("/fantasy_teams/players", tags=["fantasy_teams"])
def add_player_to_fantasy_team(player_team: datatypes.PlayerTeam):
    """
    adds a player to the specified fantasy team
    """

    with db.engine.begin() as conn:
    
        bal_subq = """
                select fantasy_team_balance
                from fantasy_teams
                where fantasy_teams.fantasy_team_id = (:id)
                for share
                """
        val_subq = """
                select player_value
                from players
                where players.player_id = (:p_id)
                for share
                """
        
        sql = """
            INSERT INTO player_fantasy_team (player_id, fantasy_team_id)
            VALUES ((:player_id),(:fantasy_team_id))
            """
        
        params = {'player_id':player_team.player_id, 'fantasy_team_id':player_team.fantasy_team_id}

        try:
            balance = conn.execute(sqlalchemy.text(bal_subq),{'id':player_team.fantasy_team_id}).scalar_one()
            value = conn.execute(sqlalchemy.text(val_subq),{'p_id':player_team.player_id}).scalar_one()
            if balance < value:
                raise HTTPException(422, "Team balance is too low.")
            conn.execute(sqlalchemy.text(sql),params)
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)

    return {"Added player {} to team {}".format(player_team.player_id, player_team.fantasy_team_id)}


@router.delete("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def remove_player_from_fantasy_team(player_team: datatypes.PlayerTeam):
    """
    removes a player from the specified fantasy team
    """

    with db.engine.begin() as conn:

        sql = """
            delete from player_fantasy_team
            where player_id = (:player_id) and fantasy_team_id = (:fantasy_team_id)
            """
        
        params = {
                'player_id': player_team.player_id, 
                'fantasy_team_id': player_team.fantasy_team_id
                  }

        try:
            conn.execute(sqlalchemy.text(sql),params)
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)

    return {"Removed player {} from team {}".format(player_team.player_id, player_team.fantasy_team_id)}



@router.get("/fantasy_teams/{fantasy_team_id}/score", tags=["fantasy_teams"])
def get_fantasy_team_score(fantasy_team_id: int):
    """
    return the score of the specified fantasy team,
    which is a sum of the team's player scores
    """
    
    with db.engine.connect() as conn:
        
        team_has_players = """
            select fantasy_team_id from player_fantasy_team
            where fantasy_team_id = (:id)
        """
        thp_result = conn.execute(sqlalchemy.text(team_has_players),{"id": fantasy_team_id}).fetchone()

        if thp_result is None:
            return {
                "team_id": fantasy_team_id,
                "Total_score": 0
        }

        sql = """
            SELECT player_fantasy_team.fantasy_team_id, SUM(player_score) AS total_team_score
            FROM (
            SELECT player_fantasy_team.player_id, SUM(num_goals*5 + num_assists*3 + num_passes*0.05 + num_shots_on_goal*0.2 - num_turnovers*0.2) AS player_score
            FROM player_fantasy_team
            JOIN games ON games.player_id = player_fantasy_team.player_id
            WHERE player_fantasy_team.fantasy_team_id = (:fantasy_team_id)
            GROUP BY player_fantasy_team.player_id
            ) AS subquery
            JOIN player_fantasy_team ON player_fantasy_team.player_id = subquery.player_id
            GROUP BY player_fantasy_team.fantasy_team_id
            """

        try:
            result = conn.execute(sqlalchemy.text(sql),{'fantasy_team_id':fantasy_team_id}).fetchone()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
        if result is None:
            raise HTTPException(422, "Fantasy team not found.")

    return {
        "team_id": fantasy_team_id,
        "Total_score": result[1]
    }
    


@router.put("/fantasy_teams/{fantasy_league_id}/join", tags=["fantasy_teams"])
def add_team_to_fantasy_league(team_id: int, league_id: int):
    """
    This endpoint adds a user to a fantasy league
    It updates the league_id column of a team
    """

    with db.engine.begin() as conn:

        team_subq = """
            select fantasy_team_id from fantasy_teams
            where fantasy_team_id = (:fantasy_team_id)
            """
        
        team_result = conn.execute(sqlalchemy.text(team_subq),{"fantasy_team_id":team_id}).fetchone()

        if team_result is None:
            raise HTTPException(422, "Team not found.")

        sql = """
            update fantasy_teams
            set fantasy_league_id = (:league_id)
            where fantasy_team_id = (:team_id)
            """
        
        params = {'league_id': league_id, 'team_id': team_id}
            

        try:
            conn.execute(sqlalchemy.text(sql),params)
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)

    return ("Team {} addded to fantasy league {}".format(team_id, league_id))
