# Stop all containers and remove them, as well as the docker network
docker stop eplf
docker rm eplf

# docker stop eplf2
# docker rm eplf

# docker stop eplf3
# docker rm eplf3


docker stop eplf-db
docker rm eplf-db


docker stop fill
docker rm fill




docker stop zd
docker rm zd

docker stop zd2
docker rm zd2

# docker stop zd3
# docker rm zd3


docker stop zd-db
docker rm zd-db




docker stop mq
docker rm mq



docker network rm containernetwork