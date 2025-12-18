#!/usr/bin/env bash
set -euo pipefail

cd "${HOME}/Documents/GitHub/studytracker-docker-learning"

# 1) Stop running containers (network and volumes remain)
docker compose stop

# 2) Start containers again with existing images and volumes
docker compose up web-fastapi db
