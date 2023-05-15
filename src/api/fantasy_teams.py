from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
from src.api import datatypes

router = APIRouter()


@router.post("/fantasy_teams/", tags=["fantasy_teams"])
def create_fantasy_team(team: datatypes.Fantasy_Team):
    """Adds a new fantasy team with the
       specified user id
       """
    
    with db.engine.begin() as conn:

        id_subq = """
            Select user_id from users
        """
        ids = []
        id_result = conn.execute(sqlalchemy.text(id_subq))
        for row in id_result:
           ids.append(row.user_id)

        if team.user_id not in ids:
           raise HTTPException(422, "User ID not found.")
        

        league_subq = """
            Select fantasy_league_id from fantasy_leagues
        """
        leagues = []
        league_result = conn.execute(sqlalchemy.text(league_subq))
        for row in league_result:
           leagues.append(row.fantasy_league_id)

        if team.fantasy_league_id not in leagues:
            team.fantasy_league_id = None

        sql = """
            INSERT INTO fantasy_teams (fantasy_team_name, user_id)
            VALUES ((:name),(:user_id))"""
        
        params = {
                  'name': team.fantasy_team_name, 
                  'user_id': team.user_id,
                  'fantasy_league_id': team.fantasy_league_id
                  }

        new_team_id = conn.execute(sqlalchemy.text(sql),params)


    return {"Team {} added".format(new_team_id.fantasy_team_id)}
    

@router.post("/fantasy_teams/players", tags=["fantasy_teams"])
def add_player_to_fantasy_team(player_team: datatypes.PlayerTeam):
    """adds a player to the specified fantasy team
    """

    with db.engine.begin() as conn:

        id_subq = """
            Select player_id from players
        """
        ids = []
        id_result = conn.execute(sqlalchemy.text(id_subq))
        for row in id_result:
           ids.append(row.player_id)

        if player_team.player_id not in ids:
            raise HTTPException(422, "Player ID not found.")
        

        team_subq = """
            Select fantasy_team_id from fantasy_teams
        """
        teams = []
        team_result = conn.execute(sqlalchemy.text(team_subq))
        for row in team_result:
           teams.append(row.fantasy_team_id)

        if player_team.fantasy_team_id not in teams:
            raise HTTPException(422, "Team ID not found.")

        sql = """
            INSERT INTO player_fantasy_team (player_id, fantasy_team_id)
            VALUES ((:player_id),(:fantasy_team_id))"""
        
        params = {'player_id':player_team.player_id, 'fantasy_team_id':player_team.fantasy_team_id}

        conn.execute(sqlalchemy.text(sql),params)

    return {"Added player {} to team {}".format(player_team.player_id, player_team.fantasy_team_id)}


@router.delete("/fantasy_teams/{fantasy_team_id}/players", tags=["fantasy_teams"])
def remove_player_from_fantasy_team(player_team: datatypes.PlayerTeam):
    """removes a player from the specified fantasy team
    """

    with db.engine.begin() as conn:


        id_subq = """
            Select player_id from players
        """
        ids = []
        id_result = conn.execute(sqlalchemy.text(id_subq))
        for row in id_result:
           ids.append(row.player_id)

        if player_team.player_id not in ids:
            raise HTTPException(422, "Player ID not found.")
        

        team_subq = """
            Select fantasy_team_id from fantasy_teams
        """
        teams = []
        team_result = conn.execute(sqlalchemy.text(team_subq))
        for row in team_result:
           teams.append(row.fantasy_team_id)

        if player_team.fantasy_team_id not in teams:
            raise HTTPException(422, "Team ID not found.")
        

        sql = """
            delete from player_fantasy_team
            where player_id = (:player_id) and fantasy_team_id = (:fantasy_team_id)
            """
        
        params = {
                'player_id': player_team.player_id, 
                'fantasy_team_id': player_team.fantasy_team_id
                  }

        conn.execute(sqlalchemy.text(sql),params)

    return {"Removed player {} from team {}".format(player_team.player_id, player_team.fantasy_team_id)}



@router.get("/fantasy_teams/{fantasy_team_id}/score", tags=["fantasy_teams"])
def get_fantasy_team_score(fantasy_team_id: int):
    """return the score of the specified fantasy team,
       which is a sum of the team's player scores"""
    
    with db.engine.connect() as conn:
        
        team_subq = """
            Select fantasy_team_id from fantasy_teams
        """
        teams = []
        team_result = conn.execute(sqlalchemy.text(team_subq))
        for row in team_result:
           teams.append(row.fantasy_team_id)

        if fantasy_team_id not in teams:
            raise HTTPException(422, "Team ID not found.")

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

        result = conn.execute(sqlalchemy.text(sql),{'fantasy_team_id':fantasy_team_id}).fetchone()

    return {
        "team_id": fantasy_team_id,
        "Total_score": result.total_team_score
    }
    


@router.put("/fantasy_teams/{fantasy_league_id}/join", tags=["fantasy_teams"])
def add_team_to_fantasy_league(team_id: int, league_id: int):
    """
    This endpoint adds a user to a fantasy league
    It sets the league_id column of a team
    """

    with db.engine.begin() as conn:

        team_subq = """
            Select fantasy_team_id from fantasy_teams
        """
        teams = []
        team_result = conn.execute(sqlalchemy.text(team_subq))
        for row in team_result:
           teams.append(row.fantasy_team_id)

        if team_id not in teams:
            raise HTTPException(422, "Team ID not found.")
        
        league_subq = """
            Select fantasy_league_id from fantasy_leagues
        """
        leagues = []
        league_result = conn.execute(sqlalchemy.text(league_subq))
        for row in league_result:
           leagues.append(row.fantasy_league_id)

        if league_id not in leagues:
            raise HTTPException(422, "League ID not found.")

        sql = """
            update fantasy_teams
            set fantasy_league_id = (:league_id)
            where fantasy_team_id = (:team_id)
            """
        
        params = {'league_id': league_id, 'team_id': team_id}
            

        conn.execute(sqlalchemy.text(sql),params)

    return ("Team {} addded to fantasy league {}".format(team_id, league_id))
