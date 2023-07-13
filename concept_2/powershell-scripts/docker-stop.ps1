# ------------- Stop and remove the EPLF containers  ------------- #

docker stop eplf-publish
docker rm eplf-publish

docker stop eplf-republish
docker rm eplf-republish

docker stop eplf-listen
docker rm eplf-listen

docker stop eplf-validation
docker rm eplf-validation


docker stop eplf-db
docker rm eplf-db

docker stop fill
docker rm fill


# ------------- Stop and remove the ZD containers  ------------- #

docker stop zd-listen
docker rm zd-listen

docker stop zd-listen2
docker rm zd-listen2

docker stop zd-validation
docker rm zd-validation


docker stop zd-db
docker rm zd-db


# ------------- Stop and remove the Message Queue containers  ------------- #

docker stop mq
docker rm mq


# ------------- Remove the Docker network ------------- #

docker network rm containernetwork