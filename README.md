**RUN it locally**

This application requires docker to run. Make sure you have it installed before moving forward. It will also use an external docker image for the DB engine. To run the application locally, navigate to the project root folder and run the command below:

`docker-compose up`

You should see the docker image build locally and the server will be up on port 5001(had to change as 5000 is already a taken port on mac environments)  


**DEBUG**
make sure the map is set in your yaml file. Example:

`- PATHS_FROM_ECLIPSE_TO_PYTHON=[["/Users/jareas/Developer/ja-docker-images/python_container/docker/base","/app"]]`

***Bash to container***
The services in the docker compose file are as follow:
- mcquaig
- mysql

when fired up, the containers name's will be:

mcquaig-mcquaig-1
mcquaig-mysql-1

to bash into the containers you will run:
` docker exec -ti mcquaig-mysql-1 bash`
` docker exec -ti mcquaig-mcquaig-1 bash`

***Tests***
To run the tests, the script expects that the containers are running. With the containers up and running, run the command as below:

- from a linux/mac machine
```
cd 'path to tests folders'
./run.sh
```

You can also bash into the container and run:
`pytest` 

***Migrations**
from within the container bash run as below

upgrading:

`alembic -c development.ini upgrade head`


