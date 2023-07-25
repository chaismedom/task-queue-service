from typing import Any, Protocol, Self

from task_queue_service.repositories.interface import AbstractTaskRepository


class UnitOfWork(Protocol):
    is_committed: bool
    task_repository: AbstractTaskRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        if not self.is_committed:
            await self.rollback()

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
