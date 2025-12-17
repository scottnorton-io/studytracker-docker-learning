# 📁 FastAPI Backend (Primary)

## FastAPI backend (primary)

### 1. Purpose

The FastAPI backend is the **reference implementation** for StudyTracker:

- Defines the canonical HTTP surface (paths, payloads, responses).
- Owns the Pydantic schemas used by clients and tests.
- Demonstrates modern async-friendly Python service design.

### 2. Module layout

```
src/app/
├─ __init__.py       # Package marker, optional app factory
├─ [main.py](http://main.py)           # FastAPI app instance, route includes
├─ [config.py](http://config.py)         # Settings from environment variables
├─ [db.py](http://db.py)             # DB engine and session management
├─ [models.py](http://models.py)         # ORM models (Topic, Session)
├─ [schemas.py](http://schemas.py)        # Pydantic models for I/O
├─ routes/
│  ├─ [topics.py](http://topics.py)      # /topics endpoints
│  └─ [sessions.py](http://sessions.py)    # /sessions endpoints
└─ templates/
   ├─ base.html
   ├─ topics_list.html
   └─ sessions_list.html
```

### 3. Core routes (conceptual)

- `GET  /healthz` – returns a simple `{ "status": "ok" }` payload.
- `GET  /topics` – list all topics, rendered as HTML (and optionally JSON).
- `POST /topics` – create a new topic.
- `GET  /topics/{topic_id}` – show a single topic and its sessions.
- `POST /sessions` – create a new study session for a topic.

### 4. Responsibilities by file (high level)

- [**`main.py`**](http://main.py) – create `FastAPI()` app, mount routers, serve templates.
- [**`config.py`**](http://config.py) – read `DATABASE_URL` and other settings from env.
- [**`db.py`**](http://db.py) – create SQLAlchemy engine and session dependency.
- [**`models.py`**](http://models.py) – SQLAlchemy models for `Topic` and `Session`.
- [**`schemas.py`**](http://schemas.py) – request/response types for FastAPI.
- **`routes/*.py`** – implement CRUD handlers using models + schemas.

Detailed file contents should live in Git/GitHub; this page stays focused on structure and intent for learning.