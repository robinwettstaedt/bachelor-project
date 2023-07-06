# Stop all containers and remove them, as well as the docker network
docker stop eplf-publish
docker rm eplf-publish

docker stop eplf-republish
docker rm eplf-republish

docker stop eplf-listen
docker rm eplf-listen


docker stop eplf-db
docker rm eplf-db


docker stop fill
docker rm fill




docker stop zd
docker rm zd

docker stop zd2
docker rm zd2

docker stop zd3
docker rm zd3


docker stop zd-db
docker rm zd-db




docker stop mq
docker rm mq



docker network rm containernetwork