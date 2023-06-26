# create the custom docker network so that the containers may communicate with one another
# the containers are added to the network with the --net flag
docker network create --subnet=172.18.0.0/16 container-net


# start the containers
docker run --net container-net --name eplf -d -p 3000:3000 eplf:latest

docker run --net container-net --name zd -d -p 3001:3000 zd:latest