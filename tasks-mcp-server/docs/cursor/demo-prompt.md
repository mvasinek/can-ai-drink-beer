# Cursor Demo Prompt

Use this prompt during the YouTube demonstration.

## Basic prompt

```text
Use the Tasks MCP Server.

Retrieve the next available task.

Implement the requested work.

After the work is completed, call mark_task_done.
```

## Concrete example

```text
Use the Tasks MCP Server.

Retrieve the next available task.

If the task asks you to create or modify a file, implement it in the current repository.

After the work is completed and verified, call mark_task_done with the task id.
```

## Available MCP tools

| Tool | Purpose |
|------|---------|
| `get_next_task` | Get the oldest open task |
| `mark_task_done` | Mark a task as completed |
| `get_task` | Read full task details by ID |
| `list_open_tasks` | List all open tasks |

## Available MCP resource

- `tasks://open` — JSON list of open tasks

## Available MCP prompt

- `implement_next_task` — built-in guidance for fetch → implement → complete
