# tasks-mcp-server

A Python backend for managing tasks, designed to expose REST API and MCP tools in future versions.

**Current version:** 0.2.0

## Project context

This project is a demonstration application for a YouTube video series about Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

The application is intended to run only on **localhost**. Production concerns such as authentication, deployment, and cloud hosting are intentionally out of scope. The goal is simplicity, readability, and ease of setup.

Version 0.2.0 adds a FastAPI REST API on top of the v0.1.0 storage layer. Frontend and MCP tools are planned for later releases.

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/mvasinek/can-ai-drink-beer.git
cd tasks-mcp-server

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -e .
```

Run the API server:

```bash
uvicorn tasks_mcp_server.app:app --reload
```

Open the interactive API docs locally:

```text
http://127.0.0.1:8000/docs
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

## REST API overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/tasks` | List tasks (optional `?status=` filter) |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/next/open` | Get oldest open task |
| GET | `/api/tasks/{task_id}` | Get a task by ID |
| PATCH | `/api/tasks/{task_id}` | Update a task |
| DELETE | `/api/tasks/{task_id}` | Delete a task |
| POST | `/api/tasks/{task_id}/done` | Mark a task as done |

## Example curl commands

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Example task", "description": "Created through REST API"}'
```

```bash
curl http://127.0.0.1:8000/api/tasks
```

## Roadmap

| Version | Focus |
|---------|-------|
| 0.1.0 | Core task storage (SQLite, models, repository, service) |
| **0.2.0** | REST API endpoints |
| 0.3.0+ | MCP server tools |
| Later | Frontend, authentication, deployment |

See `specifications/` for detailed version specs.
