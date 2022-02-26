# VSAV Match Database (Plus Discord Bot)

This is a database for storing match footage and other videos for Vampire Savior.
The database is in Postgres and REST API (Django rest framework) is mostly stubbed out and functional.

The bot is fully functional! However it will likely be discontinued as I have begun coding a web interface:

https://github.com/NBeing/VSAV_MatchDB


Type $help to see all features!

## Installation / Setup

1) Create a discord bot account, and find your token. [Read Instructions Here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).

2) Change all .dummy files to have your desired configuration. All dummy info should point you to the correct information to input. Remove .dummy extension.

		.env.bot --> insert discord token

		.env.db --> postgres db configuration

		.env.pgadmin --> postgres admin configuration

		pgadmin/servers.json --> postgres database configuration

		pgadmin/pgpass --> postgress login information

## Running
Run with Docker-Compose in root directory
	docker-compose up

Make sure to log in to the docker container and run the Django migrations!
		docker-exec -it <containername> bash 
		manage.py migrate

PGAdmin should be on http://localhost:8080. You can login with the username/pass set in your servers.json

You can view the API documentation at http://localhost:8000/vsav_info/matches/ .
If you'd like some dummy data, you may edit the following file:
		api/matchdb/match_db/util/match_db.csv
And make a get request to:
`http://localhost:8000/vsav_info/matches/seed_db_from_csv`

Discord bot should be connected if your token and bot setup is correct.
