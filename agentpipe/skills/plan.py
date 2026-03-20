"""PlanSkill – decomposes a high-level goal into sub-tickets."""

from __future__ import annotations

from typing import Any

from agentpipe.skills.base import BaseSkill, SkillResult


class PlanSkill(BaseSkill):
    name = "plan"
    description = "Decomposes a high-level goal into a list of actionable sub-tickets."
    input_schema = {
        "goal": "str – high-level goal to decompose",
        "max_tickets": "int – max number of sub-tickets (default: 5)",
    }

    def execute(self, *, goal: str = "", max_tickets: int = 5, **_: Any) -> SkillResult:
        if not goal:
            return SkillResult(success=False, error="'goal' parameter is required")
        tickets = self._simulate_decompose(goal, max_tickets)
        lines = [f"[plan] Decomposed goal: {goal!r}", "--- sub-tickets ---"]
        for i, t in enumerate(tickets, 1):
            lines.append(f"  {i}. {t}")
        lines.append("-------------------")
        return SkillResult(success=True, output="\n".join(lines), error=None)

    @staticmethod
    def _simulate_decompose(goal: str, max_tickets: int) -> list[str]:
        """Placeholder – replace with real LLM call that returns structured tickets."""
        templates = [
            f"Research and gather requirements for: {goal}",
            f"Design architecture/approach for: {goal}",
            f"Implement core logic for: {goal}",
            f"Write tests for: {goal}",
            f"Review and document: {goal}",
            f"Deploy / integrate: {goal}",
        ]
        return templates[:max_tickets]
