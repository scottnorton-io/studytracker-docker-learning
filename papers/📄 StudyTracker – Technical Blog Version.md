# 📄 StudyTracker – Technical Blog Version

# Teaching Docker and Web Architecture with a Tiny Production-Shaped App

Most Docker tutorials I see fall into one of two traps.

On one side are single-image demos: you run a container, print “Hello, world”, maybe mount a volume, and stop there. You learn a few commands, but you never see how a real service hangs together. On the other side are full-stack starter kits and cloud samples that pull in frameworks, databases, and CI before you have a mental model of what is actually running. The result is a lot of complexity and not much understanding.

I wanted something in between: a **tiny but production-shaped app** that teaches containers, a web backend, and a database as a single story. That’s where *StudyTracker* came from.

## A Tiny App with Big Intentions

StudyTracker is deliberately boring in the best way. It does one thing: it tracks learning sessions.

You define topics like “Docker”, “PostgreSQL”, or “FastAPI”. For each topic, you log sessions with a date, a duration in minutes, and some notes. The app shows you your topics and recent sessions in the browser.

That’s it.

Under the hood, though, it looks like a real service:

- A web backend with real routes and templates.
- A PostgreSQL database with a simple but honest schema.
- Docker and Docker Compose for local orchestration.
- A test suite and basic quality tooling.

The point is not the feature set. The point is that this tiny app gives you all the moving parts of a normal web stack without dragging in billing, auth, or five microservices.

## A Docker-First, Multi-Backend Architecture

At runtime, StudyTracker lives entirely inside Docker.

There is a **primary web container** that runs a FastAPI backend. There are **optional alternate web containers** for Flask and Express that implement the same HTTP surface. And there is a **PostgreSQL container** that stores topics and sessions. All containers share a Docker network so they can talk to each other by service name rather than hard-coded IPs.

The Docker Compose file defines four main services:

- `web-fastapi` – the reference backend.
- `web-flask` – a Python alternate.
- `web-express` – a Node.js alternate.
- `db` – PostgreSQL.

In a typical session you pick one backend, bring it up with `db`, and leave the others commented out. The FastAPI + Postgres pair is the default.

Environment configuration lives in `.env`, derived from `.env.example`. A named volume holds the database files. Once you’ve cloned the repo and created your `.env`, one command:

```bash
docker compose up --build web-fastapi db
```

gives you a working stack and a `/healthz` endpoint that tells you if the web container can talk to the database.

## One Domain, Three Views

The data model is small enough to draw on a napkin:

- A **topic** with an id, name, description, and created timestamp.
- A **session** with an id, topic_id, study_date, duration_minutes, notes, and created timestamp.
- One topic has many sessions; each session belongs to exactly one topic.

That relationship stays the same no matter which backend you look at. What changes is how each framework expresses it.

In FastAPI, you see Pydantic models, path operations, and dependency injection. In Flask, you see routes and view functions. In Express, you see middleware, route handlers, and a JavaScript-flavored data-access layer. The HTTP surface is identical:

- `GET /healthz`
- `GET /topics` and `POST /topics`
- `GET /topics/{topic_id}`
- `POST /sessions`

Switching backends doesn’t mean learning a new domain. It just means asking, “How does this framework build the same thing?”

## Teaching the Same System Four Ways

When I put StudyTracker together as a teaching artifact, I wanted it to support multiple ways of learning at once.

- **Visual** – Diagrams show the system context (browser → web container → Postgres), the request lifecycle, and the entity–relationship model. You can see the structure before touching code.
- **Conceptual** – Narrative docs explain the project goals, constraints, and architectural decisions. Before opening an editor, you know what problem the app solves and why it is shaped this way.
- **Procedural** – A step-by-step “recipe” walks through cloning the repo, running Docker Compose, hitting `/healthz`, creating topics and sessions, and running tests. There is always a next step.
- **Comparative** – The multiple backends are there so you can compare frameworks on equal footing. Same routes, same data model, same Docker setup, different ecosystems.

In practice, learners don’t use all four modes equally. Some gravitate to diagrams, some to the terminal, some to reading. The goal is not to force everyone through the same door, but to make sure there is at least one door that feels natural.

## What Worked (and What Surprised Me)

A few patterns have stood out when people work through StudyTracker:

- The **“tiny but real”** domain matters. Because the app isn’t doing billing or auth, people focus on the stack instead of the business logic.
- Having a **single Compose command** that brings up a full stack is a big confidence boost. Getting to a healthy `/healthz` quickly makes Docker feel less mysterious.
- The **alternate backends** turn out to be a powerful comparison tool. Once someone understands the FastAPI version, they can open the Express implementation and say, “Oh, this is the same thing, just written differently.” That shift—from “new framework” to “new view of the same architecture”—is huge.
- Most real friction comes from **environment config and networking**: `.env` issues, compose service names, and database connection strings. That’s useful information. It tells you where to invest in docs and facilitation.

If I were to turn this into a formal study, I would measure:

- Time to first successful stack run.
- Time to first meaningful feature (a topic with a session).
- Common error patterns along the way.
- How well people can explain the differences between the backends afterwards.

Even informally, tracking those four things has been enough to iterate on the docs and the onboarding flow.

## How You Can Reuse This Pattern

You don’t have to use this exact app to benefit from the pattern. The key ingredients are:

1. **A very small, coherent domain** – something you can explain in two sentences.
2. **A Docker-first architecture** – web container + persistence, with Compose as the primary entrypoint.
3. **Multiple implementations of the same API surface** – even just two is enough for comparison.
4. **A GitHub-ready repository** – clear layout, diagrams, README, basic tests, standard project files.
5. **A multi-model teaching design** – visuals, narrative, walkthroughs, and (optionally) comparisons.

Pick a domain your team understands. Choose one primary backend and, if it fits your goals, one alternate. Keep the stack as small as possible, but insist on real packaging and real persistence. Then teach, iterate, and collect just enough data to see where learners struggle.

A tiny, production-shaped app won’t replace deep experience, but it can give people a solid, shared foundation. In my experience, that foundation makes every later conversation about architecture, Docker, or databases much easier.