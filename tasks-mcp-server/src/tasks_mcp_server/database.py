from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

from tasks_mcp_server.config import get_database_url
from tasks_mcp_server.models import Task  # noqa: F401

_engine = None


def get_engine(*, database_url: str | None = None):
    global _engine
    url = database_url or get_database_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    if _engine is None or str(_engine.url) != url:
        _engine = create_engine(url, connect_args=connect_args)
    return _engine


def reset_engine() -> None:
    global _engine
    _engine = None


def create_db_and_tables(*, database_url: str | None = None) -> None:
    engine = get_engine(database_url=database_url)
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session(*, database_url: str | None = None) -> Generator[Session, None, None]:
    engine = get_engine(database_url=database_url)
    with Session(engine) as session:
        yield session
