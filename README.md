# home-projects

do I try to get druid on run on some arm64?
or do i just run druid on a different pc
and have some ssh script to start it up, when i run docker.

current project is running on rasbian, which is armhf 32-bit


Needed
docker
docker-compose
adafruit_blinka




test project-go-api DockerFile

sudo docker build -t michaeljohnwatters/project-go-api .
sudo docker run --publish 8080:8080 -t michaeljohnwatters/project-go-api



handy docker commands
stop all
docker container stop $(docker container ls -aq)
remove all
docker container rm $(docker container ls -aq)

stop and remove
docker container stop $(docker container ls -aq) && docker container rm $(docker container ls -aq)
