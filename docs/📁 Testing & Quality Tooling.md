# 📁 Testing & Quality Tooling

## Testing & quality tooling

### 1. Testing layout

```
tests/
├─ test_[topics.py](http://topics.py)      # Topic API + model tests
└─ test_[sessions.py](http://sessions.py)    # Session API + model tests
```

- Use **pytest** as the primary test runner.
- Start with a few happy-path tests for creating and listing topics/sessions.

### 2. Tooling

- **black** – code formatter.
- **isort** – import sorter.
- **flake8** – style and lint checks.

These can be wired into pre-commit hooks or run via Docker for consistent, repeatable checks.

### 3. Running tests in Docker (conceptual)

- FastAPI tests: `docker compose run --rm web-fastapi pytest`
- Optional alt-backend tests can be run via their respective services if desired.

Keep the initial suite small but real, then grow coverage as you explore more Docker and backend features.