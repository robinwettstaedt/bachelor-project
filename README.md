# bachelor-project

## Requirements

- Windows (preferably 10)
- Docker Desktop


<br>


## How to start the simulated Environment

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

There are 4 scripts in total in each concept folder.

`docker-stop-script.ps1`:
Stops all the containers upon execution (Does not do anything if the containers are not running).

`docker-build-script.ps1`:
Builds the images upon execution.

`docker-run-script.ps1`:
Starts the containers in the correct order upon execution.

`docker-full-restart.ps1`:
Executes the 3 previous scripts in the order they are shown here.