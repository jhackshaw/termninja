cd termninja
git pull
docker-compose down
docker-compose up -d --build
docker-compose exec -d api sh -c 'alembic upgrade head'
exit
