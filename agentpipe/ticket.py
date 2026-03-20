"""Ticket model with status/priority enums and full serialisation support."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class TicketStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"


class TicketPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _short_uuid() -> str:
    return str(uuid.uuid4())[:8]


@dataclass
class Ticket:
    title: str
    description: str = ""
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.TODO
    id: str = field(default_factory=_short_uuid)
    assigned_to: str | None = None
    skills_required: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    result: str | None = None
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    retry_count: int = 0

    def touch(self) -> None:
        """Refresh updated_at timestamp."""
        self.updated_at = _now_iso()

    def set_status(self, status: TicketStatus) -> None:
        """Set status and update the timestamp."""
        self.status = status
        self.touch()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value if isinstance(self.priority, TicketPriority) else self.priority,
            "status": self.status.value if isinstance(self.status, TicketStatus) else self.status,
            "assigned_to": self.assigned_to,
            "skills_required": self.skills_required,
            "depends_on": self.depends_on,
            "result": self.result,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "retry_count": self.retry_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Ticket:
        data = dict(data)
        if "priority" in data and isinstance(data["priority"], str):
            data["priority"] = TicketPriority(data["priority"])
        if "status" in data and isinstance(data["status"], str):
            data["status"] = TicketStatus(data["status"])
        return cls(**data)
