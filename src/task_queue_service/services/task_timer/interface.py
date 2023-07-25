from datetime import datetime
from typing import Protocol


class AbstractTaskTimerService(Protocol):
    def __call__(self) -> datetime:
        """Calculate time when a task must be done."""
