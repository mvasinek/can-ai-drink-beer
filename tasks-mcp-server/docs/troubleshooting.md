# Troubleshooting

Short fixes for common local setup issues.

---

## Port 8000 is already in use

**Symptoms:** `uvicorn` fails with an address-already-in-use error.

**Likely cause:** Another process (often a previous `uvicorn` instance) is using port 8000.

**Suggested fix:**

- Stop the other process, or
- Run on a different port:

```bash
uvicorn tasks_mcp_server.app:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

---

## MCP server cannot connect to REST API

**Symptoms:**

```text
Unable to contact Tasks REST API
Connection refused
```

**Likely cause:** The FastAPI application is not running.

**Suggested fix:**

```bash
uvicorn tasks_mcp_server.app:app --reload
```

Verify [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) returns `{"status":"ok"}`.

Ensure `TASKS_MCP_API_BASE_URL` in Cursor MCP settings matches the running server (default: `http://127.0.0.1:8000`).

---

## MCP tools not visible in Cursor

**Symptoms:** The agent does not call `get_next_task`, `mark_task_done`, or other tools.

**Likely cause:** Incorrect MCP configuration, wrong `cwd`, wrong Python executable, or Cursor needs a reload.

**Check:**

1. MCP configuration path and JSON syntax
2. `cwd` setting points to the `tasks-mcp-server` repository root
3. Python executable matches the environment where `pip install -e .` was run
4. Reload MCP servers or restart Cursor after config changes
5. Web app is running before using MCP tools

See [`docs/cursor/mcp-config.json`](cursor/mcp-config.json) and [`docs/cursor/mcp-config.md`](cursor/mcp-config.md).

---

## Wrong repository path (`cwd`)

**Symptoms:** MCP server fails to start, import errors, or tools return API errors.

**Likely cause:** The `cwd` setting does not point to the repository root.

**Suggested fix:**

The `cwd` value must be the folder that contains `src/`, `pyproject.toml`, and `examples/`.

Example (Windows):

```text
C:/Users/you/projects/can-ai-drink-beer/tasks-mcp-server
```

Example (Linux/macOS):

```text
/home/you/projects/can-ai-drink-beer/tasks-mcp-server
```

Do not set `cwd` to the monorepo root unless the project files live there directly.

---

## MCP server does not start

**Symptoms:** Cursor reports the MCP server failed to start, or `python -m tasks_mcp_server.mcp_server` exits immediately.

**Likely cause:** Wrong working directory, missing virtual environment, package not installed, or the REST API is not running.

**Suggested fix:**

1. Start the web app first: `uvicorn tasks_mcp_server.app:app --reload`
2. `cd` into the `tasks-mcp-server` directory.
3. Activate the virtual environment.
4. Run `pip install -e .`
5. Use the full path to the venv Python in Cursor config on Windows.

---

## Cursor does not see MCP tools

**Symptoms:** The agent does not call `get_next_task`, `mark_task_done`, or other tools.

**Likely cause:** Web app not running, MCP server cannot reach the REST API, MCP server not configured, wrong `cwd`, or Cursor needs a restart after config changes.

**Suggested fix:**

1. Start the web app: `uvicorn tasks_mcp_server.app:app --reload`
2. Verify [`docs/cursor/mcp-config.json`](cursor/mcp-config.json) matches your setup.
3. Set `cwd` to the absolute path of `tasks-mcp-server`.
4. Restart Cursor or reload MCP servers.
5. Confirm the server name appears in Cursor MCP settings.

---

## Database file is missing

**Symptoms:** Tasks disappear between runs, or the app behaves like a fresh install.

**Likely cause:** The database file is created on first startup at the default location (`tasks.db` in the current working directory). Running commands from different directories creates different files.

**Suggested fix:**

- Always start the web app and MCP server from the same directory, or
- Set a fixed path:

```bash
set TASKS_MCP_DATABASE_URL=sqlite:///./tasks.db
```

On Linux/macOS, use `export` instead of `set`.

---

## Task list does not update

**Symptoms:** Cursor marks a task done, but the browser still shows **Open**.

**Likely cause:** MCP server could not reach the REST API, or the web app and MCP server were using different API/database paths.

**Suggested fix:**

1. Ensure the web app is running on `http://127.0.0.1:8000`.
2. Start MCP only after the REST API is available.
3. Use the same `TASKS_MCP_API_BASE_URL` if you override the default.
4. Click **Refresh** in the web UI.

---

## Python module cannot be found

**Symptoms:** `ModuleNotFoundError: No module named 'tasks_mcp_server'`.

**Likely cause:** Package not installed in the active environment, or command run outside the project directory.

**Suggested fix:**

```bash
cd tasks-mcp-server
pip install -e .
```

Use the venv Python in Cursor MCP config.

---

## SQLite database is locked

**Symptoms:** Errors mentioning database locked or unable to write.

**Likely cause:** Multiple writers contending on SQLite, or a crashed process holding a lock.

**Suggested fix:**

1. Stop extra `uvicorn` or MCP server instances.
2. Restart the web app.
3. If the problem persists, close all processes using `tasks.db` and restart.

---

## Still stuck?

See also:

- [Architecture](architecture.md)
- [Demo workflow](demo-workflow.md)
- [Release notes v0.5.2](release-notes-v0.5.2.md)
