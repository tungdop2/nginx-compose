#!/bin/bash

echo "Running docker compose"
echo "Building docker images..."

# Build the Docker images
sudo docker compose build

# Read the number of replicas and workers from user input
read -p "Number of replicas: " replicas
read -p "Number of workers per replica: " workers

# Export the number of workers as an environment variable
export WORKERS=$((2 * workers + 1))

# Run Docker Compose with the specified number of replicas
sudo docker compose up --scale web=$replicas
