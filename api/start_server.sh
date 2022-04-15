docker-compose down --remove-orphans
docker-compose up --build -d pgadmin postgres
SQL_HOST_FROM_CONTAINER=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_container`
cd ../config
if [ -f .env.api ]
then
    echo "Adding"
    export $(cat ../config/.env.api | grep -v '#' | sed 's/\r$//' | awk '/=/ {print $1}' )
    export SQL_HOST=${SQL_HOST_FROM_CONTAINER}
fi
cd ../api
poetry install
poetry run ./manage.py runserver 0.0.0.0:8000