# home-projects



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