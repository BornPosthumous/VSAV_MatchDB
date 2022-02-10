# VSAV Match Database Discord Bot

Is fully functional! But is in a POC state as of now. Right now the DB is handled as a flat file but will be migrated to an RDS instance.

Type $help to see all features!

## Installation / Setup

1) Create a discord bot account, and find your token. [Read Instructions Here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).

2) Change all .dummy files to have your desired configuration. All dummy info should point you to the correct information to input.

		.env.bot --> insert discord token

		.env.db --> postgres db configuration

		.env.pgadmin --> postgres admin configuration

		pgadmin/servers.json --> postgres database configuration

		pgadmin/pgpass --> postgress login information

## Running
Run with Docker-Compose in root directory
	docker-compose up

PGAdmin should be on http://localhost:8080

Discord bot should be connected if your token and bot setup is correct.