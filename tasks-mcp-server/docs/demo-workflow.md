# Demo Workflow

This document describes the intended YouTube demonstration flow.

## Overview

The demo shows a human creating a task in the browser, then a Cursor agent picking up that task through MCP, doing the work, and marking it complete. The human refreshes the browser to see the result.

## Step-by-step

### 1. Start the web application

From the `tasks-mcp-server` directory:

```bash
uvicorn tasks_mcp_server.app:app --reload
```

### 2. Open the browser UI

Visit:

```text
http://127.0.0.1:8000
```

### 3. Create a new task

Use the **Create Task** form. Example:

- **Title:** `Create hello_mcp.txt`
- **Description:** `Create a file named hello_mcp.txt in the project root and write a short greeting from the MCP task server into it.`

### 4. Show the task in the task list

Confirm the new task appears with status **Open**.

### 5. Start the MCP server

Cursor will launch the MCP server automatically when configured. For manual testing, the command is:

```bash
python -m tasks_mcp_server.mcp_server
```

Keep the web app running in the other terminal. The MCP server calls the REST API at `http://127.0.0.1:8000` and does not access the database directly.

## How data flows during the demo

```text
Task created in web UI
        │
        ▼
REST API writes to SQLite
        │
        ▼
Cursor agent calls MCP tool
        │
        ▼
MCP server calls REST API
        │
        ▼
REST API updates SQLite
        │
        ▼
Browser refresh shows completed task
```

The task is created through the web interface. The Cursor agent retrieves the task through MCP. The MCP server calls the REST API. The REST API updates SQLite. The browser immediately displays the updated task state after refresh.

### 6. Configure Cursor MCP connection

Copy the example from [`docs/cursor/mcp-config.json`](cursor/mcp-config.json) into your Cursor MCP settings. Set `cwd` to your local `tasks-mcp-server` path.

### 7. Ask Cursor to retrieve the next task

Use the demo prompt from [`docs/cursor/demo-prompt.md`](cursor/demo-prompt.md) or paste:

```text
Use the Tasks MCP Server.

Retrieve the next available task.

Implement the requested work.

After the work is completed, call mark_task_done.
```

The agent should call the `get_next_task` MCP tool.

### 8. Let Cursor implement the task

The agent reads the task description and makes the requested change in the repository.

### 9. Ask Cursor to mark the task as done

The agent should call `mark_task_done` with the task ID.

### 10. Refresh the web UI

Click **Refresh** in the browser or reload the page. The task should now show status **Done**.

## Optional: load sample tasks

Instead of typing tasks manually, load the bundled examples:

```bash
python scripts/load_sample_tasks.py
```

Then continue from step 2.

## Demo prompt

```text
Use the Tasks MCP Server.

Retrieve the next available task.

Implement the requested work.

After the work is completed, call mark_task_done.
```

## REST API during the demo

You can also show the REST API docs at:

```text
http://127.0.0.1:8000/docs
```

This helps explain that the frontend and MCP server both use the same REST API. The API is the single source of truth for all task data.
