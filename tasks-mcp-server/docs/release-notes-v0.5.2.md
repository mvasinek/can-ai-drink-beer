# Release Notes — v0.5.2

## Summary

Version 0.5.2 is a documentation-only patch. No application functionality changed. This release improves MCP configuration guidance for the REST API architecture introduced in v0.5.1.

## Improved MCP configuration documentation

- Updated README with required startup sequence (web app first, then MCP)
- Clarified that MCP communicates over HTTP, not SQLite
- Added recommended and advanced Cursor configuration examples

## Added recommended Cursor configuration

- Updated [`docs/cursor/mcp-config.json`](cursor/mcp-config.json) with `TASKS_MCP_API_BASE_URL`
- Added [`docs/cursor/mcp-config.md`](cursor/mcp-config.md) explaining each configuration field

## Added REST API architecture explanation

- Expanded [`docs/architecture.md`](architecture.md) with **Why the MCP Server Uses REST API**
- Updated architecture diagrams to show `MCP Server → REST API → SQLite`

## Improved troubleshooting guidance

New sections in [`docs/troubleshooting.md`](troubleshooting.md):

- MCP server cannot connect to REST API
- MCP tools not visible in Cursor
- Wrong repository path (`cwd`)

## Clarified startup workflow

- [`docs/demo-workflow.md`](demo-workflow.md) now documents the full REST API data flow step by step
- [`docs/cursor/demo-prompt.md`](demo-prompt.md) notes the web app prerequisite

## Known limitations

Unchanged from v0.5.1:

- **Localhost only**
- **No authentication**
- **No production deployment**
- **Web app must be running** before MCP tools can fetch or update tasks

## Previous versions

| Version | Focus |
|---------|-------|
| 0.5.1 | MCP routed through REST API |
| 0.5.0 | Demo and documentation release |
| 0.4.0 | MCP integration |
| 0.3.0 | Web frontend |
| 0.2.0 | REST API |
| 0.1.0 | Core task storage |
