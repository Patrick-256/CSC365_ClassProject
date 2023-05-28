import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np
import random

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://postgres:postgres@localhost:54322/postgres"
    #return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
    
#num_players = 600
num_games = 760
fake = Faker()
#total_players = 0
total_games=0
positions = ['GK','LB','CB','RB','CDM','CM','CAM','ST','CF','LM','RM','LW','RW','LWB','RWB']

with engine.begin() as conn:

    # print("creating fake players...")
    # players = []
    # for i in range(num_players):
    #     if (i % 10 == 0):
    #         print(i)

    #     total_players += 1
    #     players.append({
    #     "player_name": fake.unique.first_name(),
    #     "player_position": random.choice(positions),
    #     "irl_team_name": fake.company_suffix() + " " + fake.city_suffix(),
    #     "player_value": random.randint(1000, 2000000)
    #     })

    # if players:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO players (player_name, player_position, irl_team_name, player_value) 
    #     VALUES (:player_name, :player_position, :irl_team_name, :player_value);
    #     """), players)

    # print("total players: ", total_players)
    
    print("creating fake games...")
    games = []
    gid=0
    for i in range(num_games):
        if (i % 10 == 0):
            print(i)
        gid += 1


        total_games += 1
        games.append({
        "game_id": gid,
        "player_id": random.randint(50,605),
        "num_goals": random.randint(0,4),
        "num_assists": random.randint(0,4),
        "num_passes": random.randint(0,30),
        "num_shots_on_goal": random.randint(0,6),
        "num_turnovers": random.randint(0,5)
        })

    if games:
        conn.execute(sqlalchemy.text("""
        INSERT INTO games (game_id, player_id, num_goals, num_assists, num_passes, num_shots_on_goal, num_turnovers) 
        VALUES (:game_id, :player_id, :num_goals, :num_assists, :num_passes, :num_shots_on_goal, :num_turnovers);
        """), games)

    print("total games: ", total_games)