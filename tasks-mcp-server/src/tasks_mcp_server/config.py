import os

DEFAULT_DATABASE_URL = "sqlite:///tasks.db"
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"


def get_database_url() -> str:
    return os.environ.get("TASKS_MCP_DATABASE_URL", DEFAULT_DATABASE_URL)


def get_api_base_url() -> str:
    return os.environ.get("TASKS_MCP_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
