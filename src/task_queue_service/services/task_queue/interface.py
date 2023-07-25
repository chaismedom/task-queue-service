from typing import Protocol


class AbstractTaskQueueService(Protocol):
    async def poll(self) -> None:
        """Poll tasks inside queue and mark all the tasks as ready."""
