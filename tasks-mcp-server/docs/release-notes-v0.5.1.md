# Release Notes — v0.5.1

## Summary

Version 0.5.1 refactors MCP integration so the MCP server communicates exclusively through the REST API. No application behavior changes for the web UI or REST endpoints.

## Refactored MCP integration

- Removed direct database, repository, and service access from MCP code
- Added `mcp_api_client.py` as a thin HTTP client wrapper
- MCP tools now call existing REST endpoints

## MCP now communicates through REST API

The MCP server uses:

- `GET /api/tasks/next/open`
- `GET /api/tasks/{id}`
- `GET /api/tasks?status=open`
- `POST /api/tasks/{id}/done`

Configure the API base URL with `TASKS_MCP_API_BASE_URL` (default: `http://127.0.0.1:8000`).

## Improved architecture

```text
MCP Server → REST API → Service Layer → SQLite
```

Instead of:

```text
MCP Server → Service Layer → SQLite
```

## Improved demo experience

- One source of truth for task data
- Browser and Cursor always see the same tasks
- Easier troubleshooting during live demos

## Single source of truth

The REST API is now the only entry point for task mutations and reads from MCP tools. The web frontend already used the REST API; MCP now follows the same path.

## Known limitations

Unchanged from v0.5.0:

- **Localhost only**
- **No authentication**
- **No production deployment**
- **No autonomous monitoring loop**
- **Web app must be running** before MCP tools can fetch or update tasks

## Previous versions

| Version | Focus |
|---------|-------|
| 0.5.0 | Demo and documentation release |
| 0.4.0 | MCP integration |
| 0.3.0 | Web frontend |
| 0.2.0 | REST API |
| 0.1.0 | Core task storage |
