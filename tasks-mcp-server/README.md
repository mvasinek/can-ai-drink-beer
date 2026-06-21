# tasks-mcp-server

A Python backend for managing tasks with a web frontend, REST API, and MCP server for AI agents.

**Current version:** 0.4.0

## Project context

This project is a demonstration application for a YouTube video series about Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

The application is intended to run only on **localhost**. Production concerns such as authentication, deployment, and cloud hosting are intentionally out of scope. The goal is simplicity, readability, and ease of setup.

Version 0.4.0 adds a standalone MCP server so Cursor and other MCP-compatible agents can read and complete tasks through the shared service layer.

## Architecture

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
| MCP Server           |
+----------+-----------+
           |
           v
+----------------------+
| Service Layer        |
+----------------------+
```

Both the web application and MCP server reuse the same service layer and SQLite database.

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

Optional: override the database location with the `TASKS_MCP_DATABASE_URL` environment variable (default: `sqlite:///tasks.db`).

## Running the web application

```bash
uvicorn tasks_mcp_server.app:app --reload
```

Open the web frontend locally:

```text
http://127.0.0.1:8000
```

Open the interactive REST API docs locally:

```text
http://127.0.0.1:8000/docs
```

## Running the MCP server

Run the MCP server in a separate terminal while the web app is running:

```bash
python -m tasks_mcp_server.mcp_server
```

The MCP server uses stdio transport and is intended for local tools such as Cursor.

### MCP tools

| Tool | Description |
|------|-------------|
| `get_next_task` | Return the oldest open task |
| `mark_task_done` | Mark a task as done |
| `get_task` | Return full task details |
| `list_open_tasks` | List all open tasks |

### MCP resource

| Resource | Description |
|----------|-------------|
| `tasks://open` | JSON list of all open tasks |

### MCP prompt

| Prompt | Description |
|--------|-------------|
| `implement_next_task` | Guides an agent to fetch, implement, and complete the next task |

## Example Cursor configuration

Add this to your Cursor MCP settings. Set `cwd` to the local path of this project:

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "tasks_mcp_server.mcp_server"
      ],
      "cwd": "/path/to/tasks-mcp-server"
    }
  }
}
```

On Windows, use the full path to the project virtual environment Python if needed:

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "C:/path/to/tasks-mcp-server/.venv/Scripts/python.exe",
      "args": [
        "-m",
        "tasks_mcp_server.mcp_server"
      ],
      "cwd": "C:/path/to/tasks-mcp-server"
    }
  }
}
```

## Example Cursor prompt

Use this prompt during the YouTube demonstration:

```text
Use the Tasks MCP Server.

Retrieve the next available task.

Implement the requested work.

After the work is completed, call mark_task_done.
```

## Running tests

```bash
pytest
```

## Linting

```bash
ruff check .
```

## Frontend overview

The web UI is a single-page interface served at `/`. It uses vanilla JavaScript and talks to the REST API only.

Supported actions:

- view the task list
- create a task
- edit a task (title, description, status)
- delete a task
- mark a task as done
- filter tasks by status
- refresh the task list

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
| 0.2.0 | REST API endpoints |
| 0.3.0 | Web frontend |
| **0.4.0** | MCP server integration |
| Later | Authentication, deployment |

See `specifications/` for detailed version specs.
