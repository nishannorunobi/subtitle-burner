#!/bin/bash
# Stop all running containers, remove stopped containers, and prune dangling images.

echo "Stopping containers..."
docker compose down

echo "Removing dangling images..."
docker image prune -f

echo "Done."
