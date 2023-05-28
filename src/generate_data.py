import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np
import random
import hashlib

def hash_password(pwd: str):
    hash_object = hashlib.sha256()

    hash_object.update(pwd.encode('utf-8'))

    hashed_password = hash_object.hexdigest()

    return hashed_password


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

fake = Faker()

num_players = 600
num_games = 760
num_leagues = 10000
num_users = 450000
num_teams = 540000
num_player_fantasy_teams = 540000

total_players = 0
total_games=0
total_leauges = 0
total_users = 0
total_teams = 0
total_player_fantasy_teams = 0

positions = ['GK','LB','CB','RB','CDM','CM','CAM','ST','CF','LM','RM','LW','RW','LWB','RWB']

with engine.begin() as conn:

    #-----------------PLAYERS----------------------------------


    print("creating fake players...")
    players = []
    for i in range(num_players):
        if (i % 10 == 0):
            print(i)

        total_players += 1
        players.append({
        "player_name": fake.unique.first_name(),
        "player_position": random.choice(positions),
        "irl_team_name": fake.company_suffix() + " " + fake.city_suffix(),
        "player_value": random.randint(1000, 2000000)
        })

    if players:
        conn.execute(sqlalchemy.text("""
        INSERT INTO players (player_name, player_position, irl_team_name, player_value) 
        VALUES (:player_name, :player_position, :irl_team_name, :player_value);
        """), players)

    print("total players: ", total_players)


    #-----------------GAMES----------------------------------
    

    # print("creating fake games...")
    # games = []
    # gid=0
    # for i in range(num_games):
    #     if (i % 10 == 0):
    #         print(i)
    #     gid += 1


    #     total_games += 1
    #     games.append({
    #     "game_id": gid,
    #     "player_id": random.randint(50,605),
    #     "num_goals": random.randint(0,4),
    #     "num_assists": random.randint(0,4),
    #     "num_passes": random.randint(0,30),
    #     "num_shots_on_goal": random.randint(0,6),
    #     "num_turnovers": random.randint(0,5)
    #     })

    # if games:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO games (game_id, player_id, num_goals, num_assists, num_passes, num_shots_on_goal, num_turnovers) 
    #     VALUES (:game_id, :player_id, :num_goals, :num_assists, :num_passes, :num_shots_on_goal, :num_turnovers);
    #     """), games)

    # print("total games: ", total_games)

    
    #-----------------LEAGUES----------------------------------


    # print("creating fake leagues...")
    # leagues = []
    # for i in range(num_leagues):
    #     if (i % 10 == 0):
    #         print(i)

    #     total_leauges += 1
    #     leagues.append({
    #     "fantasy_league_name": fake.first_name()+"\'s fantasy league",
    #     "fantasy_league_budget": round(random.randint(100000,10000000),-3)
    #     })

    # if leagues:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO fantasy_leagues (fantasy_league_name, fantasy_league_budget)
    #     VALUES (:fantasy_league_name, :fantasy_league_budget);
    #     """), leagues)

    # print("total leagues: ", total_leauges)


    #-----------------USERS----------------------------------


    # print("creating fake users...")
    # users = []
    # for i in range(num_users):
    #     if (i % 10 == 0):
    #         print(i)

    #     total_users += 1
    #     users.append({
    #     "user_name": fake.user_name(),
    #     "is_admin": False,
    #     "password": hash_password(fake.password())
    #     })

    # if users:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO users (user_name, is_admin, password)
    #     VALUES (:user_name, :is_admin, :password);
    #     """), users)

    # print("total users: ", total_users)


    #-----------------TEAMS----------------------------------


    # print("creating fake teams...")
    # teams = []
    # for i in range(num_teams):
    #     if (i % 100 == 0):
    #         print(i)

    #     total_teams += 1
    #     teams.append({
    #     "fantasy_team_name": fake.first_name()+"\'s fantasy team",
    #     "user_id": random.randint(1,450000),
    #     "fantasy_league_id": random.randint(1,10000),
    #     "fantasy_team_balance": 10000000
    #     })

    # if teams:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO fantasy_teams (fantasy_team_name, user_id, fantasy_league_id, fantasy_team_balance)
    #     VALUES (:fantasy_team_name, :user_id, :fantasy_league_id, :fantasy_team_balance);
    #     """), teams)

    # print("total teams: ", total_teams)


    #-----------------PLAYER_FANTASY_TEAM----------------------------------


    # print("creating fake player_fantasy_teams...")
    # player_fantasy_teams = []
    # for i in range(2194,num_player_fantasy_teams):
    #     if (i % 100 == 0):
    #         print(i)

    #     total_player_fantasy_teams += 1
    #     player_fantasy_teams.append({
    #     "player_id": random.randint(2,605),
    #     "fantasy_team_id": i
    #     })

    # if player_fantasy_teams:
    #     conn.execute(sqlalchemy.text("""
    #     INSERT INTO player_fantasy_team (player_id, fantasy_team_id)
    #     VALUES (:player_id, :fantasy_team_id);
    #     """), player_fantasy_teams)

    # print("total player_fantasy_teams: ", total_player_fantasy_teams)