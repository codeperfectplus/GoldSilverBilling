#!/bin/bash

# Stop and remove any existing containers
docker-compose down

# Build the Docker image and start the containers
docker-compose up --build
