# Release Notes — v0.5.0

## Summary

Version 0.5.0 prepares the project for public GitHub release and YouTube demonstration. No major application features were added. This release focuses on documentation, demo workflow, example tasks, and repository polish.

## Added documentation

- `docs/architecture.md` — system overview and component diagram
- `docs/demo-workflow.md` — step-by-step YouTube demo script
- `docs/troubleshooting.md` — common local setup issues and fixes
- `docs/cursor/mcp-config.json` — example Cursor MCP configuration
- `docs/cursor/demo-prompt.md` — prompts for the live demo

## Added Cursor configuration examples

Minimal MCP config and demo prompts so viewers can connect Cursor quickly.

## Added demo workflow

Documented the full human → browser → Cursor → MCP → completed task flow.

## Added example tasks

- `examples/sample_tasks.json` — three ready-to-use demo tasks
- `scripts/load_sample_tasks.py` — optional script to load examples into the database

## Improved README

Rewrote the project README with quick start, architecture summary, demo links, troubleshooting references, and roadmap update.

## Known limitations

- **Localhost only** — not designed for remote or production use
- **No authentication** — anyone with local access can read and change tasks
- **No production deployment** — no Docker, CI/CD, or cloud hosting in this demo
- **No autonomous monitoring loop** — tasks are not polled or executed automatically; an agent must be prompted

## Previous versions

| Version | Focus |
|---------|-------|
| 0.1.0 | Core task storage |
| 0.2.0 | REST API |
| 0.3.0 | Web frontend |
| 0.4.0 | MCP integration |
| 0.5.0 | Demo and documentation release |
