# build the eplf image
docker build --no-cache --pull --rm -f "..\eplf\Dockerfile" -t eplf:latest "..\..\"

# build the zd image
docker build --no-cache --pull --rm -f "..\zd\Dockerfile" -t zd:latest "..\..\"