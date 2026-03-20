"""CodeWriteSkill – writes code for a given task."""

from __future__ import annotations

import textwrap
from typing import Any

from agentpipe.skills.base import BaseSkill, SkillResult


class CodeWriteSkill(BaseSkill):
    name = "code_write"
    description = "Writes code to implement a described feature or fix."
    input_schema = {
        "task": "str – description of what to implement",
        "language": "str – programming language (default: python)",
        "context": "str – optional surrounding context",
    }

    def execute(self, *, task: str = "", language: str = "python", context: str = "", **_: Any) -> SkillResult:
        if not task:
            return SkillResult(success=False, error="'task' parameter is required")
        code = self._simulate_code(task, language)
        output = (
            f"[code_write] Wrote {language} code for: {task!r}\n"
            f"  Context used: {context!r}\n"
            f"--- generated code ---\n{code}\n----------------------"
        )
        return SkillResult(success=True, output=output)

    @staticmethod
    def _simulate_code(task: str, language: str) -> str:
        """Produce a representative stub – swap with real LLM call."""
        if language.lower() == "python":
            return textwrap.dedent(f"""\
                # TODO: implement – {task}
                def main():
                    raise NotImplementedError("{task}")
                """)
        return f"// TODO: implement – {task}"
