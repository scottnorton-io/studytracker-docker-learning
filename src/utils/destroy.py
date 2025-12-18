#!/usr/bin/env bash
set -euo pipefail

cd "${HOME}/Documents/GitHub/studytracker-docker-learning"

# 1) Stop containers and remove network + volumes
#    WARNING: this deletes the Postgres data volume (fresh DB next run)
docker compose down -v
