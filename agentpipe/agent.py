"""Agent – named entity with a skill registry that can execute tickets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from agentpipe.skills.base import BaseSkill, SkillResult
from agentpipe.skills.file_ops import FileOpsSkill

if TYPE_CHECKING:
    from agentpipe.ticket import Ticket


@dataclass
class Agent:
    name: str
    skills: list[BaseSkill] = field(default_factory=list)
    description: str = ""

    # ------------------------------------------------------------------
    # Skill helpers
    # ------------------------------------------------------------------

    @property
    def skill_names(self) -> list[str]:
        return [s.name for s in self.skills]

    def has_skill(self, skill_name: str) -> bool:
        return skill_name in self.skill_names

    def get_skill(self, skill_name: str) -> BaseSkill | None:
        for s in self.skills:
            if s.name == skill_name:
                return s
        return None

    # ------------------------------------------------------------------
    # Ticket execution
    # ------------------------------------------------------------------

    def execute_ticket(self, ticket: Ticket) -> SkillResult:
        """Execute the ticket using the most appropriate skill.

        Selection logic:
        1. If ``ticket.skills_required`` is non-empty, use the first skill that
           this agent actually has.
        2. If no matching skill is found but the agent has at least one skill,
           fall back to the first skill in the agent's registry.
        3. If the agent has no skills at all, fall back to ``FileOpsSkill``
           (a no-op/logging default) and log a warning.
        4. If ``skills_required`` is empty, use the agent's first skill or
           ``FileOpsSkill``.
        """
        skill: BaseSkill | None = None

        if ticket.skills_required:
            for skill_name in ticket.skills_required:
                skill = self.get_skill(skill_name)
                if skill:
                    break
            if skill is None:
                missing = ticket.skills_required
                return SkillResult(
                    success=False,
                    error=(
                        f"Agent '{self.name}' lacks required skills "
                        f"{missing} for ticket '{ticket.id}'"
                    ),
                )
        else:
            skill = self.skills[0] if self.skills else FileOpsSkill()

        return skill.execute(
            task=ticket.title,
            goal=ticket.title,
            target=ticket.title,
            code=ticket.description or ticket.title,
            query=ticket.title,
            path=ticket.description or ".",
            operation="read",
        )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skill_names,
        }

    @classmethod
    def from_dict(cls, data: dict, skill_registry: dict | None = None) -> Agent:
        from agentpipe.skills import SKILL_REGISTRY

        registry = skill_registry or SKILL_REGISTRY
        skills = [registry[s]() for s in data.get("skills", []) if s in registry]
        return cls(name=data["name"], description=data.get("description", ""), skills=skills)
