import os

DEFAULT_DATABASE_URL = "sqlite:///tasks.db"


def get_database_url() -> str:
    return os.environ.get("TASKS_MCP_DATABASE_URL", DEFAULT_DATABASE_URL)
