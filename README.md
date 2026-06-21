# tasks-mcp-server

A Python backend for managing tasks, designed to expose REST API and MCP tools in future versions.

**Current version:** 0.1.0

Version 0.1.0 contains only the core task storage layer — SQLite persistence, domain models, repository and service layers, and basic tests. REST API, frontend, and MCP server integration are planned for later releases.

## Local setup

Requires Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -e ".[dev]"
```

Optional: override the database location with the `TASKS_MCP_DATABASE_URL` environment variable (default: `sqlite:///tasks.db`).

## Running tests

```bash
pytest
```

## Linting

```bash
ruff check .
```

## Roadmap

| Version | Focus |
|---------|-------|
| **0.1.0** | Core task storage (SQLite, models, repository, service) |
| 0.2.0+ | REST API endpoints |
| 0.3.0+ | MCP server tools |
| Later | Frontend, authentication, deployment |

See `specifications/` for detailed version specs.
