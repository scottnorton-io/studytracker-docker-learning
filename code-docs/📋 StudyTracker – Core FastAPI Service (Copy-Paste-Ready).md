# 📋 StudyTracker – Core FastAPI Service (Copy-Paste Ready)

This page contains the initial, copy-paste-ready implementation of the **core FastAPI service** for StudyTracker.

> **Scope of this page:** minimal but functional service with in-memory storage, matching the Greenfield Docker Learning spec. Later iterations can add Postgres, SQLAlchemy, and migrations.
> 

---

## src/app/[main.py](http://main.py)

```python
from datetime import date, datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="StudyTracker")

class TopicBase(BaseModel):
    name: str
    description: str | None = None

class Topic(TopicBase):
    id: int
    created_at: datetime

class SessionBase(BaseModel):
    topic_id: int
    study_date: date
    duration_minutes: int
    notes: str | None = None

class Session(SessionBase):
    id: int
    created_at: datetime

_topics: list[Topic] = []
_sessions: list[Session] = []
_topic_id = 0
_session_id = 0

@app.get("/healthz")
def healthz() -> dict:
    """Basic liveness check used by Compose, CI, and monitoring."""
    return {"status": "ok", "service": "studytracker-web-fastapi"}

@app.get("/topics", response_model=List[Topic])
def list_topics() -> List[Topic]:
    """Return all topics.

    v0.1.0 uses in-memory storage so you can validate the HTTP API
    shape before wiring Postgres.
    """

    return _topics

@[app.post](http://app.post)("/topics", response_model=Topic, status_code=201)
def create_topic(payload: TopicBase) -> Topic:
    """Create a new learning topic.

    Examples:
    - name: "Docker", description: "Learn container basics"
    - name: "PostgreSQL", description: "SQL and migrations"
    """

    global _topic_id

    _topic_id += 1
    topic = Topic(
        id=_topic_id,
        created_at=datetime.utcnow(),
        **payload.dict(),
    )
    _topics.append(topic)
    return topic

@app.get("/topics/{topic_id}", response_model=Topic)
def get_topic(topic_id: int) -> Topic:
    """Get a single topic by ID.

    In later versions, this will also surface related sessions via
    either embedding or a companion endpoint.
    """

    for t in _topics:
        if [t.id](http://t.id) == topic_id:
            return t
    raise HTTPException(status_code=404, detail="Topic not found")

@[app.post](http://app.post)("/sessions", response_model=Session, status_code=201)
def create_session(payload: SessionBase) -> Session:
    """Create a new study session for an existing topic."""

    global _session_id

    if not any([t.id](http://t.id) == payload.topic_id for t in _topics):
        raise HTTPException(status_code=400, detail="Unknown topic_id")

    _session_id += 1
    session = Session(
        id=_session_id,
        created_at=datetime.utcnow(),
        **payload.dict(),
    )
    _sessions.append(session)
    return session
```

---

## Next planned iteration on this page

- Add **database integration** (SQLAlchemy models + Postgres) consistent with the ERD.
- Introduce a simple **repository/service layer** to keep routes thin.
- Add **error-handling patterns** aligned to Titanium 10+ (standard error envelope, trace IDs).
- Align docstrings and examples with the StudyTracker publication variants.