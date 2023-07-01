# create the custom docker network so that the containers may communicate with one another
# the containers are added to the network with the --net flag
docker network create --subnet=192.168.0.0/16 containernetwork

# start the containers
docker run --network=containernetwork --ip 192.168.0.22 -d --hostname rabbit-mq --name mq -p 5672:5672 -p 15672:15672 mq:latest

# wait for the rabbit mq server to start
Start-Sleep -Seconds 10



# Start the EPLF db
docker run --network=containernetwork --ip 192.168.0.23 --name eplf-db -d -p 3000:3000 eplf-db:latest

# Start the EPLF applications
docker run --network=containernetwork --name eplf -d -p 3000:3000 eplf:latest
# docker run --network=containernetwork --name eplf2 -d -p 3001:3000 eplf:latest
# docker run --network=containernetwork --name eplf3 -d -p 3002:3000 eplf:latest



# Start the ZD db
docker run --network=containernetwork --ip 192.168.0.24 --name zd-db -d -p 3000:3000 zd-db:latest

# Start the ZD applications
docker run --network=containernetwork --name zd -d -p 3003:3000 zd:latest
# docker run --network=containernetwork --name zd2 -d -p 3004:3000 zd:latest
# docker run --network=containernetwork --name zd3 -d -p 3005:3000 zd:latest