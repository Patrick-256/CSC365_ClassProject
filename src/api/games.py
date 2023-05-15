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


@router.post("/games/", tags=["games"])
def add_game(game: datatypes.Game):
    """"""

    if game.num_goals < 0 or game.num_goals is None:
          game.num_goals = 0
    if game.num_assists < 0 or game.num_assists is None:
          game.num_assists = 0
    if game.num_passes < 0 or game.num_passes is None:
          game.num_passes = 0
    if game.num_shots_on_goal < 0 or game.num_shots_on_goal is None:
          game.num_shots_on_goal = 0
    if game.num_turnovers < 0 or game.num_turnovers is None:
          game.num_turnovers = 0
    
    with db.engine.begin() as conn:

        player_subq = """
            select player_id from players
            where player_id = (:player_id)
            """
        
        player_result = conn.execute(sqlalchemy.text(player_subq),{"player_id":game.player_id}).fetchone()

        if player_result is None:
            raise HTTPException(422, "Player not found.")
        
        sql = """
            INSERT INTO games (
                                game_id,
                                player_id,
                                num_goals,
                                num_assists,
                                num_passes,
                                num_shots_on_goal,
                                num_turnovers)
            VALUES (:game_id, :player_id, :num_goals, :num_assists, :num_passes, :num_shots_on_goal, :num_turnovers)
            returning game_id
        """
        
        params = {
            'game_id': game.game_id,
            'player_id': game.player_id,
            'num_goals': game.num_goals,
            'num_assists': game.num_assists,
            'num_passes': game.num_passes,
            'num_shots_on_goal': game.num_shots_on_goal,
            'num_turnovers': game.num_turnovers
        }

        try:
            new_game_id = conn.execute(sqlalchemy.text(sql), params).scalar_one()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)


    return {"Game {} added!".format(new_game_id)}
        


@router.get("/games/{game_id}", tags=["games"])
def get_game_info(game_id: int):
    """returns information about the specified game
    """

    with db.engine.connect() as conn:
   
        sql = """
            select  game_id,
                    games.player_id,
                    players.player_name,
                    num_goals,
                    num_assists,
                    num_passes,
                    num_shots_on_goal,
                    num_turnovers
            from games
            join players on games.player_id = players.player_id
            where games.game_id = (:game_id)"""

        try:
            result = conn.execute(sqlalchemy.text(sql),{'game_id':game_id}).fetchall()
        except sqlalchemy.exc.IntegrityError as e:
            error_msg = e.orig.diag.message_detail
            raise HTTPException(422, error_msg)
        
        if result is None:
             raise HTTPException(422, "Game not found.")
        
        player_stats = []

        for row in result:
            ps = {
                    "game_id": row.game_id,
                    "player_id": row.player_id,
                    "player_name": row.player_name,
                    "num_goals": row.num_goals,
                    "num_assists": row.num_assists,
                    "num_passes": row.num_passes,
                    "num_shots_on_goal": row.num_shots_on_goal,
                    "num_turnovers": row.num_turnovers
            }
            player_stats.append(ps)
        
        
    return player_stats