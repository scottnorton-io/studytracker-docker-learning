#!/usr/bin/env bash
set -euo pipefail

cd "${HOME}/Documents/GitHub/studytracker-docker-learning"

# 1) Rebuild the web-fastapi image
docker compose build --no-cache web-fastapi

# 2) Restart app + database (reuses existing volume data)
docker compose up web-fastapi db
