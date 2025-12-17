# 📁 Alternate Backends (Flask & Express)

## Alternate backends (Flask & Express)

### 1. Purpose

Flask and Express are **plug-and-play** backends that:

- Reuse the same PostgreSQL database and Docker network.
- Expose an equivalent HTTP surface (at least `/healthz`, `/topics`, `/sessions`).
- Let you compare Python (FastAPI vs Flask) and JS (Express) ergonomics.

### 2. Files

```
src/alt_backends/
├─ flask_[app.py](http://app.py)      # Flask application
└─ express_app.js    # Express application
```

### 3. Alignment with FastAPI

- Endpoints and basic payload shapes should mirror the FastAPI backend.
- Environment and DB connectivity come from the same `.env` / compose file.
- Frontend templates can be shared or reimplemented for learning.

### 4. Switching backends with Docker

- **Flask:** `docker compose up --build web-flask db`
- **Express:** `docker compose up --build web-express db`

In both cases, you should be able to hit:

- `GET /healthz`
- `GET /topics`
- `POST /topics`
- `POST /sessions`

and see behavior compatible with the FastAPI reference implementation.