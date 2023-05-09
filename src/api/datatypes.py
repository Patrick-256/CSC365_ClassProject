import pydantic.dataclasses

@pydantic.dataclasses.dataclass
class User:
    # user_id: int
    user_name: str
    is_admin: bool
    # fantasy_team_id: int
    # fantast_league_id: int
    
class Player:
    player_id: int
    player_name: str
    player_position: str
    irl_team_name: str

class Fantasy_Team:
    fantasy_team_id: int
    fantasy_team_name: str
    fantasy_league_id: int

class Friend:
    user1_id: int
    user2_id: int
