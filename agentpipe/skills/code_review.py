"""CodeReviewSkill – reviews code and provides feedback."""

from __future__ import annotations

from typing import Any

from agentpipe.skills.base import BaseSkill, SkillResult


class CodeReviewSkill(BaseSkill):
    name = "code_review"
    description = "Reviews code for bugs, style issues, and improvements."
    input_schema = {
        "code": "str – source code to review",
        "language": "str – programming language (default: python)",
        "focus": "str – optional focus area (security, performance, …)",
    }

    def execute(self, *, code: str = "", language: str = "python", focus: str = "", **_: Any) -> SkillResult:
        if not code:
            return SkillResult(success=False, error="'code' parameter is required")
        feedback = self._simulate_review(code, language, focus)
        output = (
            f"[code_review] Reviewed {language} code "
            f"(focus: {focus or 'general'})\n"
            f"--- review feedback ---\n{feedback}\n-----------------------"
        )
        return SkillResult(success=True, output=output)

    @staticmethod
    def _simulate_review(code: str, language: str, focus: str) -> str:
        lines = code.strip().split("\n")
        comments = [
            f"Line count: {len(lines)}",
            "✓ No obvious syntax errors detected (simulation)",
            "⚠ Consider adding docstrings to public functions",
            "⚠ Ensure error handling for edge cases",
        ]
        if focus == "security":
            comments.append("⚠ Check for SQL injection / input sanitisation")
        if focus == "performance":
            comments.append("⚠ Profile hot paths before optimising")
        return "\n".join(f"  {c}" for c in comments)
