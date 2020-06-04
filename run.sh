#!/bin/bash
echo "STARTING BASH SCRIPT..."
echo "STARTING HOME-PROJECTS DOCKER-COMPOSE UP"
sudo docker-compose up
wait $!
echo "FINISHED START HOME-PROJECTS"
echo "STARTING APACHE-DRUID-0.18.1..."
sudo ./apache-druid-0.18.1/bin/start-nano-quickstart
echo "FINISHED STARTING APACHE-DRUID-0.18.1..."
