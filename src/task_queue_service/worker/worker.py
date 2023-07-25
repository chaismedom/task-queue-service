import asyncio
from datetime import timedelta
from typing import NoReturn

from task_queue_service.use_cases import AbstractPollTasksUseCase
from task_queue_service.worker.interface import AbstractPollWorkerLoop


class PollWorkerLoop(AbstractPollWorkerLoop):
    def __init__(
        self,
        poll_timeout: timedelta,
        use_case: AbstractPollTasksUseCase,
    ) -> None:
        self.poll_timeout_seconds = poll_timeout.total_seconds()
        self.use_case = use_case

    async def run(self) -> NoReturn:
        while True:
            await asyncio.sleep(self.poll_timeout_seconds)
            await self.use_case()
