# 📋 StudyTracker – CI Workflow (GitHub Actions)

Minimal GitHub Actions workflow to run formatting, linting, and tests for StudyTracker.

---

## .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, master, develop ]
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f pyproject.toml ]; then
            pip install .[dev]
          elif [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi

      - name: Lint with flake8
        run: |
          flake8 src tests

      - name: Check formatting with black
        run: |
          black --check src tests

      - name: Run tests
        env:
          DATABASE_URL: postgresql+psycopg2://studytracker:[studytracker@localhost:5432](mailto:studytracker@localhost:5432)/studytracker
        run: |
          pytest -v
```

You can later extend this to spin up Postgres via a service container, generate coverage reports, or add security scanning once the core repo is stable.