# bachelor-project


The code contained in this repository is part of the Bachelors Thesis 'Eventual Consistency zwischen (in) Microservices' by Robin Wettstädt, which was overseen by Prof. Dr.-Ing. Piotr Wojciech Dabrowski and M.Sc. André Mai.

The goal was to simulate system concepts that were developed in the thesis and test their validity on a smaller scale.


<br>


## Technologies used

- Docker
- Python
- RabbitMQ
- PostgreSQL
- HTML/CSS/Javascript (only for the visualization)


<br>


## Project Structure

Two concepts were develop as part of the thesis, hence the split into 2 different directories (/concept_1, /concept_2).

Inside each concept directory, the contents are split up into the different domains of each system. To fully understand this, the context of the actual thesis is certainly helpful. Nonetheless, a brief explanation of their contents:

db:
- Contains the Dockerfiles and initialization scripts for the databases.

eplf:
- Is one of the two primary services in the simulated system. Its primary responsibility is sending data retrieved from its own database to the ZD (Zahlungsdienst) service.
- Contains more directories for each of its functions, which contain the Dockerfiles and Python scripts of the resulting container.

interface:
- Is a web interface for visualizing the databases data during the running simulation.
- Contains the Dockerfile(s) and Python/HTML/Javascript scripts needed for the execution of the container.

mq:
- Contains the Dockerfile and RabbitMQ configuration file needed for the execution of the message queue container.

powershell-scripts:
- Contains all the Windows PowerShell (.ps1) scripts needed for interacting with the simulated system (starting, stopping, building the Docker containers)

bash-scripts:
- Contains all the Linux Bash (.sh) scripts needed for interacting with the simulated system (starting, stopping, building the Docker containers)

validator (only in /concept_2):
- Is the third service in the simulated system and responsible for validating the data sent between EPLF and ZD.
- Contains more directories for each of its functions, which contain the Dockerfiles and Python scripts of the resulting container.

zd:
- Is one of the two primary services in the simulated system. Its primary responsibility is receiving and processing the data sent by the EPLF (Einnahmeplattform) service.
- Contains more directories for each of its functions, which contain the Dockerfiles and Python scripts of the resulting container.


<br>


## Requirements

Windows:
- (tested on Windows 10)
- Docker Desktop

Linux:
- (tested on Ubuntu 20.04)
- Docker


<br>


## How to start the simulated Environment (Windows)

1. Open the project in PowerShell.
2. Change directories in the concept of choice:

```
cd .\concept_1\
```

or

```
cd .\concept_2\
```
3. Change directories into the `powershell-scripts` directory
```
cd .\powershell-scripts\
```

4. For convenience, start the `docker-full-restart.ps1` script. For a more detailed explanation on the scripts, please see below.

```
.\docker-full-restart.ps1
```

The images will be built and the containers will start. This should take around 3-4 minutes, as the databases get filled with random data.

The logs of the containers can be easily viewed within Docker Desktop and the `interface` container will provide a table overview of the current state of the databases on [localhost:5000](http://localhost:5000/).


<br>


## The PowerShell scripts

There are 4 scripts in total in each concept_X/powershell-scripts folder.

`docker-stop-script.ps1`:
Stops all the containers upon execution (Does not do anything if the containers are not running).

`docker-build-script.ps1`:
Builds the images upon execution.

`docker-run-script.ps1`:
Starts the containers in the correct order upon execution.

`docker-full-restart.ps1`:
Executes the 3 previous scripts in the order they are shown here.


<br>


## How to start the simulated Environment (Linux)

# TODO:
- test



<br>


## The Bash scripts

There are 4 scripts in total in each concept_X/bash-scripts folder.

`docker-stop-script.sh`:
Stops all the containers upon execution (Does not do anything if the containers are not running).

`docker-build-script.sh`:
Builds the images upon execution.

`docker-run-script.sh`:
Starts the containers in the correct order upon execution.

`docker-full-restart.sh`:
Executes the 3 previous scripts in the order they are shown here.
