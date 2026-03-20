"""Skill implementations for AgentPipe."""

from agentpipe.skills.base import BaseSkill, SkillResult
from agentpipe.skills.code_review import CodeReviewSkill
from agentpipe.skills.code_write import CodeWriteSkill
from agentpipe.skills.file_ops import FileOpsSkill
from agentpipe.skills.plan import PlanSkill
from agentpipe.skills.search import SearchSkill
from agentpipe.skills.test_write import TestWriteSkill

__all__ = [
    "BaseSkill",
    "SkillResult",
    "CodeWriteSkill",
    "CodeReviewSkill",
    "FileOpsSkill",
    "SearchSkill",
    "PlanSkill",
    "TestWriteSkill",
]

ALL_SKILLS: list[type[BaseSkill]] = [
    CodeWriteSkill,
    CodeReviewSkill,
    FileOpsSkill,
    SearchSkill,
    PlanSkill,
    TestWriteSkill,
]

SKILL_REGISTRY: dict[str, type[BaseSkill]] = {cls().name: cls for cls in ALL_SKILLS}
