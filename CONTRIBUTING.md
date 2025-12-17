# Contributing to StudyTracker

Thanks for your interest in improving this learning project. The primary goal of
this repo is to provide a **production-shaped**, Docker-first example for
learning FastAPI, PostgreSQL, and container-based workflows.

## Ways to Contribute

- Fix bugs or clarify confusing behavior  
- Improve documentation, diagrams, or comments  
- Add tests that exercise existing behavior  
- Propose small, focused improvements that keep the project simple

## Getting Started

1. **Fork** the repository  
2. **Clone** your fork locally  
3. Create a feature branch:
```bash
git checkout -b feature/short-description
```
4. Run the stack in Docker:
```bash
docker compose up --build web-fastapi db
```
5. Run tests:
```bash
docker compose run --rm web-fastapi pytest
```

## Coding Guidelines

- Follow the **Titanium 10+** standards of clarity and organization  
- Keep modules small and focused (routes, schemas, models, config separated)  
- Prefer explicit over clever; comments should explain *why*, not restate *what*  

Python:

- Use `black` + `isort` formatting  
- Keep functions small and predictable  
- Add type hints for public functions and data structures  

## Commit Messages

Use concise, descriptive commit messages:

- `fix: handle empty topic list gracefully`  
- `docs: clarify docker compose workflow`  
- `test: add coverage for /sessions create`

## Pull Request Process

1. Ensure the test suite passes  
2. Update documentation if behavior changes  
3. Open a PR with:

   - A clear summary of the change  
   - A short checklist of what you validated (tests, manual checks)  

Maintainers will review PRs for correctness, clarity, and alignment with the
learning goals of the project.
