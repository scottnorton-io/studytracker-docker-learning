# 📄 StudyTracker – Journal Article Version

# A Multi-Backend, Docker-First Learning Artifact for Teaching Web Application Architecture

## Abstract

Containers, web application frameworks, and relational databases are now baseline skills for many engineers, yet most introductory materials treat them in isolation or as linear, single-stack walkthroughs. This article presents *StudyTracker*, a deliberately small but production-shaped learning artifact that combines Docker, a web backend, and PostgreSQL into a cohesive exercise. The project is designed around a FastAPI reference implementation with plug-and-play Flask and Express alternates, all orchestrated via Docker Compose, and is distributed as a GitHub-ready repository.

The core contribution is a **multi-model teaching design** in which the same concepts are presented visually (Mermaid diagrams), conceptually (architecture narratives and implementation pillars), procedurally (step-by-step “recipes”), and comparatively (multiple backends implementing the same HTTP surface). Learners are guided through three passes: understanding the shape of the system, mapping documentation to repository layout, and comparing backend implementations. A structured milestone and tagging scheme (v0.1.0–v0.5.0) enables incremental adoption and repeatable instruction.

We describe the context and motivation for the artifact, its design and implementation, and an evaluation framework based on measures such as time to first successful stack run, time to first meaningful feature, and error-pattern distribution. We outline initial observations from early deployments and discuss threats to validity, implications for teaching container-based web architecture, and directions for future empirical study.

## 1. Introduction

Modern software development frequently requires engineers to reason about containers, web frameworks, and relational databases as a single system rather than as isolated technologies. However, many learning resources separate these concerns. Docker tutorials often focus on individual commands or simple images. Framework-specific “getting started” guides emphasize application code while assuming a preconfigured database and environment. Cloud-centric samples foreground deployment pipelines before learners have a firm grasp of the services they are deploying.

Such materials can be effective for introducing individual tools, but they often fail to convey how containers, web backends, and databases interact in practice. Learners may acquire fragmented knowledge that does not transfer easily to real projects. In particular, they may struggle to understand how a small service is packaged, configured, and connected to persistence within a multi-service environment.

*StudyTracker* was developed in response to these challenges. The artifact is a small but production-shaped web application designed specifically as a learning exercise. The application supports logging learning sessions by topic and is implemented as a Docker-first system with a FastAPI reference backend and alternate Flask and Express implementations, all sharing a PostgreSQL database. The associated repository includes architecture diagrams, narrative documentation, tests, and standard project assets, with the explicit intention that instructors can reuse it with minimal adaptation.

The central question guiding this work is:

> How can a small, production-shaped project be structured to teach containers, web frameworks, and databases as a coherent system without overwhelming learners?
> 

This article makes three contributions. First, it presents the design of the *StudyTracker* artifact, including its domain, architecture, and repository structure. Second, it proposes an evaluation framework that operationalizes practical measures of learner progress. Third, it reports preliminary observations from early deployments and discusses how this pattern may generalize to other stacks and contexts.

## 2. Context and Motivation

The artifact was developed in an applied training setting where engineers and practitioners needed to build confidence with Docker-first development and web application architecture. Participants often arrived with experience in one part of the stack—for example, application code without containers, or database skills without exposure to orchestrated services—but lacked practice reasoning about the system as a whole.

Several constraints shaped the design. Learning activities were time-boxed to sessions ranging from a few hours to a few days. Participants worked on laptops with Docker available but without uniform prior configuration of databases or language environments. The goal was not merely to run a prebuilt image, but to connect documentation, diagrams, code, and runtime behavior in a way that would transfer to future projects.

Within this context, three design principles emerged:

1. **Intentional minimalism in the domain**: The application must be simple enough that domain details do not dominate cognitive load.
2. **Publication-level clarity in architecture and documentation**: The artifact should model good practice, not only in code but also in structure, naming, and explanatory material.
3. **Reusability as a portable learning asset**: The repository should be self-contained, versioned, and understandable without access to the original author.

These principles informed choices about the application concept, architectural topology, and the way the repository is organized.

## 3. Design of the Learning Artifact

### 3.1 Application concept and learning objectives

At the application level, *StudyTracker* is a deliberately simple system for logging learning sessions. Users define topics such as “Docker”, “PostgreSQL”, or “FastAPI” and record sessions for each topic with a date, duration, and notes. The application displays a list of topics and recent sessions. This small domain supports a clear set of learning objectives without requiring a complex business model.

By the end of the exercise, learners should be able to:

- Explain the overall structure of a containerized web application that uses a relational database.
- Run the application locally using Docker Compose and interpret basic container logs.
- Trace a request from the browser through the web backend to the database and back.
- Modify or add routes in at least one backend implementation.
- Compare implementations of the same HTTP surface across FastAPI, Flask, and Express.

These objectives map directly onto the architectural and repository choices described below.

### 3.2 System architecture

The system consists of three main components: a web application container, optional alternate web containers, and a database container, all connected via a shared Docker network. The primary web application container hosts a FastAPI backend. Alternate containers host Flask and Express implementations that expose the same endpoints. A PostgreSQL container provides persistent storage.

A system context diagram captures the following relationships:

- The client (a browser) issues HTTP requests to a web container running on the learner’s machine.
- The web container connects to the PostgreSQL container using service-name-based addressing within the Compose network.
- Alternate backends can be started by enabling the corresponding services in the Compose configuration while still targeting the same database.

This topology is intentionally modest but realistic. It demonstrates networked services, environment configuration, and persistent storage without introducing additional tiers such as message brokers or caching layers.

### 3.3 Data model

The data model comprises two entities. A *topic* represents a subject of study and includes an identifier, a name, a description, and a creation timestamp. A *session* represents an individual learning episode and includes its own identifier, a foreign key to the associated topic, a study date, duration in minutes, free-text notes, and a creation timestamp. The relationship is one-to-many: each topic can have many sessions; each session belongs to exactly one topic.

An entity–relationship diagram formalizes this relationship and serves as a shared reference for backend implementations and database migrations. Maintaining a single, technology-agnostic description of the model helps learners see consistency across frameworks.

## 4. Implementation and Repository Structure

### 4.1 Repository layout

The repository is organized to make architectural boundaries visible. The `src` directory contains application code. Within it, an `app` directory holds the FastAPI reference implementation, and an `alt_backends` directory contains separate subdirectories for Flask and Express. Database migrations are located alongside the relevant code to keep schema evolution explicit. A `tests` directory holds automated tests, and a `docker` directory contains Dockerfiles and related assets.

Top-level files include `.env.example`, `docker-compose.yml`, `pyproject.toml`, and `package.json`, which together define how the system is built and run. A [`README.md`](http://README.md) provides a guided introduction, while standard project files such as a license, code of conduct, contributing guide, and security policy model best practices for repository hygiene.

This structure is intended to be discoverable. Directory and file names convey responsibilities, and cross-references from the documentation to specific paths help learners connect conceptual explanations to concrete locations in the codebase.

### 4.2 Docker and Compose design

The `docker-compose.yml` configuration defines four primary services: `web-fastapi`, `web-flask`, `web-express`, and `db`. In typical use, learners run one web service alongside the database rather than all three at once. Each web service has its own build context and Dockerfile, but all share a network and connect to the same PostgreSQL container using environment variables for host, port, database name, and credentials.

A named Docker volume provides persistence for database files. Environment variables are managed via an `.env` file derived from `.env.example`, encouraging learners to separate configuration from code. With this arrangement, a single command such as `docker compose up --build web-fastapi db` can build and run the primary stack. The same pattern applies when swapping to Flask or Express.

### 4.3 Backend implementations

The FastAPI backend functions as the reference implementation. It exposes endpoints for health checks, topic listing and creation, viewing a topic with its sessions, and creating sessions. The Flask and Express backends implement the same HTTP surface and operate on the same database schema.

This deliberate symmetry is pedagogically significant. It allows instructors to analyze how different frameworks express identical behavior while holding the domain and architecture constant. Learners can open corresponding route handlers in each backend to compare control flow, data validation, and error handling styles.

### 4.4 Testing and quality tooling

The repository includes a basic but functional test suite implemented with pytest. Tests cover core behaviors such as health checks, topic creation, and session creation. Python tooling such as `black`, `isort`, and `flake8` is integrated into the development workflow, and analogous practices can be applied to the Express codebase.

The intent is not to provide exhaustive test coverage, but to demonstrate how even a small learning project can incorporate automated checks and consistent formatting. This reinforces the idea that production discipline is compatible with teaching artifacts.

## 5. Evaluation Framework and Methodology

To evaluate *StudyTracker* as a learning artifact, we define a framework grounded in observable learner actions and outcomes. The framework is designed to be practical in instructional settings while allowing for more systematic data collection in future studies.

### 5.1 Metrics

We focus on four categories of measures:

- **Time to first successful run (T1)**: the elapsed time between learners cloning the repository and successfully running the prescribed Docker Compose command with a healthy response from the health-check endpoint.
- **Time to first meaningful feature (T2)**: the elapsed time between cloning and successfully creating and viewing a topic and session in the application interface.
- **Error-pattern distribution (E)**: the frequency and nature of setup and runtime errors, including missing environment variables, container build failures, database connection issues, and route or schema errors.
- **Backend comparison outcomes (B)**: learners’ ability to articulate similarities and differences between backend implementations of the same HTTP surface, assessed through short written or oral explanations.

These metrics balance quantitative and qualitative aspects. T1 and T2 capture broad efficiency, while E and B provide insight into where conceptual and practical difficulties arise.

### 5.2 Data collection

In an instrumented deployment, T1 and T2 can be captured by scripts that log timestamps when key actions occur, such as the first successful health-check request or the first successful creation of a session. Error patterns can be collected from container logs and from simple reporting forms where learners categorize the issues they encountered.

Backend comparison outcomes can be assessed through short, structured prompts. For example, learners might be asked to describe how route definitions and database access differ between FastAPI and Express while serving the same endpoint, or to identify which framework made specific concerns (such as data validation) more explicit.

In smaller or less formal settings, instructors can approximate this data through direct observation and debrief sessions, using the same categories to guide discussion.

### 5.3 Study designs

Several study designs are possible. One straightforward approach is a single-group observation in which a cohort works through *StudyTracker* and metrics are collected for descriptive analysis. A more rigorous design would involve a comparison between *StudyTracker* and an alternative learning path, such as a traditional sequence of Docker and framework tutorials, with cohorts assigned to each condition.

In either case, the evaluation framework is intended to be reusable. Instructors at different institutions or organizations can adopt the artifact and collect T1, T2, E, and B data under their own constraints, enabling meta-analysis across settings.

## 6. Results and Interpretation (Preliminary)

At the time of writing, systematic data collection is ongoing. However, initial deployments of *StudyTracker* in small, practice-oriented cohorts provide qualitative indications of its impact.

Learners report that the constrained domain makes the exercise approachable. They describe the system as “small enough to finish” while still feeling “like a real app.” They also note that the presence of diagrams and a clear repository layout helps them navigate unfamiliar parts of the stack more confidently.

Informal tracking of T1 and T2 suggests that most learners can achieve a first successful stack run within a short period once basic Docker installation issues are resolved. Variability in T2 is higher and appears to be influenced by prior familiarity with the chosen backend framework. Error patterns are concentrated around environment configuration and understanding Compose service naming, which in turn informs improvements to documentation.

When asked to compare backends, learners are generally able to identify commonalities in routes and data model usage. Their comments highlight differences in ergonomics and structure rather than semantics, indicating that the exercise encourages them to think in terms of architecture and behavior rather than language-specific syntax alone.

These observations are tentative but consistent with the design goals of the artifact. They suggest that the pattern may help learners form a coherent mental model of the system and transfer that model across frameworks.

## 7. Discussion

The *StudyTracker* artifact embodies a particular philosophy of teaching web application architecture and container-based deployment. It treats a small, coherent project as a central organizing object and uses architecture diagrams, narrative documentation, and repository structure to make the system’s shape explicit. Multiple backends act as lenses through which learners can view the same architecture from different language and framework perspectives.

From an instructional standpoint, this approach has several advantages. It reduces context switching between disparate tutorials, concentrates practice on a single domain, and models realistic project hygiene. It also supports learners who prefer different modalities by providing visual, conceptual, procedural, and comparative entry points.

At the same time, the design involves trade-offs. Focusing on a single domain and topology may underserve learners who need exposure to a broader variety of patterns. Leaning on Docker and PostgreSQL assumes access to suitable hardware and permissions. The inclusion of multiple backends introduces additional complexity that may not be necessary for all audiences.

These trade-offs suggest that *StudyTracker* is best understood as a reusable pattern rather than a universal solution. Instructors can adopt the pattern and adjust the specifics—domain, frameworks, persistence technology—while keeping the core idea of a small, production-shaped artifact that is carefully documented and instrumented for learning.

## 8. Threats to Validity

Several threats to validity limit the conclusions that can be drawn from the current state of the work.

- **Internal validity**: Without randomized assignment or carefully matched comparison groups, it is difficult to attribute improvements in learner performance solely to the artifact. Instructor expertise, cohort composition, and prior exposure to related technologies may confound results.
- **External validity**: The artifact was developed within a particular organizational context and with specific constraints. Results from one setting may not generalize directly to other institutions, learner populations, or technology stacks.
- **Construct validity**: The chosen metrics, while practical, are indirect measures of learning. Faster times to first run or first feature may reflect improved documentation or tooling rather than deeper understanding. Self-reported comfort with containers and architecture may not align perfectly with actual performance in new tasks.
- **Conclusion validity**: With small sample sizes and informal observation in early deployments, there is a risk of overinterpreting patterns or underestimating variability.

These threats do not negate the potential value of the artifact, but they highlight the need for careful study design and cautious interpretation of results.

## 9. Conclusion

*StudyTracker* demonstrates how a small, production-shaped project can be structured as a multi-backend, Docker-first learning artifact for web application architecture. By combining a constrained domain with a carefully documented architecture, multiple backend implementations, a GitHub-ready repository, and a multi-modal teaching design, the artifact seeks to bridge the gap between toy examples and over-complex starter kits.

The evaluation framework and preliminary observations suggest that this pattern can support learners in forming a coherent mental model of containers, web backends, and databases as a single system. At the same time, the current evidence is preliminary, and further empirical work is needed to quantify its impact and explore its generalizability.

Future research will focus on deploying *StudyTracker* and related artifacts in more diverse settings, collecting comparable metrics across cohorts, and refining the pattern in response to both quantitative and qualitative feedback. More broadly, the work points toward a class of teaching artifacts that are intentionally designed to be both production-shaped and pedagogy-aware, providing a path for learners to move from isolated tutorials to integrated architectural thinking.