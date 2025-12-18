# Show status of all services in this compose project
docker compose ps

# Tail logs from the web-fastapi service
docker compose logs -f web-fastapi

# Tail logs from the db service
docker compose logs -f db

# Open a shell inside the running web-fastapi container
# (useful for inspecting environment, Python path, etc.)
docker compose exec web-fastapi /bin/bash

# Run a one-off command inside web-fastapi
# Example: run tests from inside the container
docker compose run --rm web-fastapi pytest -v

# Connect to Postgres from inside the db container
# (psql will already be installed)
docker compose exec db psql \
  -U studytracker \
  -d studytracker
  
