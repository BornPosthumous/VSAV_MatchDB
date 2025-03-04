#!/bin/bash
docker compose down --remove-orphans

docker compose up --build --force-recreate pgadmin postgres api
