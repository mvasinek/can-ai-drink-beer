# tasks-mcp-server

A localhost demo app for managing tasks through a web UI, REST API, and MCP tools. Built for a YouTube series on Spec-Driven Development, Semantic Versioning, Cursor Agents, and Model Context Protocol (MCP).

**Current version:** 0.5.1

## What this project demonstrates

- **Spec-driven development** — each version is defined before implementation
- **Semantic versioning** — incremental releases from storage to API to frontend to MCP
- **Human + agent workflow** — create tasks in the browser, let Cursor complete them via MCP
- **Single source of truth** — the REST API is the only task data path for frontend and MCP

Tasks can be fetched by Cursor through MCP while humans manage the same task list in the browser.

## Architecture overview

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
| SQLite Database      |
+----------------------+
```

The MCP server is a lightweight adapter. It does not access SQLite directly.

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

## Running the web app

**Terminal 1** — start the REST API and web UI:

```bash
uvicorn tasks_mcp_server.app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

REST API interactive docs:

```text
http://127.0.0.1:8000/docs
```

## Running the MCP server

**Terminal 2** — start the MCP adapter (keep Terminal 1 running):

```bash
python -m tasks_mcp_server.mcp_server
```

The MCP server communicates with the application through the REST API. This guarantees that all task operations are immediately visible in the web UI.

Cursor normally launches this process automatically when MCP is configured.

## Cursor MCP configuration

Copy [docs/cursor/mcp-config.json](docs/cursor/mcp-config.json) into your Cursor MCP settings. Set `cwd` to your local `tasks-mcp-server` directory.

On Windows, prefer the venv Python path:

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "C:/path/to/tasks-mcp-server/.venv/Scripts/python.exe",
      "args": ["-m", "tasks_mcp_server.mcp_server"],
      "cwd": "C:/path/to/tasks-mcp-server"
    }
  }
}
```

## Demo workflow

Full step-by-step guide: [docs/demo-workflow.md](docs/demo-workflow.md)

1. Start the web app and open the browser UI
2. Create a task (or load examples — see below)
3. Configure Cursor MCP
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

Topics include port conflicts, REST API unavailable, MCP startup, and Cursor not seeing tools.

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
| **0.5.1** | MCP routed through REST API |
| Later | Authentication, deployment |

Release notes: [docs/release-notes-v0.5.1.md](docs/release-notes-v0.5.1.md)

See `specifications/` for version specs.

## License note

This project is provided as educational demo material for the YouTube series. Use and adapt it for learning and local experimentation.
