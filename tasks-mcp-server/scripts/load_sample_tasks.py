#!/usr/bin/env python3
"""Load example tasks from examples/sample_tasks.json into the database."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from tasks_mcp_server.database import create_db_and_tables, get_session
from tasks_mcp_server.schemas import TaskCreate
from tasks_mcp_server.services import TaskService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE_FILE = PROJECT_ROOT / "examples" / "sample_tasks.json"


def load_sample_tasks(sample_file: Path = DEFAULT_SAMPLE_FILE) -> int:
    if not sample_file.is_file():
        raise FileNotFoundError(f"Sample task file not found: {sample_file}")

    with sample_file.open(encoding="utf-8") as handle:
        tasks = json.load(handle)

    create_db_and_tables()
    created_count = 0

    with get_session() as session:
        service = TaskService(session)
        for item in tasks:
            service.create_task(
                TaskCreate(
                    title=item["title"],
                    description=item.get("description"),
                )
            )
            created_count += 1

    return created_count


def main() -> int:
    try:
        count = load_sample_tasks()
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Created {count} sample task(s) from {DEFAULT_SAMPLE_FILE.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
