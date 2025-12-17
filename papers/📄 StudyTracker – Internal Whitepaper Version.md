# 📄 StudyTracker – Internal Whitepaper Version

# StudyTracker: A Titanium 10+ Pattern for Teaching Docker-First Web Architecture

## 1. Executive Summary

StudyTracker is a small, production-shaped web application and Docker stack designed as a **Titanium 10+ training asset**. It exists to give consultants and engineers a concrete, end-to-end example of a containerized web service with a relational database, implemented to a standard that we would be comfortable publishing externally.

The app itself is intentionally simple: it tracks learning topics (for example, "Docker", "PostgreSQL") and sessions (date, duration, notes). Under the hood, it is a Docker-first system with a FastAPI primary backend, optional Flask and Express alternates, and a PostgreSQL database, all orchestrated via Docker Compose. The associated repository includes architecture diagrams, narrative documentation, tests, and standard GitHub assets.

For Johanson, StudyTracker has three primary uses:

- As an **onboarding vehicle** to get new team members comfortable with Docker-first workflows and web architecture.
- As a **reference pattern** for how we want small services and training projects to be structured (layout, documentation, tests, visuals).
- As a **reusable teaching artifact** for internal workshops and client enablement sessions.

This document describes why StudyTracker exists, the design principles behind it, how to use it in training, how to measure outcomes, and how to adapt the pattern to other initiatives.

## 2. Why StudyTracker Exists

We routinely work with systems where containers, web backends, and databases must be reasoned about together. However, learning paths are often fragmented:

- Docker is introduced via one-off commands and simple images.
- Web frameworks are learned via quickstarts that assume a database and deployment story already exist.
- Databases are taught as isolated schemas or queries without the surrounding application context.

This fragmentation shows up in practice. Engineers and consultants may be comfortable in one layer but hesitant when asked to trace a request through the stack or to understand how the local environment maps to production. When we add compliance, observability, and resilience requirements on top, the cognitive load can become significant.

StudyTracker is designed as a **single, coherent story**:

- One small domain (topics and sessions).
- One Docker-first architecture (web container + database container on a shared network).
- Multiple backends implementing the same HTTP surface.
- One repository that meets our standards for clarity and documentation.

The goal is to provide a shared mental model that we can reference in training, in design discussions, and in client conversations.

## 3. Design Principles and Constraints

StudyTracker was built under a set of explicit principles that should also guide future training artifacts.

### 3.1 Titanium 10+ alignment

The project is intended to be an example of **Titanium 10+ Code of Excellence and Standards** in miniature. That means:

- Clear, well-structured documentation, not just working code.
- Obvious separation of concerns in the repository (routes, models, schemas, config, tests).
- No hidden configuration or ad hoc scripts; everything needed to run is in the repo.

### 3.2 Intentional minimalism

The domain is deliberately small. We do not model accounts, authentication, billing, or complex workflows. Instead, we pick a problem that is rich enough to be realistic (logging work over time) but simple enough that domain details do not crowd out the architecture.

Constraints include:

- Limited number of routes.
- A single database and schema.
- No unnecessary external dependencies.

### 3.3 Docker-first, not Docker-after

Docker is not an afterthought. The **primary way** to run and interact with the system is via Docker Compose:

- `web-fastapi` (primary backend) and `db` are the default services.
- Alternate backends plug into the same Compose network and database.
- Environment configuration is handled through `.env` and `.env.example`.

Local, non-Docker execution is possible for debugging but is not the main learning path.

### 3.4 Publication-ready repository

From the beginning, StudyTracker is structured as if it will be published externally:

- A complete [`README.md`](http://README.md) that explains architecture, setup, and learning goals.
- Standard GitHub assets (license, code of conduct, contributing guide, security policy, issue and PR templates).
- Diagrams checked into the repo and referenced from the documentation.

This makes StudyTracker an asset we can point to in external talks, workshops, or case studies.

## 4. Architecture and Repository Pattern

This section summarizes the pattern that StudyTracker models.

### 4.1 High-level architecture

At a high level, StudyTracker is a three-container system:

- **Web container (FastAPI)** – primary backend implementation.
- **Alternate web containers (Flask, Express)** – optional, same HTTP surface.
- **Database container (PostgreSQL)** – persistence for topics and sessions.

All containers share a Docker network, and the web containers refer to the database by the service name `db`. Health checks (for example, `/healthz`) expose whether the web container is up and can talk to the database.

### 4.2 Repository layout

The repository adheres to a standard layout that we want to reuse:

- `src/app/` – FastAPI primary backend.
- `src/alt_backends/` – Flask and Express implementations.
- `src/migrations/` – database migrations.
- `tests/` – automated tests.
- `docker/` – Dockerfiles and supporting assets.
- `docker-compose.yml` – orchestration of web and database containers.
- `.env.example` – template for environment configuration.
- [`README.md`](http://README.md) – narrative overview, diagrams, and usage instructions.
- `LICENSE`, `CODE_OF_[CONDUCT.md](http://CONDUCT.md)`, [`CONTRIBUTING.md`](http://CONTRIBUTING.md), [`SECURITY.md`](http://SECURITY.md), `.github/` templates – standard project hygiene.

This layout should be the **default starting point** for similar internal training repos.

## 5. How to Use StudyTracker in Training

StudyTracker is designed to support several training formats.

### 5.1 Onboarding module (2–4 hours)

For new team members, we recommend a focused session:

1. **Orientation (20–30 minutes)** – Review the README, diagrams, and high-level goals.
2. **Bring up the stack (40–60 minutes)** – Configure `.env` and run `docker compose up --build web-fastapi db`; verify `/healthz` and basic endpoints.
3. **Trace a request (30–45 minutes)** – Walk through one or two routes end-to-end (request → route → ORM/model → database → response).
4. **Debrief (15–30 minutes)** – Discuss what felt clear or confusing, and where Docker or database details were surprising.

### 5.2 Deeper architecture workshop (half-day / full-day)

For experienced staff, StudyTracker can anchor a more advanced workshop:

- Compare FastAPI, Flask, and Express implementations of the same surface.
- Explore how tests are wired in and how to extend the suite.
- Experiment with adding a small new feature (for example, basic reporting or tagging).
- Discuss how similar patterns appear in our client systems and internal platforms.

### 5.3 Client enablement

For clients who are learning Docker-first development, StudyTracker can be:

- A **neutral example** that is not tied to their domain but still realistic.
- A **homework or follow-up asset** after architectural workshops.

When used externally, references to internal standards can be trimmed or generalized, but the core patterns remain the same.

## 6. Measuring Learning Outcomes

We recommend a small, practical set of measures when using StudyTracker in structured training:

- **Time to first successful run** – How long it takes participants to go from clone to a successful `/healthz` response using Docker Compose.
- **Time to first meaningful feature** – How long it takes to create and view a topic and session in the UI or API.
- **Error patterns** – The most common setup and runtime issues (for example, environment configuration, Docker networking, migrations).
- **Backend comparison clarity** – Whether participants can explain how FastAPI, Flask, and Express differ and what remains constant.

These metrics can be collected informally (through facilitator observation and debrief) or more formally (through logging and short surveys) depending on the setting.

## 7. Adapting the Pattern to Other Initiatives

StudyTracker should not be a one-off. The same pattern can be applied to other internal projects:

- **Scope Calculator** – A small, Docker-first FastAPI app with Postgres backing, designed as a learning artifact for PCI scoping logic.
- **MCP or API gateways** – Minimal but realistic services that demonstrate gateway patterns, observability, and security controls.
- **Content automation** – Narrow, end-to-end workflows that touch APIs, storage, and background processing.

When creating new training repos:

- Start from the StudyTracker repository layout.
- Preserve multi-modal documentation (diagrams + narrative + walkthroughs).
- Keep the domain as small as possible while still realistic.
- Decide early whether alternate backends are appropriate for that case.

## 8. Recommendations and Next Steps

To make full use of StudyTracker, we recommend:

1. **Adoption** – Treat StudyTracker as a first-class part of onboarding for roles that touch application architecture or Docker.
2. **Maintenance** – Assign an owner or small group to keep the repository current with our evolving best practices (for example, CI patterns, security checks).
3. **Pattern reuse** – Use the StudyTracker layout and standards as the default when starting new internal training repos.
4. **Data collection** – When feasible, capture time-to-first-run, time-to-first-feature, and error patterns in workshops to refine both the artifact and our facilitation.

Over time, we should maintain a small stable of similar artifacts under a common umbrella, each focused on a specific part of our technical stack but sharing the same Titanium 10+ design principles.