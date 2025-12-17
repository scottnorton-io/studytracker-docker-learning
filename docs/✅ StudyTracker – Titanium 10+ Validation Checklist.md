# ✅ StudyTracker – Titanium 10+ Validation Checklist

# StudyTracker – Titanium 10+ Validation Checklist

Use this checklist to validate that the **actual GitHub repository** for StudyTracker still meets the **Titanium 10+ Code of Excellence and Standards** defined for the Greenfield Docker Learning project.

This is a **repo-facing** checklist: it assumes the Notion design is the source of truth and verifies that the implementation matches.

---

## 1. Repository Layout & Files

**Goal:** Confirm that the repo structure matches the documented pattern.

- [ ]  Top-level layout includes:
    - [ ]  `src/app/` (FastAPI primary backend)
    - [ ]  `src/alt_backends/` (Flask and Express implementations)
    - [ ]  `src/migrations/` or equivalent migrations directory
    - [ ]  `tests/` (pytest suite)
    - [ ]  `docker/` (Dockerfiles and related assets, if used)
    - [ ]  `docker-compose.yml`
    - [ ]  `.env.example`
    - [ ]  [`README.md`](http://README.md)
    - [ ]  `LICENSE`
    - [ ]  `CODE_OF_[CONDUCT.md](http://CONDUCT.md)`
    - [ ]  [`CONTRIBUTING.md`](http://CONTRIBUTING.md)
    - [ ]  [`SECURITY.md`](http://SECURITY.md)
    - [ ]  `.github/` (issue + PR templates, optional CI workflows)

**Pass criteria:** All expected paths and files exist, and their purpose matches the Greenfield Docker Learning spec.

---

## 2. Domain & Architecture Integrity

**Goal:** Ensure the implemented system still matches the documented **topics/sessions** and **system context** design.

- [ ]  Data model:
    - [ ]  `Topic` entity with: id, name, description, created_at (or equivalents)
    - [ ]  `Session` entity with: id, topic_id, study_date, duration_minutes, notes, created_at
    - [ ]  One-to-many relationship (one topic, many sessions) is enforced in schema and models
- [ ]  HTTP surface (for each backend):
    - [ ]  `GET /healthz`
    - [ ]  `GET /topics`
    - [ ]  `POST /topics`
    - [ ]  `GET /topics/{topic_id}`
    - [ ]  `POST /sessions`
- [ ]  Docker/Compose topology:
    - [ ]  `web-fastapi` + `db` services in `docker-compose.yml`
    - [ ]  Optional `web-flask` and `web-express` services present (can be toggled on/off)
    - [ ]  All web services connect to the same Postgres service via service-name (for example, host `db`)

**Pass criteria:** Routes, data model, and Compose services match the architecture described in the StudyTracker paper and internal docs.

---

## 3. Docker-First Run Story

**Goal:** Validate that Docker/Compose is the **primary** and reliable way to run the app.

- [ ]  `.env.example` is present and accurate (no real secrets; clear placeholders)
- [ ]  README includes a **canonical Quick Start** section:
    - [ ]  Copy `.env.example` → `.env`
    - [ ]  Run `docker compose up --build web-fastapi db`
    - [ ]  Visit `/healthz` to confirm system health
- [ ]  Running the above command on a clean machine:
    - [ ]  Builds without errors (assuming Docker is installed)
    - [ ]  Starts FastAPI and Postgres containers
    - [ ]  Health-check endpoint returns an expected success indication

**Pass criteria:** A new user can follow the README and get to a healthy stack using Docker/Compose only.

---

## 4. Security Hygiene (Learning Level)

**Goal:** Confirm basic security hygiene appropriate for a teaching repo.

- [ ]  No plaintext secrets checked into the repo (API keys, real passwords, real connection strings)
- [ ]  `.env.example` contains **example** values only (clearly non-production)
- [ ]  [`SECURITY.md`](http://SECURITY.md) states that this is a **learning repository** and not intended for direct deployment in high-risk production environments without additional hardening
- [ ]  README or [SECURITY.md](http://SECURITY.md) mentions:
    - [ ]  Need for further hardening (auth, TLS, secrets management, etc.) before production use

**Pass criteria:** Repo is safe to make public as a teaching artifact; no sensitive configuration is embedded.

---

## 5. Tests, Tooling & CI

**Goal:** Validate that StudyTracker meets Titanium 10+ expectations for quality and repeatability.

- [ ]  Tests:
    - [ ]  `tests/` directory contains pytest-based tests for:
        - Health check
        - Topic creation/listing
        - Session creation
    - [ ]  README documents how to run tests locally, preferably via Docker (for example, `docker compose run --rm web-fastapi pytest`)
- [ ]  Tooling:
    - [ ]  Python tooling set up (`black`, `isort`, `flake8` or equivalents)
    - [ ]  Optional: JavaScript tooling configured for Express backend (linting, formatting)
- [ ]  CI (recommended, even minimal):
    - [ ]  A GitHub Actions (or similar) workflow that runs tests and/or linters on push/PR
    - [ ]  Status is visible in the repo (badges optional but nice)

**Pass criteria:** Tests run cleanly, tooling is configured, and (ideally) CI enforces at least the basics.

---

## 6. Documentation & Visuals

**Goal:** Ensure that the repository-level documentation reflects the design captured in Notion.

- [ ]  [`README.md`](http://README.md) includes:
    - [ ]  Short project overview and learning goals
    - [ ]  System context diagram (or link/image)
    - [ ]  Data model (ER diagram or equivalent description)
    - [ ]  Quick Start (Docker-first)
    - [ ]  Basic troubleshooting / common issues
    - [ ]  A condensed version of the **“Follow the recipe”** checklist
- [ ]  Diagrams (system, request lifecycle, ER) are present in the repo (for example, under `docs/` or embedded as images) and match the Notion versions
- [ ]  Links (if any) to the **StudyTracker papers/whitepaper/blog** are up to date

**Pass criteria:** A reader who never sees Notion can understand the system from the repo alone.

---

## 7. Multi-Backend Coherence

**Goal:** Confirm that alternate backends are truly first-class and coherent.

- [ ]  Flask and Express backends:
    - [ ]  Implement the same set of endpoints as FastAPI
    - [ ]  Use the same database schema / migrations
    - [ ]  Have working Dockerfiles
    - [ ]  Are wired into `docker-compose.yml` and documented in README
- [ ]  At least one documented flow for swapping backends:
    - [ ]  Comment out `web-fastapi`, enable `web-flask` or `web-express`
    - [ ]  Run Compose
    - [ ]  Verify `/healthz`, topics, and sessions work as expected

**Pass criteria:** Alternate backends are not “stale demos”; they are functional and aligned with the primary.

---

## 8. Pattern & Reuse Notes

**Goal:** Ensure that someone cloning this repo understands it as a **pattern**, not just a one-off app.

- [ ]  README (or a `docs/[pattern.md](http://pattern.md)`) briefly explains that:
    - [ ]  StudyTracker is a template for small, production-shaped learning projects
    - [ ]  The pattern can be reused with different domains and stacks
    - [ ]  Key ingredients: small domain, Docker-first architecture, multi-backend (optional), strong docs

**Pass criteria:** Readers see how to *adapt* StudyTracker, not only how to run it.

---

## 9. Final Titanium 10+ Sign-Off

Once all sections above are satisfied:

- [ ]  Update this checklist in Notion with the date of validation and the validator’s name.
- [ ]  (Optional) Add a short [`VALIDATION.md`](http://VALIDATION.md) or badge in the repository noting that it meets the current Titanium 10+ standard.

**Recommendation:** Re-run this checklist whenever you:

- Add a new backend
- Change the Compose topology
- Significantly refactor the repository layout
- Prepare a new public release or talk based on the project