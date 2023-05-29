import pydantic.dataclasses

@pydantic.dataclasses.dataclass
class User:
    user_name: str
    is_admin: bool
    password: str

@pydantic.dataclasses.dataclass
class UserLogin:
    user_name: str
    password: str
    
@pydantic.dataclasses.dataclass
class Player:
    player_id: int
    player_name: str
    player_position: str
    irl_team_name: str
    player_value: int

@pydantic.dataclasses.dataclass
class Fantasy_Team:
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

@pydantic.dataclasses.dataclass
class fantasy_league:
    fantasy_league_name: str
    fantasy_league_budget: int

