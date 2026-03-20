"""SearchSkill – searches for information (simulated; swap with real API)."""

from __future__ import annotations

from typing import Any

from agentpipe.skills.base import BaseSkill, SkillResult


class SearchSkill(BaseSkill):
    name = "search"
    description = "Searches for information online or in a codebase."
    input_schema = {
        "query": "str – search query",
        "scope": "str – 'web' | 'codebase' | 'docs' (default: web)",
        "max_results": "int – maximum results to return (default: 5)",
    }

    def execute(self, *, query: str = "", scope: str = "web", max_results: int = 5, **_: Any) -> SkillResult:
        if not query:
            return SkillResult(success=False, error="'query' parameter is required")
        results = self._simulate_search(query, scope, max_results)
        output = (
            f"[search] Query: {query!r} (scope={scope}, max={max_results})\n"
            f"--- results ---\n{results}\n---------------"
        )
        return SkillResult(success=True, output=output)

    @staticmethod
    def _simulate_search(query: str, scope: str, max_results: int) -> str:
        """Placeholder – replace with real search API (SerpAPI, Tavily, etc.)."""
        items = [f"  {i + 1}. [Simulated {scope} result for '{query}']" for i in range(min(max_results, 3))]
        items.append("  (Connect a real search API to get live results)")
        return "\n".join(items)
