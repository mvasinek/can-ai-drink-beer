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

## MCP server does not start

**Symptoms:** Cursor reports the MCP server failed to start, or `python -m tasks_mcp_server.mcp_server` exits immediately.

**Likely cause:** Wrong working directory, missing virtual environment, or package not installed.

**Suggested fix:**

1. `cd` into the `tasks-mcp-server` directory.
2. Activate the virtual environment.
3. Run `pip install -e .`
4. Use the full path to the venv Python in Cursor config on Windows.

---

## Cursor does not see MCP tools

**Symptoms:** The agent does not call `get_next_task`, `mark_task_done`, or other tools.

**Likely cause:** MCP server not configured, wrong `cwd`, or Cursor needs a restart after config changes.

**Suggested fix:**

1. Verify [`docs/cursor/mcp-config.json`](cursor/mcp-config.json) matches your setup.
2. Set `cwd` to the absolute path of `tasks-mcp-server`.
3. Restart Cursor or reload MCP servers.
4. Confirm the server name appears in Cursor MCP settings.

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

**Likely cause:** Web app and MCP server are using different database files or directories.

**Suggested fix:**

1. Ensure both processes run from the same `tasks-mcp-server` directory.
2. Use the same `TASKS_MCP_DATABASE_URL` for both if you override it.
3. Click **Refresh** in the web UI.

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
- [Release notes v0.5.0](release-notes-v0.5.0.md)
