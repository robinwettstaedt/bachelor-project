# Stop all containers and remove them, as well as the docker network
docker stop eplf
docker rm eplf

docker stop zd
docker rm zd

docker network rm container-net