# Architecture

## Purpose

`tasks-mcp-server` is a local demo application for a YouTube series about Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

It shows how a human can create tasks in a web UI while a Cursor agent reads and completes those tasks through MCP tools, all sharing one SQLite database.

## Main components

| Component | Role |
|-----------|------|
| Web frontend | HTML/CSS/JS UI at `/` for humans |
| REST API | FastAPI endpoints at `/api/tasks` |
| Service layer | Business logic shared by API and MCP |
| SQLite database | Local persistence in `tasks.db` |
| MCP server | Standalone stdio server for Cursor agents |

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
| Service Layer        |
+----------------------+
```

Humans interact through the browser. The frontend calls the REST API. Cursor interacts through MCP tools. Both paths reach the same service layer and the same database file.

## Why the MCP server is separate from FastAPI

The MCP server and the web application run as separate processes:

```text
Terminal 1: uvicorn tasks_mcp_server.app:app --reload
Terminal 2: python -m tasks_mcp_server.mcp_server
```

This separation keeps the demo easy to explain:

- FastAPI serves HTTP for humans and browser tools.
- MCP uses stdio transport, which Cursor launches as a child process.
- Mixing both into one process would complicate local setup and the video narrative.

Both processes read and write the same SQLite database, so a task created in the browser appears to the MCP tools, and a task marked done by Cursor appears in the web UI after refresh.

## Code layout

```text
src/tasks_mcp_server/
├── app.py          # FastAPI web app
├── web.py          # Frontend route
├── api/tasks.py    # REST endpoints
├── services.py     # Business logic
├── repositories.py # Database access
├── models.py       # SQLModel entities
├── mcp_server.py   # MCP server entry point
└── mcp_tools.py    # MCP tool implementations
```

## Design principles

- **Localhost only** — no authentication or deployment complexity
- **Shared service layer** — no duplicated business rules
- **Simple stack** — Python, SQLite, vanilla frontend, official MCP SDK
- **Educational clarity** — easy to clone, run, and demonstrate on video
