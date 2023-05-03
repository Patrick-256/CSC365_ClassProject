from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


print(database_connection_url())
# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url())

# Create a single connection to the database. Later we will discuss pooling connections.
conn = engine.connect()

from sqlalchemy import MetaData, Table, Column, Integer, String, Float

# metadata = MetaData()

metadata_obj = sqlalchemy.MetaData()
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
fantasy_leagues = sqlalchemy.Table("fantasy_leagues", metadata_obj, autoload_with=engine)
friends = sqlalchemy.Table("friends", metadata_obj, autoload_with=engine)
fantasy_teams = sqlalchemy.Table("fantasy_teams", metadata_obj, autoload_with=engine)
players = sqlalchemy.Table("players", metadata_obj, autoload_with=engine)
games = sqlalchemy.Table("games", metadata_obj, autoload_with=engine)



db = {
    "users": users,
    "fantasy_leagues":fantasy_leagues,
    "friends":friends,
    "fantasy_teams":fantasy_teams,
    "players": players,
    "games": games
}