import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


class TaskStatus(enum.StrEnum):
    WAITING = "waiting"
    DONE = "done"


@dataclass
class Task:
    title: str
    waiting_time: datetime

    id_: UUID = field(default_factory=uuid.uuid4)
    status: TaskStatus = TaskStatus.WAITING

    def mark_done(self) -> None:
        if not self.is_expired():
            raise Exception("Cannot be marked as done")

        self.task_status = TaskStatus.DONE

    def is_expired(self) -> bool:
        return datetime.now() > self.waiting_time
