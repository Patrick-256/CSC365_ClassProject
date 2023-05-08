from fastapi import FastAPI
from src.api import pkg_util, users,players,fantasy_teams,friends,fantasy_leagues,games

description = """
Fantasy Soccer API allows users to simulate a fantasy soccer league.

## users

You can:
* **Add a new user by providing the user_name and is_admin options.**
* **list existing users**

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Access information or add users.",
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
        "name": "Patrick Whitlock and Ashton Alonge",
        "email": "pwhitloc@calpoly.edu and aalonge@calpoly.edu",
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
