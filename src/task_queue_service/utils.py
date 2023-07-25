from typing import Protocol
from urllib.parse import quote, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession


def pg_dsn_factory(
    user: str,
    password: str,
    host: str,
    port: int,
    db: str,
    scheme: str = "postgresql+asyncpg",
) -> str:
    netloc = (
        f"{quote(user, safe='')}"
        f":{quote(password, safe='')}"
        f"@{quote(host, safe='')}"
        f":{port}"
    )
    path = quote(f"/{db}")
    return urlunparse([scheme, netloc, path, "", "", ""])


class AsyncSessionFactory(Protocol):
    def __call__(self) -> AsyncSession:
        """Make a session."""
