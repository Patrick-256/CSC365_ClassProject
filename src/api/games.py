from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
router = APIRouter()


@router.post("/games/", tags=["games"])
def add_game(player_id: int, num_goals: int, num_assists: int,
             num_passes: int, num_shots_on_goal: int, num_turnovers: int):
    """"""

    #if player_id not in players edge case check

    if num_goals < 0 or num_goals is None:
          num_goals = 0
    if num_assists < 0 or num_goals is None:
          num_goals = 0
    if num_passes < 0 or num_goals is None:
          num_goals = 0
    if num_shots_on_goal < 0 or num_goals is None:
          num_goals = 0
    if num_turnovers < 0 or num_goals is None:
          num_goals = 0
    
    conn = db.engine.connect()

    max_id = conn.execute(sqlalchemy.select(func.max(db.games.c.game_id))).scalar()
    new_id = (max_id or 0) + 1

    sql = """
          INSERT INTO games (game_id,
                             player_id,
                             num_goals,
                             num_assists,
                             num_passes,
                             num_shots_on_goal,
                             num_turnovers)
          VALUES ("""+new_id+""", """+player_id+""", """+num_goals+""", """+num_assists+""", 
                """+num_passes+""", """+num_shots_on_goal+""", """+num_turnovers+""")
    """

    conn.execute(sqlalchemy.text(sql))

    return new_id
        


@router.get("/games/{game_id}", tags=["games"])
def get_game_info(game_id: int):
    """returns information about the specified game
    """

    conn = db.engine.connect()

   
    sql = """
          select game_id,
                 games.player_id,
                 players.name,
                 num_goals,
                 num_assists,
                 num_passes,
                 num_shots_on_goal,
                 num_turnovers
          from games
          join players where games.player_id = players.player_id
          where games.game_id = """+game_id

    result = conn.execute(sqlalchemy.text(sql))
    player_stats = []

    for row in result:
         ps = {
                 "game_id": row.game_id,
                 "games.player_id": row.player_id,
                 "players.name": row.name,
                 "num_goals": row.num_goals,
                 "num_assists": row.num_assists,
                 "num_passes": row.num_passes,
                 "num_shots_on_goal": row.num_shots_on_goal,
                 "num_turnovers": row.num_turnovers
         }
         player_stats.append(ps)
    
    
    return player_stats