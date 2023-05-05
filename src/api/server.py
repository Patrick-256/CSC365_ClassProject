from fastapi import FastAPI
from src.api import pkg_util

description = """
Movie API returns dialog statistics on top hollywood movies from decades past.

## Characters

You can:
* **list characters with sorting and filtering options.**
* **retrieve a specific character by id**

## Movies

You can:
* **list movies with sorting and filtering options.**
* **retrieve a specific movie by id**
"""
tags_metadata = [
    {
        "name": "users",
        "description": "Access information on characters in movies.",
    },
    {
        "name": "friends",
        "description": "Access information on top-rated movies.",
    },
    {
        "name": "fantasy_league",
        "description": "Access information on lines.",
    },
    {
        "name": "fantasy_team",
        "description": "POST new conversations",
    },
    {
        "name": "player",
        "description": "POST new conversations",
    },
    {
        "name": "game",
        "description": "POST new conversations",
    } 
]

app = FastAPI(
    title="Movie API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Patrick Whitlock",
        "email": "pwhitloc@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(users.router)
app.include_router(players.router)
app.include_router(fantasy_teams.router)
app.include_router(pkg_util.router)



@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API. See /docs for more information."}
