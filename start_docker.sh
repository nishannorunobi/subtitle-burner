#!/bin/bash
# Build (uses cache) and run the container interactively.

docker compose build
docker compose run --rm study
