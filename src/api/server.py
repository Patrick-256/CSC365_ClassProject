from fastapi import FastAPI
from src.api import pkg_util, users,players,fantasy_teams,friends,fantasy_leagues,games

description = """
Fantasy Soccer API allows users to simulate a fantasy soccer league.

## users

You can:
* **Add a new user by providing the user_name and is_admin options.**
* **List existing users**
* **Log in


## players

You can:
* **Edit or add a new player by providing the player name, position, and team.**
* **List existing players**


## fantasy_teams

You can:
* **Add a new team by providing the name and (optional)fantasy league.**
* **Add/remove a player to/from a team**
* **Get the team score
* **Add a team to a league


## games

You can:
* **Add a new game by providing the game_id, player_id, and game statistics.**
* **List existing game stats**


## friends

You can:
* **Create a new friendship between two users.**
* **List existing friendships**


## fantasy_leagues

You can:
* **Create a new league by providing the league name.**
* **List existing leagues**
* **List the top teams by score in a league

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Log in, access information or add users.",
    },
    {
        "name": "friends",
        "description": "Access information or add new friendships",
    },
    {
        "name": "fantasy_leagues",
        "description": "Access information or add new fantasy leagues.",
    },
    {
        "name": "fantasy_teams",
        "description": "Access information or add new fantasy teams.",
    },
    {
        "name": "players",
        "description": "Access information, edit or add new players",
    },
    {
        "name": "games",
        "description": "Access information or add new IRL games (to be used for calculating player stats).",
    } 
]

app = FastAPI(
    title="Fantasy Soccer API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Patrick Whitlock & Ashton Alonge",
        "email": "pwhitloc@calpoly.edu & aalonge@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(fantasy_leagues.router)
app.include_router(fantasy_teams.router)
app.include_router(friends.router)
app.include_router(games.router)
app.include_router(pkg_util.router)
app.include_router(players.router)
app.include_router(users.router)



@app.get("/")
async def root():
    return {"message": "Welcome to the Fantasy Soccer API. See /docs for more information."}
