# 📄 StudyTracker Docker Learning Paper

# A Multi-Backend, Docker-First Learning Exercise for Web Application Architecture

## Abstract

Docker, web application frameworks, and relational databases are now baseline skills for many engineers, yet most tutorials treat them in isolation or as linear, single-stack walkthroughs. This paper presents *StudyTracker*, a deliberately small but production-shaped learning project that combines Docker, a web backend, and PostgreSQL into a cohesive exercise. The project is designed around a FastAPI reference implementation with plug-and-play Flask and Express alternates, all orchestrated via Docker Compose.

The core contribution is a **multi-model teaching design** in which the same concepts are presented visually (Mermaid diagrams), conceptually (architecture narratives and implementation pillars), procedurally (step-by-step "recipes"), and comparatively (multiple backends implementing the same HTTP surface). Learners are guided through three passes: understanding the shape of the system, mapping documentation to repository layout, and comparing backend implementations. A structured milestone and tagging scheme (v0.1.0–v0.5.0) enables incremental adoption and repeatable instruction. Together, these elements support a learning experience that aims for a "code of excellence" standard while remaining small enough to complete as a focused exercise.

## 1. Introduction

Modern application development frequently requires engineers to understand containers, web frameworks, and databases as a single system. However, common tutorials often fall into one of two traps. Some simplify too aggressively, avoiding realistic concerns such as container networks and persistent storage. Others introduce full frameworks or cloud platforms before learners have a firm grasp of fundamentals, leading to a sense of over-complexity and loss of control.

The *StudyTracker* project is designed as a response to these patterns. It provides a small, fully scoped application that nevertheless looks and feels like a real service. The originating brief can be summarized as follows: we are learning Docker; we will architect, design, and build a basic website with database support; the application does not need to be feature-rich, but it must present a meaningful learning opportunity; the full details will be published as a learning GitHub repository; the project should be elevated to a Titanium 10+ Code of Excellence and Standards; the documentation should be enhanced with relevant visuals; and the exact phrasing and intent of this prompt should be preserved.

From this brief, three design constraints emerge. The project must be intentionally minimal in feature set, resisting the temptation to accrete requirements that do not serve the learning goal. The architecture and documentation must meet a high bar of clarity and rigor, consistent with the Titanium 10+ standard. Finally, the project must be publishable and reusable, both as a GitHub repository and as a documented teaching artifact that other instructors and teams can adopt.

The remainder of this paper describes how *StudyTracker* embodies these constraints using a multi-backend, Docker-first architecture and a multi-model teaching approach.

## 2. Design of the Learning Exercise

### 2.1 Application concept: StudyTracker

*StudyTracker* is a deliberately simple web application for logging learning sessions. Learners define topics such as "Docker", "PostgreSQL", or "FastAPI" and record sessions for each topic. A session captures a date, a duration, and free-text notes. The application displays a list of topics and recent sessions, providing a minimal but concrete domain around which to organize the stack.

Although the feature set is small, it is sufficient to introduce the key ingredients of a contemporary web application. Learners see HTTP routing and templated views, rather than working only with command-line examples. They encounter CRUD operations backed by a relational database, rather than a purely in-memory store. They interact with container orchestration for a web tier and a database tier, instead of running everything directly on a host machine. Finally, they work with a test suite and basic quality tooling, reinforcing the idea that even small learning projects can and should be instrumented for correctness and maintainability.

### 2.2 System architecture

At a high level, the system is composed of a web application container, one or more alternate web containers, and a database container, all joined by a shared Docker network. The primary web application container hosts the FastAPI backend. Optional alternate containers run Flask and Express implementations that expose the same HTTP surface. A PostgreSQL container provides persistent storage for topics and sessions, and the Docker network allows containers to communicate by service name rather than by hard-coded IP addresses.

A system context diagram, expressed in Mermaid for documentation purposes, captures this arrangement. It depicts traffic flowing from the learner’s browser to the chosen web container and from there to the PostgreSQL service over the compose network. This diagram serves partly as a navigational aid and partly as a contract: any additional backends or services must fit within this mental model.

### 2.3 Data model

The data model contains two main entities. The first is the topic, which has an identifier, a name, a description, and a timestamp indicating when it was created. The second is the session, which has its own identifier, a foreign key back to the topic, a date representing when the study occurred, a duration in minutes, free-text notes, and a created-at timestamp. This structure expresses a simple one-to-many relationship in which a single topic may have many sessions, and each session belongs to exactly one topic.

An entity–relationship diagram communicates this relationship visually. It becomes the canonical reference for the database schema and the ORM models used by all backends. When learners move between FastAPI, Flask, and Express implementations, the ER diagram anchors their understanding and reduces the perceived cost of switching languages or frameworks.

## 3. Architecture and Repository Structure

### 3.1 Repository layout

The repository layout reinforces the architectural story. At the top level, the `src` directory contains the application code. Within it, an `app` directory holds the FastAPI primary backend, and an `alt_backends` directory holds the Flask and Express implementations. Migrations live alongside the application code so that database evolution is explicit and versioned rather than hidden in ad hoc scripts. A `tests` directory contains automated tests, while a `docker` directory collects Dockerfiles and related assets.

Surrounding this core are files such as `.env.example`, `docker-compose.yml`, `pyproject.toml`, and `package.json`, which describe how to configure, run, and extend the system. A [`README.md`](http://README.md) provides entry-level documentation, and standard project files such as a license, code of conduct, contributing guide, and security policy establish expectations for collaboration and responsible use. Together, these elements make the project discoverable, extensible, and publishable. Developers can infer responsibilities from path names and file names, extend the project without restructuring it, and treat the repository as a first-class artifact rather than a throwaway experiment.

### 3.2 Docker and Compose design

The `docker-compose.yml` file models the primary services needed for the learning exercise. It defines a `web-fastapi` service that mounts the FastAPI application code, a `web-flask` service and a `web-express` service that provide alternate backends, and a `db` service that runs PostgreSQL. In typical use, learners run one web service alongside the database, rather than all three simultaneously. This keeps the runtime environment understandable while still making alternate implementations readily available.

The compose configuration uses service names as stable hostnames on a shared network, so application code can refer to a database host named `db` instead of a fixed IP address. Environment variables configure database credentials and other settings, and a named volume provides persistent storage for database files. Even in a learning context, this arrangement exposes patterns that learners will encounter in production systems.

### 3.3 Backend implementations

Within this architecture, the FastAPI backend serves as the reference implementation. It exposes a small set of endpoints that are sufficient to exercise the system: a health check at `/healthz`, routes to list and create topics, a route to display a topic and its associated sessions, and an endpoint to create new sessions. Flask and Express backends implement the same HTTP surface and operate against the same PostgreSQL database. This deliberate symmetry allows learners to focus on the architectural invariants while noticing how each framework organizes routes, data access, and configuration.

## 4. Multi-Model Teaching Approach

A central design goal of *StudyTracker* is to support multiple learning models simultaneously. At a Titanium 10+ standard, the learning experience must be explicitly multi-modal, intentionally sequenced, and directly implementable from the accompanying repository rather than relying on implicit instructor knowledge.

From a visual standpoint, the project provides diagrams that show the system context, the request lifecycle, and the entity–relationship structure. These diagrams are treated not as decorative elements but as first-class explanations that can be cross-referenced with the code and configuration.

Conceptually, the documentation introduces the overall project goals, the *StudyTracker* domain, and a set of implementation pillars that frame the exercise: repository organization, Docker and Compose, backends, and testing and quality. Before touching code, learners are invited to form a mental model of what the system is and why it was shaped this way.

Procedurally, the project guides learners through a series of concrete steps. They begin by reading the overview and examining the diagrams. They then bring the stack to life by running the appropriate Docker Compose command, verify that the health check responds as expected, and focus on implementing and exercising a minimal set of endpoints. As they progress, they add sessions, run tests, and eventually swap backends to experience the same surface through different implementations.

Comparatively, the exercise encourages learners to treat FastAPI, Flask, and Express as alternate lenses on the same architecture. When they switch backends, they do not encounter a new domain or a new deployment topology; instead, they see how different ecosystems express familiar patterns. This comparative mode is particularly valuable for teams who work across languages or who need to evaluate framework choices.

## 5. Implementation Summary

The implementation of *StudyTracker* is intentionally compact. Across all backends, the surface area of the application remains consistent: a health check endpoint, routes to list and create topics, a route to view a topic with its sessions, and a route to create new sessions. The tests directory contains pytest suites that exercise these behaviors, and the project relies on common Python tooling such as `black`, `isort`, and `flake8` to maintain code quality.

Rather than serving as a full code listing, the implementation summary functions as a narrative index. It tells readers what kinds of behaviors exist, where to find them, and how they relate to the diagrams and learning objectives introduced earlier in the paper. A reader interested in the HTTP surface can move directly from this section to the relevant routes. An instructor designing a workshop can map these behaviors to exercises and checkpoints. A learner who has just completed the basic flows can use this section to verify that they have touched all of the major components.

## 6. Reflections and Evaluation

This section aligns with the publication outline’s emphasis on reflection and evaluation. It considers both the subjective experience of working through the exercise and the more objective measures that can be used to assess its effectiveness.

Qualitatively, the *StudyTracker* exercise appears to reduce cognitive overload by keeping the domain intentionally simple while still modeling realistic concerns. Learners are not asked to reason about billing systems, multi-tenant access control, or complex workflows. Instead, they focus on topics and sessions, which are easy to grasp and reason about. Within this constrained domain, however, they encounter genuine engineering concerns such as container networking, environment configuration via `.env` files, multi-service orchestration in Docker Compose, and the discipline of keeping tests and tooling in step with the code.

Reports from early use suggest that this balance of simplicity and realism makes it easier for learners to understand how the pieces of the system fit together. They find it more natural to connect the diagrams to specific files and services, and they are more willing to experiment with swapping backends or modifying the compose configuration because the blast radius feels contained. The presence of multiple backends, in particular, appears to improve the transfer of concepts across languages and frameworks. Once learners have a solid grasp of the FastAPI implementation, they are able to recognize equivalent routes and data access patterns in Flask and Express and to articulate how the frameworks differ in ergonomics rather than in fundamental capability.

From an evaluation standpoint, the project lends itself to several practical metrics. One useful measure is the time required to achieve a first successful run of the stack, defined as the interval between cloning the repository and receiving a healthy response from the `/healthz` endpoint while running the prescribed Docker Compose command. Another is the time required to achieve a first meaningful feature, such as creating a topic and a session and observing them in the application’s interface. Patterns in the kinds of errors that occur along the way—for example, missing environment variables, container build failures, or database connection issues—provide insight into where learners struggle and where documentation or scaffolding might need to be strengthened.

Even when formal data collection is not feasible, the exercise supports structured debriefs. Instructors can ask learners which parts of the stack felt most confusing and why, which diagrams were most helpful, and how the presence of multiple backends affected their understanding of the architecture. Answers to these questions can be captured as part of a retrospective or teaching evaluation and can guide future refinements of the project.

## 7. Discussion and Future Work

Although *StudyTracker* is anchored in a specific stack, the underlying pattern is intentionally generic. The combination of a small but coherent domain, a Docker-first architecture, multiple backends that share a surface, and a publication-quality repository can be applied to other languages and frameworks. For example, an instructor might replace the FastAPI reference implementation with a Django application or a Go HTTP service, provided that the application preserves the same routes and data model. In doing so, they would keep the cognitive benefits of the *StudyTracker* design while tailoring the exercise to a different ecosystem.

The multi-model approach described earlier can also be extended. Additional diagrams, such as deployment diagrams or observability flows, would enable learners to reason about production-like concerns such as scaling, monitoring, and failure modes without significantly expanding the feature set. The same is true for operational practices. Integrating continuous integration workflows for tests and linting, adding container and dependency security scans, and introducing basic observability patterns such as health checks and structured logging would move the project closer to production reality while retaining its focus on learnability.

Future work may also explore the addition of extra backends or limited integrations. A simple background worker, a reporting endpoint, or a small front-end variation could open new learning avenues for intermediate or advanced cohorts. The central question, from a teaching perspective, is how far to push production realism before the cognitive load outweighs the benefits. Each new component introduces both an opportunity and a cost. Iterative experimentation with different configurations, paired with the evaluation practices described above, can help locate a sensible boundary.

## 8. Appendix

### 8.1 Tag map from v0.1.0 to v0.5.0

The repository uses a simple tagging scheme to make the evolution of the project visible and to give instructors and learners clear stopping points. An early tag such as v0.1.0 represents the skeleton of the system and a functioning health check. At this stage, the repository layout is in place, the compose file defines the web and database services, and the `/healthz` endpoint responds successfully. A subsequent tag, v0.2.0, introduces the core of the domain by adding the topic and session data model, the routes needed to create and list these entities, and minimal presentation logic to make the results visible.

A third tag in the sequence, v0.3.0, establishes a baseline for testing and quality. Pytest suites exercise the main behaviors, and formatting and linting tools such as `black`, `isort`, and `flake8` are integrated into the workflow. Documentation, including the [`README.md`](http://README.md), is updated to describe how to run tests and interpret their results. The next tag, v0.4.0, introduces the alternate backends. At this point, Flask and Express implementations join the FastAPI reference, all sharing the same database schema and migrations. Documentation now includes a comparative discussion of framework structure and ergonomics.

The v0.5.0 tag marks the point at which the repository becomes fully publication-ready. Standard GitHub assets such as the license, code of conduct, contributing guide, and security policy are in place, and issue and pull request templates are available to support structured collaboration. Diagrams have been embedded or linked from the [`README.md`](http://README.md), and the documentation provides clear, end-to-end instructions for cloning, running, and extending the project. Instructors can choose to stop at any of these tags depending on the time available and the depth of the course, and learners can use the tags as milestones to track their own progress.

### 8.2 The "Follow the recipe" checklist as a teaching aid

Alongside the repository and this paper, the project provides a compact teaching aid informally referred to as the "Follow the recipe" checklist. Rather than existing as a standalone artifact, it mirrors the structure of the exercise and serves as a narrative companion. The checklist begins with a simple invitation to clone the repository, open it in an editor, and skim the top-level files. Learners are encouraged to treat the [`README.md`](http://README.md), the compose file, and the project configuration files as signals of intent rather than as noise.

The checklist then directs attention to the architecture. Learners review the system context, sequence, and ER diagrams and are asked to identify the main services and how they communicate. Only after this orientation do they move on to running the baseline stack. At that point they copy `.env.example` to `.env`, adjust any required variables, and start the FastAPI and database services with Docker Compose. A successful health check confirms that the system is alive.

Subsequent steps in the checklist invite learners to exercise the core features by creating topics and sessions and verifying that they appear as expected. They then explore tests and quality tooling by running the test suite in a container and inspecting any failures. Once they are comfortable with the reference implementation, they switch to one of the alternate backends and repeat the same flows, paying attention to both similarities and differences. The final steps ask learners to reflect on what surprised them, which parts of the stack felt most and least clear, and what small extension or refactor they would attempt next.

In this way, the checklist reinforces the narrative of the paper without fragmenting the experience into isolated bullet points. It keeps the exercise grounded in a sequence of concrete actions while preserving the sense that learners are engaging with a coherent, story-like system rather than a disconnected set of tasks.

## 9. Conclusion

*StudyTracker* demonstrates that a small, well-structured project can teach Docker, web development, and database fundamentals without overwhelming learners. By combining a constrained domain with a Docker-first architecture, multiple backends that share a common surface, and a publication-quality repository, the project turns a single exercise into a reusable learning artifact. The multi-model approach, spanning visual, conceptual, procedural, and comparative modes, allows different kinds of learners to find an entry point that makes sense for them.

The refinements described in this paper—explicit evaluation criteria, a transparent tag map, and a narrative "Follow the recipe" aid—are intended to make the exercise easier to adopt in structured settings and to give instructors levers for tuning depth and pace. As teams adapt the pattern to new stacks and extend it with additional operational realism, the underlying principle remains the same: a thoughtfully designed, production-shaped learning project can provide a clearer path to mastery than a sequence of isolated tutorials.