# MCP Configuration Reference

This file documents the fields in [`mcp-config.json`](mcp-config.json).

## Field reference

| Field | Purpose |
|-------|---------|
| `command` | Python executable. Use your virtual environment Python on Windows, e.g. `.venv/Scripts/python.exe`. |
| `args` | Entry script for the MCP server. Default: `src/tasks_mcp_server/mcp_server.py` relative to `cwd`. |
| `cwd` | **Repository root** — the `tasks-mcp-server` folder that contains `src/`, `pyproject.toml`, and `examples/`. |
| `env.TASKS_MCP_API_BASE_URL` | Base URL of the running FastAPI application. Default: `http://127.0.0.1:8000`. |

## Important notes

1. **Start the web app first.** The MCP server calls the REST API over HTTP. It does not access SQLite directly.
2. **`cwd` must point to the repository root**, not `src/` or a parent monorepo folder unless that folder contains this project.
3. **Direct script path:** If you use `src/tasks_mcp_server/mcp_server.py`, add `"PYTHONPATH": "src"` to `env`, or run `pip install -e .` first.
4. **Alternative:** Use `python -m tasks_mcp_server.mcp_server` in `args` after `pip install -e .` (see README advanced configuration).

## Example with venv Python (Windows)

```json
{
  "mcpServers": {
    "tasks-mcp-server": {
      "command": "C:/path/to/tasks-mcp-server/.venv/Scripts/python.exe",
      "args": ["src/tasks_mcp_server/mcp_server.py"],
      "cwd": "C:/path/to/tasks-mcp-server",
      "env": {
        "TASKS_MCP_API_BASE_URL": "http://127.0.0.1:8000",
        "PYTHONPATH": "src"
      }
    }
  }
}
```
