# Architecture

## Purpose

`tasks-mcp-server` is a local demo application for a YouTube series about Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

It shows how a human can create tasks in a web UI while a Cursor agent reads and completes those tasks through MCP tools. Both paths use the **REST API as the single source of truth** for task data.

## Main components

| Component | Role |
|-----------|------|
| Web frontend | HTML/CSS/JS UI at `/` for humans |
| REST API | FastAPI endpoints at `/api/tasks` |
| Service layer | Business logic used by the REST API |
| SQLite database | Local persistence in `tasks.db` |
| MCP server | Lightweight adapter that calls the REST API |

## How the pieces fit together

```text
+----------------------+
| Web Frontend         |
+----------+-----------+
           |
           v
+----------------------+
| REST API             |
+----------+-----------+
           |
           v
+----------------------+
| Service Layer        |
+----------+-----------+
           |
           v
+----------------------+
| SQLite Database      |
+----------------------+

+----------------------+
| Cursor Agent         |
+----------+-----------+
           |
           v
+----------------------+
| MCP Server           |
+----------+-----------+
           |
           v
+----------------------+
| REST API             |
+----------+-----------+
           |
           v
+----------------------+
| Service Layer        |
+----------+-----------+
           |
           v
+----------------------+
| SQLite Database      |
+----------------------+
```

Humans interact through the browser. The frontend calls the REST API. Cursor interacts through MCP tools, which also call the REST API. All task changes flow through the same HTTP endpoints and the same service layer.

## REST API as the single source of truth

Since v0.5.1, the MCP server no longer accesses SQLite directly. It uses a small HTTP client (`mcp_api_client.py`) to call:

- `GET /api/tasks/next/open`
- `GET /api/tasks/{id}`
- `GET /api/tasks?status=open`
- `POST /api/tasks/{id}/done`

This guarantees that:

- tasks created in the browser are visible to MCP tools,
- tasks marked done by Cursor appear in the web UI after refresh,
- there is only one database access path to troubleshoot.

## Why the MCP server is separate from FastAPI

The MCP server and the web application run as separate processes:

```text
Terminal 1: uvicorn tasks_mcp_server.app:app --reload
Terminal 2: python -m tasks_mcp_server.mcp_server
```

This separation keeps the demo easy to explain:

- FastAPI serves HTTP for humans and browser tools.
- MCP uses stdio transport, which Cursor launches as a child process.
- The MCP server is a thin adapter over the REST API, not a second backend.

The web app must be running before MCP tools can fetch or update tasks.

## Code layout

```text
src/tasks_mcp_server/
├── app.py            # FastAPI web app
├── web.py            # Frontend route
├── api/tasks.py      # REST endpoints
├── services.py       # Business logic
├── repositories.py   # Database access
├── models.py         # SQLModel entities
├── mcp_server.py     # MCP server entry point
├── mcp_tools.py      # MCP tool response shaping
└── mcp_api_client.py # REST API client for MCP
```

## Design principles

- **Localhost only** — no authentication or deployment complexity
- **REST API first** — one source of truth for all task operations
- **Simple stack** — Python, SQLite, vanilla frontend, official MCP SDK, httpx
- **Educational clarity** — easy to clone, run, and demonstrate on video
