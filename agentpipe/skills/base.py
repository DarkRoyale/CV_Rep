"""Base skill ABC and SkillResult dataclass."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillResult:
    success: bool
    output: Any = None
    error: str | None = None

    def __str__(self) -> str:
        if self.success:
            return str(self.output) if self.output is not None else "OK"
        return f"ERROR: {self.error}"


class BaseSkill(ABC):
    """Abstract base class for all agent skills."""

    name: str = ""
    description: str = ""
    input_schema: dict = field(default_factory=dict)

    @abstractmethod
    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill with the given keyword arguments."""

    def __repr__(self) -> str:
        return f"Skill(name={self.name!r}, description={self.description!r})"
