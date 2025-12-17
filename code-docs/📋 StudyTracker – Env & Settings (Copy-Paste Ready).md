# 📋 StudyTracker – Env & Settings (Copy-Paste Ready)

Environment files and basic settings for StudyTracker, aligned with Docker Compose and local development patterns.

---

## .env.example

```
# Application
APP_ENV=local
APP_DEBUG=true
APP_PORT=8000

# Database
DATABASE_URL=postgresql+psycopg2://studytracker:studytracker@db:5432/studytracker
```

Copy this to `.env` in local development and adjust as needed.

---

## docker-compose.yml snippet (env usage)

Use this pattern in the `web-fastapi` service to read from `.env`:

```yaml
web-fastapi:
  build:
    context: .
    dockerfile: docker/Dockerfile.web-fastapi
  env_file:
    - .env
  depends_on:
    - db
  ports:
    - "8000:8000"
```

For Postgres, you can either keep inline env vars or move them into `.env` as well, depending on how much indirection you prefer for a learning repo.