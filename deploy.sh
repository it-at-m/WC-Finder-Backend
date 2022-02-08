echo "Starting deployment ..."

cd /docker/batch14--LHM--backend

git pull

docker-compose down 

docker image prune --all --force

docker-compose up -d --build

echo "Starting deployment complete"