# create the custom docker network so that the containers may communicate with one another
# the containers are added to the network with the --net flag
docker network create --subnet=192.168.0.0/16 containernetwork

# start the containers
docker run --network=containernetwork --ip 192.168.0.22 -d --hostname rabbit-mq --name mq -p 5672:5672 -p 15672:15672 mq:latest

# wait for the rabbit mq server to start
Start-Sleep -Seconds 10



# Start the EPLF db
docker run --network=containernetwork --ip 192.168.0.23 --name eplf-db -d -p 3000:3000 eplf-db:latest

# wait for the database to start
Start-Sleep -Seconds 10

# Start the container that fills the EPLF db
docker run --network=containernetwork --name fill -d -p 4000:3000 fill:latest

# wait for the database to be filled
Start-Sleep -Seconds 120

# Start the EPLF applications
docker run --network=containernetwork --name eplf-publish -d -p 3001:3000 eplf-publish:latest
docker run --network=containernetwork --name eplf-listen -d -p 3002:3000 eplf-listen:latest
docker run --network=containernetwork --name eplf-republish -d -p 3003:3000 eplf-republish:latest
docker run --network=containernetwork --name eplf-validation -d -p 3004:3000 eplf-validation:latest



# Start the ZD db
docker run --network=containernetwork --ip 192.168.0.24 --name zd-db -d -p 3005:3000 zd-db:latest

# wait for the database to start
Start-Sleep -Seconds 30

# Start the ZD applications
docker run --network=containernetwork --name zd-listen -d -p 3006:3000 zd-listen:latest
docker run --network=containernetwork --name zd-listen2 -d -p 3007:3000 zd-listen:latest
docker run --network=containernetwork --name zd-validation -d -p 3008:3000 zd-validation:latest