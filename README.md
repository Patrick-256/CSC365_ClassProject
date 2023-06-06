# Fantasy Soccer API

Welcome to our Fantasy Soccer API! Check out the features below to get started!

## Table of Contents
- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Resources](#resources)
- [Credits](#credits)

## About

Fantasy Soccer API makes it possible for a user to create fantasy teams, and choose real players to add to their team. Users can also create leagues, where multiple teams can compete with each other as they are ranked by the real life performances of their players. 

As real-life games happen, administrators can add games to the database, where the statistics of each player from the game will be recorded. This data is used to score each player, where statistics such as goals and assists will increase the points of a player, and statistics such as turnovers will decrease their points. The player score will be used to calculate the total score of all fantasy teams that have that player.

Users can create an account, add friends, manage multiple fantasy teams, and create and join leagues. All players have specific values associated with them, where better players are more expensive. Each fantasy team is given a budget to purchase players, so users must be strategic about their spendings. Additionally, when creating fantasy leagues, users can set the maximum budget of the league, where every team in the league cannot surpass that amount.


## Installation

To install the required resources to contribute to the API, please run the following commands in the terminal:

   - Clone the repository:
git clone https://github.com/Patrick-256/CSC365_FantasySoccer.git

   - Install the dependencies:
pip install requirements.txt

   -  Install alembic for database migrations:
pip install alembic
alembic init alembic
Follow the instructions here for creating and running migrations scripts

   - Set up the Vercel CLI to test endpoint and deployment:
npx i -g vercel
npx i -g vercel@latest
Follow the instructions here for further information

   - Install Docker to run on a local database
Download and install Docker from its offical website: www.docker.com
Follow the instructions here for setting up your local database


## Usage

To use Fantasy Soccer API, run the following command: ‘vercel dev’
The project will start and be accessible at `http://localhost:3001`.

Alternatively, open a web browser and go to: fantasy-soccer-api.vercel.app to run the production version of the project. Add /docs to the url to see all endpoints.


## Configuration

To configure the project, follow these steps:

1. Create a `.env` file in the project root.
2. Add the following environment variables:
   - `SUPABASE_API_KEY`: Your API key
   - `SUPABASE_URL`: Database URL
   - `POSTGRES_USER`: Postgres username
   - `POSTGRES_PASSWORD`: Postgres password
   - `POSTGRES_SERVER`: Postgres server URL
   - `POSTGRES_PORT`: Port number
   - `POSTGRES_DB`: Database name
3. Go to vercel.com and in your project -> Settings -> Environment Variables, include these same variables in order to allow vercel to access the database.

By default, the project uses the development environment. You can modify the configuration in the `.env` file.


## Resources

To construct our database, deploy our project, and create our diagrams, we used the following resources:

   - Supabase
   - Vercel
   - Alembic
   - LucidChart
   - Docker
   - PostgresSQL


## Credits
Patrick Whitlock   pwhitloc@calpoly.edu
Ashton Alonge     aalonge@calpoly.edu  

If you have any questions, issues, or feedback, feel free to contact us!
---
