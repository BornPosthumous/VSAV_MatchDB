#!/bin/bash
docker compose down
docker volume rm vsav_matchdb_pgadmin-data  
docker volume rm vsav_matchdb_matchdb-data