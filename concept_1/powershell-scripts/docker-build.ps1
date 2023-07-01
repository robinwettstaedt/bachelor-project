#$ build the rabbit mq image
docker build --no-cache --pull --rm -f "..\mq\Dockerfile" -t mq:latest "..\..\"


# build the eplf database image
docker build --no-cache --pull --rm -f "..\db\eplf\Dockerfile" -t eplf-db:latest "..\..\"

# build the eplf service image
docker build --no-cache --pull --rm -f "..\eplf\Dockerfile" -t eplf:latest "..\..\"


# build the zd database image
docker build --no-cache --pull --rm -f "..\db\zd\Dockerfile" -t zd-db:latest "..\..\"

# build the zd service image
docker build --no-cache --pull --rm -f "..\zd\Dockerfile" -t zd:latest "..\..\"