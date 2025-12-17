# 📄 StudyTracker – Conference Paper Version

# StudyTracker: A Multi-Backend, Docker-First Learning Exercise for Web Application Architecture

## Abstract

Containers, web application frameworks, and relational databases are now baseline skills for many engineers, yet most introductory materials treat them in isolation or as linear, single-stack walkthroughs. This paper presents *StudyTracker*, a deliberately small but production-shaped learning project that combines Docker, a web backend, and PostgreSQL into a cohesive exercise. The project is designed around a FastAPI reference implementation with plug-and-play Flask and Express alternates, all orchestrated via Docker Compose.

The core contribution is a **multi-model teaching design** in which the same concepts are presented visually (Mermaid diagrams), conceptually (architecture narratives and implementation pillars), procedurally (step-by-step “recipes”), and comparatively (multiple backends implementing the same HTTP surface). Learners are guided through three passes: understanding the shape of the system, mapping documentation to repository layout, and comparing backend implementations. A structured milestone and tagging scheme (v0.1.0–v0.5.0) enables incremental adoption and repeatable instruction. Together, these elements support a learning experience that aims for a "code of excellence" standard while remaining small enough to complete as a focused exercise.

## 1. Introduction

Modern application development frequently requires engineers to understand containers, web frameworks, and databases as a single system. However, the tutorials and example projects that learners encounter often fall into one of two traps. Some simplify too aggressively, avoiding realistic concerns such as container networking, environment configuration, and persistence. Others introduce full frameworks or cloud platforms before learners have a firm grasp of fundamentals, leading to over-complexity and a loss of control.

The *StudyTracker* project is designed as a response to these patterns. It provides a small, fully scoped application that nevertheless looks and feels like a real service. The originating brief can be summarized as follows: we are learning Docker; we will architect, design, and build a basic website with database support; the application does not need to be feature-rich, but it must present a meaningful learning opportunity; the full details will be published as a learning GitHub repository; the project should be elevated to a Titanium 10+ Code of Excellence and Standards; the documentation should be enhanced with relevant visuals; and the exact phrasing and intent of this prompt should be preserved.

From this brief, three design constraints emerge. The project must be intentionally minimal in feature set, resisting the temptation to accrete requirements that do not serve the learning goal. The architecture and documentation must meet a high bar of clarity and rigor, consistent with the Titanium 10+ standard. Finally, the project must be publishable and reusable, both as a GitHub repository and as a documented teaching artifact that other instructors and teams can adopt.

The research and practice question this paper addresses is:

> How can a small, production-shaped project be structured to teach containers, web frameworks, and databases as a coherent system without overwhelming learners?
> 

We answer this question by presenting the design of *StudyTracker*, a Docker-first, multi-backend learning exercise, and by outlining an evaluation framework and early observations from its use.

## 2. Background and Related Work

Teaching modern web application architecture often involves a tension between realism and cognitive load. On one end of the spectrum, single-service “Hello, world” examples fail to expose learners to the realities of container networking, persistent storage, and cross-service configuration. On the other end, full-stack starter kits and production frameworks can introduce a volume of incidental complexity that obscures basic concepts.

Existing materials in DevOps and web development education commonly follow one of three patterns: stepwise Docker tutorials centered on individual commands, framework-specific starter applications that assume prior knowledge of containers and databases, and cloud-centric samples that focus on deployment pipelines before learners understand the services they are deploying. These approaches are valuable, but they often treat containers, web frameworks, and databases as separate episodes rather than as a single architectural story.

In parallel, CS and software engineering education has explored **multi-modal teaching**: presenting concepts visually, conceptually, procedurally, and comparatively to support different learning styles. However, many such efforts focus on algorithmic or language fundamentals rather than on the practical integration of infrastructure, application code, and data stores.

*StudyTracker* sits at the intersection of these concerns. It adopts a deliberately small domain and a Docker-first architecture, but it also uses a multi-model teaching design and a GitHub-ready artifact to support reuse. The design aims to occupy the space between toy examples and overbuilt “real” applications: realistic enough to teach production-shaped thinking, but constrained enough to be learnable in a short, structured exercise.

## 3. Design of the Learning Exercise

### 3.1 Application concept

At its core, *StudyTracker* is a simple web application for logging learning sessions. Learners define topics such as “Docker”, “PostgreSQL”, or “FastAPI” and record sessions for each topic. A session captures a date, a duration, and free-text notes. The application displays a list of topics and recent sessions, providing a minimal but concrete domain around which to organize the stack.

This feature set is intentionally small but sufficient to introduce key ingredients of a contemporary web application. Learners see HTTP routing and templated views rather than working only with command-line examples. They encounter CRUD operations backed by a relational database rather than a purely in-memory store. They interact with container orchestration for a web tier and a database tier instead of running everything directly on a host machine. Finally, they work with a test suite and basic quality tooling, reinforcing the idea that even small learning projects can and should be instrumented for correctness and maintainability.

### 3.2 System architecture

At a high level, the system is composed of a web application container, one or more alternate web containers, and a database container, all joined by a shared Docker network. The primary web application container hosts the FastAPI backend. Optional alternate containers run Flask and Express implementations that expose the same HTTP surface. A PostgreSQL container provides persistent storage for topics and sessions, and the Docker network allows containers to communicate by service name rather than by hard-coded IP addresses.

A system context diagram, expressed in Mermaid, captures this arrangement. It depicts traffic flowing from the learner’s browser to the chosen web container and from there to the PostgreSQL service over the compose network. This diagram serves partly as a navigational aid and partly as a contract: any additional backends or services must fit within this mental model.

### 3.3 Data model

The data model contains two main entities. The first is the topic, which has an identifier, a name, a description, and a timestamp indicating when it was created. The second is the session, which has its own identifier, a foreign key back to the topic, a date representing when the study occurred, a duration in minutes, free-text notes, and a created-at timestamp. This structure expresses a simple one-to-many relationship in which a single topic may have many sessions, and each session belongs to exactly one topic.

An entity–relationship diagram communicates this relationship visually. It becomes the canonical reference for the database schema and the ORM models used by all backends. When learners move between FastAPI, Flask, and Express implementations, the ER diagram anchors their understanding and reduces the perceived cost of switching languages or frameworks.

## 4. Implementation and Teaching Modality

### 4.1 Repository and container structure

The repository layout reinforces the architectural story. At the top level, the `src` directory contains the application code. Within it, an `app` directory holds the FastAPI primary backend, and an `alt_backends` directory holds the Flask and Express implementations. Migrations live alongside the application code so that database evolution is explicit and versioned rather than hidden in ad hoc scripts. A `tests` directory contains automated tests, while a `docker` directory collects Dockerfiles and related assets.

Surrounding this core are files such as `.env.example`, `docker-compose.yml`, `pyproject.toml`, and `package.json`, which describe how to configure, run, and extend the system. A [`README.md`](http://README.md) provides entry-level documentation, and standard project files such as a license, code of conduct, contributing guide, and security policy establish expectations for collaboration and responsible use. Together, these elements make the project discoverable, extensible, and publishable.

The `docker-compose.yml` file models the primary services needed for the learning exercise. It defines a `web-fastapi` service that mounts the FastAPI application code, a `web-flask` service and a `web-express` service that provide alternate backends, and a `db` service that runs PostgreSQL. In typical use, learners run one web service alongside the database rather than all three simultaneously, keeping the runtime environment understandable while still making alternate implementations readily available.

The compose configuration uses service names as stable hostnames on a shared network, so application code can refer to a database host named `db` instead of a fixed IP address. Environment variables configure database credentials and other settings, and a named volume provides persistent storage for database files. Even in a learning context, this arrangement exposes patterns that learners will encounter in production systems.

Within this architecture, the FastAPI backend serves as the reference implementation. It exposes a small set of endpoints that are sufficient to exercise the system: a health check at `/healthz`, routes to list and create topics, a route to display a topic and its associated sessions, and an endpoint to create new sessions. Flask and Express backends implement the same HTTP surface and operate against the same PostgreSQL database. This deliberate symmetry allows learners to focus on the architectural invariants while noticing how each framework organizes routes, data access, and configuration.

### 4.2 Multi-model teaching design

A central design goal of *StudyTracker* is to support multiple learning models simultaneously. At a Titanium 10+ standard, the learning experience must be explicitly multi-modal, intentionally sequenced, and directly implementable from the accompanying repository rather than relying on implicit instructor knowledge.

From a visual standpoint, the project provides diagrams that show the system context, the request lifecycle, and the entity–relationship structure. These diagrams are treated not as decorative elements but as first-class explanations that can be cross-referenced with the code and configuration.

Conceptually, the documentation introduces the overall project goals, the *StudyTracker* domain, and a set of implementation pillars that frame the exercise: repository organization, Docker and Compose, backends, and testing and quality. Before touching code, learners are invited to form a mental model of what the system is and why it was shaped this way.

Procedurally, the project guides learners through a series of concrete steps. They begin by reading the overview and examining the diagrams. They then bring the stack to life by running the appropriate Docker Compose command, verify that the health check responds as expected, and focus on implementing and exercising a minimal set of endpoints. As they progress, they add sessions, run tests, and eventually swap backends to experience the same surface through different implementations.

Comparatively, the exercise encourages learners to treat FastAPI, Flask, and Express as alternate lenses on the same architecture. When they switch backends, they do not encounter a new domain or a new deployment topology; instead, they see how different ecosystems express familiar patterns. This comparative mode is particularly valuable for teams who work across languages or who need to evaluate framework choices.

## 5. Evaluation Framework and Preliminary Observations

### 5.1 Evaluation framework

To assess the effectiveness of *StudyTracker* as a learning artifact, we define an evaluation framework centered on a small set of practical metrics:

- **Time to first successful run**: the elapsed time from cloning the repository to receiving a healthy response from the `/healthz` endpoint while running the prescribed Docker Compose command.
- **Time to first meaningful feature**: the elapsed time from clone to successful creation and display of a topic and session in the application’s interface.
- **Error-pattern distribution**: the types and frequencies of setup and runtime errors encountered along the way, such as missing environment variables, container build failures, or database connection issues.
- **Backend comparison outcomes**: learners’ ability to explain key similarities and differences between FastAPI, Flask, and Express implementations of the same HTTP surface.

These metrics can be captured via instrumented scripts, logs, and short post-exercise surveys. Even when full instrumentation is not available, instructors can approximate them through observation and structured debrief questions.

### 5.2 Preliminary observations

Although formal controlled studies are still in progress, early use of *StudyTracker* in small cohorts has yielded several qualitative observations. Learners report that the constrained domain makes it easier to understand how the pieces of the system fit together. They find it more natural to connect diagrams to specific files and services, and they express less anxiety about experimenting with Docker and compose once the health check is working.

The presence of multiple backends appears to improve the transfer of concepts across languages and frameworks. Once learners achieve fluency with the FastAPI implementation, they can more readily recognize equivalent routes and data access patterns in Flask and Express, and they describe the differences between frameworks in terms of ergonomics and organization rather than capability.

Instructors, in turn, find that the proposed metrics align with visible difficulties. Long times to first successful run correlate with environment and networking issues, suggesting that additional scaffolding is needed around `.env` configuration and container logs. Difficulties in articulating backend differences point toward opportunities to strengthen the comparative narrative.

## 6. Discussion and Limitations

*StudyTracker* illustrates one way to align a small but realistic application with multi-modal teaching and a Docker-first architecture. The pattern appears to help learners form a coherent mental model of a multi-service system without overwhelming them with incidental complexity. It also provides a concrete artifact that instructors can reuse and adapt for different audiences.

However, several limitations remain. First, the current evaluation evidence is preliminary and based on relatively small, self-selected cohorts. The absence of a control group using traditional tutorials limits the strength of causal claims about learning outcomes. Second, the design reflects the needs and context of a specific organization with an existing Docker-first philosophy and may require adjustment in other settings. Third, the metrics proposed, while practical, are imperfect proxies for deeper understanding; reductions in time to first run, for example, may reflect improved documentation as much as improved conceptual grasp.

Despite these limitations, the pattern offers a foundation for more systematic study. The combination of a clearly defined artifact, a concrete evaluation framework, and a set of preliminary observations positions *StudyTracker* as a candidate for future comparative work.

## 7. Future Work

Future work will proceed along three main lines. The first is formal evaluation: deploying *StudyTracker* and comparable alternatives across multiple cohorts, collecting the metrics described above, and analyzing the results to quantify its impact on learner performance and confidence.

The second is pattern generalization. The same structure—a small, coherent domain; a Docker-first architecture; multiple backends sharing a surface; and a GitHub-ready repository—can be applied to other languages and frameworks. For example, instructors might define a Django or Go-based version of the exercise that preserves the HTTP surface and data model while broadening the set of ecosystems represented.

The third is operational realism. Integrating continuous integration workflows for tests and linting, adding container and dependency security scans, and introducing basic observability patterns such as health checks and structured logging would move the project closer to production norms. Careful evaluation would be needed to ensure that these additions do not overwhelm learners or obscure the core lessons.

## 8. Conclusion

*StudyTracker* demonstrates that a small, well-structured project can teach Docker, web development, and database fundamentals without overwhelming learners. By combining a constrained domain with a Docker-first architecture, multiple backends that share a common surface, and a publication-quality repository, the project turns a single exercise into a reusable learning artifact. The multi-model approach—spanning visual, conceptual, procedural, and comparative modes—allows different kinds of learners to find an entry point that makes sense for them.

The evaluation framework and preliminary observations presented here suggest that this pattern can reduce cognitive overload and support more confident reasoning about multi-service systems. As instructors and organizations adapt the pattern to new stacks and contexts, the underlying principle remains the same: a thoughtfully designed, production-shaped learning project can provide a clearer path to mastery than a sequence of isolated tutorials.