# VSAV Match Database Discord Bot

Is fully functional! But is in a POC state as of now. Right now the DB is handled as a flat file but will be migrated to an RDS instance.

Type $help to see all features!

## Installation / Setup

1) Create a discord bot account, and find your token. [Read Instructions Here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).
1) Create a .env file in the root directory with the line.

		TOKEN=mydiscordbottoken

### Docker

1) Build the Image (in root directory):
	
		docker build -t matchdb .

2) Run Image

		docker run matchdb

### Poetry
1. [Install Poetry](https://python-poetry.org/) 
2. Install Dependencies via Poetry  

		poetry install
3. Run:

		poetry run python main.py