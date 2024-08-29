#!/bin/bash

script_dir=$(dirname $0)
cd $script_dir
# Stop and remove any existing containers
docker-compose down

# Build the Docker image and start the containers
docker-compose up --build
