# 📋 StudyTracker – Testing & Quality (Copy-Paste Ready)

Minimal but meaningful tests and quality tooling for StudyTracker, aligned with the Testing & Quality Tooling page.

---

## tests/test_[healthz.py](http://healthz.py)

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "studytracker-web-fastapi"
```

---

## tests/test_[topics.py](http://topics.py)

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_and_get_topic():
    create_resp = [client.post](http://client.post)(
        "/topics",
        json={"name": "Docker", "description": "Learn Docker"},
    )
    assert create_resp.status_code == 201
    topic = create_resp.json()

    get_resp = client.get(f"/topics/{topic['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["name"] == "Docker"

def test_create_session_for_existing_topic():
    # create topic
    topic_resp = [client.post](http://client.post)(
        "/topics",
        json={"name": "Postgres", "description": "Learn SQL"},
    )
    topic = topic_resp.json()

    # create session
    session_resp = [client.post](http://client.post)(
        "/sessions",
        json={
            "topic_id": topic["id"],
            "study_date": "2025-01-01",
            "duration_minutes": 60,
            "notes": "Intro session",
        },
    )
    assert session_resp.status_code == 201

def test_create_session_for_unknown_topic_fails():
    resp = [client.post](http://client.post)(
        "/sessions",
        json={
            "topic_id": 9999,
            "study_date": "2025-01-01",
            "duration_minutes": 30,
            "notes": "Should fail",
        },
    )
    assert resp.status_code in (400, 404)
```

---

## pyproject.toml (minimal tools)

```toml
[project]
name = "studytracker-docker-learning"
version = "0.1.0"
requires-python = ">=3.12"

[project.optional-dependencies]
dev = [
  "fastapi",
  "uvicorn[standard]",
  "sqlalchemy",
  "psycopg2-binary",
  "pydantic",
  "pytest",
  "httpx",
  "black",
  "isort",
  "flake8",
]

[[tool.black](http://tool.black)]
line-length = 88
target-version = ["py312"]

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
pythonpath = ["src"]
```

You can either commit `pyproject.toml` directly from here or map the dependencies into `requirements.txt` depending on your preferred packaging approach.