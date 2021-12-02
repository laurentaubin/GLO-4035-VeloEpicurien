docker-compose down
docker volume rm $(docker volume ls -qf dangling=true)
cp README.md JoGod/PROJECT_README.md
docker-compose up --build