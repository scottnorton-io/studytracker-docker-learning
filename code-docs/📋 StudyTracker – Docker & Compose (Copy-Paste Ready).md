# 📋 StudyTracker – Docker & Compose (Copy-Paste Ready)

This page contains the initial Dockerfile and docker-compose configuration for the StudyTracker FastAPI service and Postgres database.

> **Scope of this page:** minimal but functional Docker + Compose setup for local development. Later iterations can add healthcheck wiring, multi-stage builds, and CI integration.
> 

---

## docker/Dockerfile.web-fastapi

```docker
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir fastapi uvicorn[standard]

COPY src ./src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## docker-compose.yml (v0.1.0 – FastAPI + Postgres)

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: studytracker
      POSTGRES_USER: studytracker
      POSTGRES_PASSWORD: studytracker
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data

  web-fastapi:
    build:
      context: .
      dockerfile: docker/Dockerfile.web-fastapi
    environment:
      DATABASE_URL: postgres://studytracker:studytracker@db:5432/studytracker
    depends_on:
      - db
    ports:
      - "8000:8000"

volumes:
  db-data:
```

---

## Next planned iteration on this page

- Add **healthchecks** for `db` and `web-fastapi` services.
- Introduce **env file usage** (`.env` / `.env.example`) instead of hardcoded credentials.
- Add separate service entries for **Flask** and **Express** alternates once implemented.
- Align service names and ports with the conventions in the broader Docker & Compose Layout page.