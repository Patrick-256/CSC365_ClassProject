from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db
import sqlalchemy
from sqlalchemy import func
import pydantic.dataclasses

router = APIRouter()

@pydantic.dataclasses.dataclass
class User:
    # user_id: int
    user_name: str
    is_admin: bool
    # fantasy_team_id: int
    # fantast_league_id: int
    
@pydantic.dataclasses.dataclass
class Player:
    player_id: int
    player_name: str
    player_position: str
    irl_team_name: str

@pydantic.dataclasses.dataclass
class Fantasy_Team:
    fantasy_team_id: int
    fantasy_team_name: str
    user_id: int

@pydantic.dataclasses.dataclass
class Friend:
    user1_id: int
    user2_id: int

@pydantic.dataclasses.dataclass
class PlayerTeam:
    player_id: int
    fantasy_team_id: int

@pydantic.dataclasses.dataclass
class Game:
    game_id: int
    player_id: int
    num_goals: int
    num_assists: int
    num_passes: int
    num_shots_on_goal: int
    num_turnovers: int 



@router.post("/games/", tags=["games"])
def add_game(game: Game):
    """"""

    #if player_id not in players edge case check

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
        conn.execute(sqlalchemy.text(sql), params)


    return {"New game added!"}
        


@router.get("/games/{game_id}", tags=["games"])
def get_game_info(game_id: int):
    """returns information about the specified game
    """

    with db.engine.connect() as conn:
   
        sql = """
            select game_id,
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

        result = conn.execute(sqlalchemy.text(sql),
                              {'game_id':game_id})
        player_stats = []

        for row in result:
            ps = {
                    "game_id": row.game_id,
                    "games.player_id": row.player_id,
                    "players.player_name": row.player_name,
                    "num_goals": row.num_goals,
                    "num_assists": row.num_assists,
                    "num_passes": row.num_passes,
                    "num_shots_on_goal": row.num_shots_on_goal,
                    "num_turnovers": row.num_turnovers
            }
            player_stats.append(ps)
        
        
    return player_stats