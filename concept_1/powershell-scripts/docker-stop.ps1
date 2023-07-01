# Stop all containers and remove them, as well as the docker network
docker stop eplf
docker rm eplf

docker stop zd
docker rm zd

docker stop rabbit-mq
docker rm rabbit-mq

docker network rm container-net