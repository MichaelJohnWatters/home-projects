#!/bin/bash
echo "STARTING BASH SCRIPT..."
echo "STARTING HOME-PROJECTS DOCKER-COMPOSE UP"
sudo docker-compose up
wait $!
echo "FINISHED START HOME-PROJECTS"

