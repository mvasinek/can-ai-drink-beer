# tasks-mcp-server

A localhost demo app for managing tasks through a web UI, REST API, and MCP tools. Built for a YouTube series on Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

**Current version:** 0.5.2

## What this project demonstrates

- **Spec-driven development** — each version is defined before implementation
- **Semantic versioning** — incremental releases from storage to API to frontend to MCP
- **Human + agent workflow** — create tasks in the browser, let Cursor complete them via MCP
- **Single source of truth** — the REST API is the only task data path for frontend and MCP

Tasks can be fetched by Cursor through MCP while humans manage the same task list in the browser.

## Architecture overview

```text
Browser
   │
   ▼
Web Frontend
   │
   ▼
REST API
   │
   ▼
SQLite

Cursor Agent
   │
   ▼
MCP Server
   │
   ▼
REST API
   │
   ▼
SQLite
```

The MCP server is a lightweight HTTP adapter. It never accesses SQLite directly — all task reads and writes go through the REST API.

More detail: [docs/architecture.md](docs/architecture.md)

Screenshots may be added later in [docs/images/](docs/images/).

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

Optional environment variables:

```bash
set TASKS_MCP_DATABASE_URL=sqlite:///./tasks.db
set TASKS_MCP_API_BASE_URL=http://127.0.0.1:8000
```

### Required startup sequence

Both the web application and MCP integration depend on the REST API. Always start in this order:

#### Terminal 1 — web application

```bash
uvicorn tasks_mcp_server.app:app --reload
```

#### Verify

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and confirm the web UI loads.

REST API interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Terminal 2 — MCP server (optional manual test)

Cursor normally starts the MCP server automatically. For manual testing:

```bash
python -m tasks_mcp_server.mcp_server
```

The MCP server communicates with the application through the REST API. This guarantees that all task operations are immediately visible in the web UI.

## Cursor MCP Configuration

Cursor starts the MCP server as a local child process. The MCP server then sends HTTP requests to the FastAPI REST API — it does not open the SQLite database.

Copy the example from [docs/cursor/mcp-config.json](docs/cursor/mcp-config.json). Field-by-field help: [docs/cursor/mcp-config.md](docs/cursor/mcp-config.md).

### Recommended configuration

Use the direct script path with `cwd` pointing at the repository root:

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "python",
      "args": [
        "src/tasks_mcp_server/mcp_server.py"
      ],
      "cwd": "/path/to/tasks-mcp-server",
      "env": {
        "TASKS_MCP_API_BASE_URL": "http://127.0.0.1:8000"
      }
    }
  }
}
```

- `cwd` points to the repository root (the folder containing `src/` and `pyproject.toml`).
- `TASKS_MCP_API_BASE_URL` points to the running FastAPI application.

On Windows, set `command` to your venv Python, e.g. `C:/path/to/tasks-mcp-server/.venv/Scripts/python.exe`.

If imports fail, add `"PYTHONPATH": "src"` to `env` or run `pip install -e .` first.

### Advanced configuration

After `pip install -e .`, you can use the module entry point:

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "tasks_mcp_server.mcp_server"
      ],
      "env": {
        "TASKS_MCP_API_BASE_URL": "http://127.0.0.1:8000"
      }
    }
  }
}
```

This version assumes the package is installed in the Python environment Cursor uses.

## Demo workflow

Full step-by-step guide: [docs/demo-workflow.md](docs/demo-workflow.md)

1. Start the web app and verify [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. Create a task (or load examples — see below)
3. Configure Cursor MCP with `TASKS_MCP_API_BASE_URL`
4. Ask Cursor to retrieve and complete the next task
5. Refresh the browser to see the completed task

**Demo prompt:**

```text
Use the Tasks MCP Server.

Retrieve the next available task.

Implement the requested work.

After the work is completed, call mark_task_done.
```

More prompts: [docs/cursor/demo-prompt.md](docs/cursor/demo-prompt.md)

## Example tasks

Bundled demo tasks live in [examples/sample_tasks.json](examples/sample_tasks.json):

- Create `hello_mcp.txt`
- Add `demo_note.md`
- Update README demo section

Load them into the database:

```bash
python scripts/load_sample_tasks.py
```

## Troubleshooting

Common issues and fixes: [docs/troubleshooting.md](docs/troubleshooting.md)

Topics include REST API unavailable, MCP configuration, `cwd` path mistakes, and Cursor not seeing tools.

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

## MCP tools

| Tool | REST endpoint used |
|------|-------------------|
| `get_next_task` | `GET /api/tasks/next/open` |
| `get_task` | `GET /api/tasks/{id}` |
| `list_open_tasks` | `GET /api/tasks?status=open` |
| `mark_task_done` | `POST /api/tasks/{id}/done` |

Resource: `tasks://open` — JSON list of open tasks

Prompt: `implement_next_task` — built-in agent guidance

## Roadmap

| Version | Focus |
|---------|-------|
| 0.1.0 | Core task storage |
| 0.2.0 | REST API |
| 0.3.0 | Web frontend |
| 0.4.0 | MCP integration |
| 0.5.0 | Demo and documentation release |
| 0.5.1 | MCP routed through REST API |
| **0.5.2** | MCP configuration documentation |
| Later | Authentication, deployment |

Release notes: [docs/release-notes-v0.5.2.md](docs/release-notes-v0.5.2.md)

See `specifications/` for version specs.

## License note

This project is provided as educational demo material for the YouTube series. Use and adapt it for learning and local experimentation.
