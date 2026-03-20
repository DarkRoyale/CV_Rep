"""FileOpsSkill – reads and writes files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentpipe.skills.base import BaseSkill, SkillResult


class FileOpsSkill(BaseSkill):
    name = "file_ops"
    description = "Reads, writes, appends, or lists files on disk."
    input_schema = {
        "operation": "str – 'read' | 'write' | 'append' | 'list'",
        "path": "str – file or directory path",
        "content": "str – content to write (for write/append)",
    }

    def execute(self, *, operation: str = "read", path: str = "", content: str = "", **_: Any) -> SkillResult:
        if not path:
            return SkillResult(success=False, error="'path' parameter is required")
        try:
            p = Path(path)
            if operation == "read":
                text = p.read_text(encoding="utf-8")
                return SkillResult(success=True, output=f"[file_ops:read] {path}\n{text}")
            elif operation == "write":
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
                return SkillResult(success=True, output=f"[file_ops:write] Wrote {len(content)} chars to {path}")
            elif operation == "append":
                p.parent.mkdir(parents=True, exist_ok=True)
                with p.open("a", encoding="utf-8") as fh:
                    fh.write(content)
                return SkillResult(success=True, output=f"[file_ops:append] Appended {len(content)} chars to {path}")
            elif operation == "list":
                entries = [str(e) for e in sorted(p.iterdir())] if p.is_dir() else []
                return SkillResult(success=True, output=f"[file_ops:list] {path}\n" + "\n".join(entries))
            else:
                return SkillResult(success=False, error=f"Unknown operation: {operation!r}")
        except OSError as exc:
            return SkillResult(success=False, error=str(exc))
