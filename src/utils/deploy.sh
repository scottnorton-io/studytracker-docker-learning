#!/usr/bin/env bash
set -euo pipefail

# 1) Go to the repo root
cd "${HOME}/Documents/GitHub/studytracker-docker-learning"

# 2) Make sure env file exists
if [ ! -f .env ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
fi

# 3) Build and start app + database
docker compose up --build web-fastapi db
