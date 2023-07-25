from typing import NoReturn, Protocol


class AbstractPollWorkerLoop(Protocol):
    async def run(self) -> NoReturn:
        pass
