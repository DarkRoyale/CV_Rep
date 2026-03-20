"""Tests for the skill system."""


from agentpipe.skills import SKILL_REGISTRY
from agentpipe.skills.base import SkillResult
from agentpipe.skills.code_review import CodeReviewSkill
from agentpipe.skills.code_write import CodeWriteSkill
from agentpipe.skills.file_ops import FileOpsSkill
from agentpipe.skills.plan import PlanSkill
from agentpipe.skills.search import SearchSkill
from agentpipe.skills.test_write import TestWriteSkill

# ---------------------------------------------------------------------------
# SkillResult
# ---------------------------------------------------------------------------

def test_skill_result_success_str():
    r = SkillResult(success=True, output="hello")
    assert str(r) == "hello"


def test_skill_result_error_str():
    r = SkillResult(success=False, error="boom")
    assert "boom" in str(r)


# ---------------------------------------------------------------------------
# SKILL_REGISTRY
# ---------------------------------------------------------------------------

def test_skill_registry_contains_all_skills():
    expected = {"code_write", "code_review", "file_ops", "search", "plan", "test_write"}
    assert expected == set(SKILL_REGISTRY.keys())


# ---------------------------------------------------------------------------
# CodeWriteSkill
# ---------------------------------------------------------------------------

def test_code_write_success():
    skill = CodeWriteSkill()
    result = skill.execute(task="Add login endpoint")
    assert result.success
    assert "login" in str(result.output).lower()


def test_code_write_requires_task():
    skill = CodeWriteSkill()
    result = skill.execute()
    assert not result.success
    assert result.error


# ---------------------------------------------------------------------------
# CodeReviewSkill
# ---------------------------------------------------------------------------

def test_code_review_success():
    skill = CodeReviewSkill()
    result = skill.execute(code="def main(): pass")
    assert result.success
    assert "review" in str(result.output).lower()


def test_code_review_requires_code():
    skill = CodeReviewSkill()
    result = skill.execute()
    assert not result.success


# ---------------------------------------------------------------------------
# FileOpsSkill
# ---------------------------------------------------------------------------

def test_file_ops_write_read(tmp_path):
    skill = FileOpsSkill()
    p = str(tmp_path / "test.txt")
    write_result = skill.execute(operation="write", path=p, content="hello world")
    assert write_result.success

    read_result = skill.execute(operation="read", path=p)
    assert read_result.success
    assert "hello world" in str(read_result.output)


def test_file_ops_append(tmp_path):
    skill = FileOpsSkill()
    p = str(tmp_path / "log.txt")
    skill.execute(operation="write", path=p, content="line1\n")
    skill.execute(operation="append", path=p, content="line2\n")
    read_result = skill.execute(operation="read", path=p)
    assert "line1" in str(read_result.output)
    assert "line2" in str(read_result.output)


def test_file_ops_list(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    skill = FileOpsSkill()
    result = skill.execute(operation="list", path=str(tmp_path))
    assert result.success
    assert "a.txt" in str(result.output)


def test_file_ops_requires_path():
    skill = FileOpsSkill()
    result = skill.execute(operation="read")
    assert not result.success


def test_file_ops_unknown_operation():
    skill = FileOpsSkill()
    result = skill.execute(operation="delete", path="/tmp/x")
    assert not result.success


# ---------------------------------------------------------------------------
# SearchSkill
# ---------------------------------------------------------------------------

def test_search_success():
    skill = SearchSkill()
    result = skill.execute(query="Python async patterns")
    assert result.success
    assert "Python async" in str(result.output)


def test_search_requires_query():
    skill = SearchSkill()
    result = skill.execute()
    assert not result.success


# ---------------------------------------------------------------------------
# PlanSkill
# ---------------------------------------------------------------------------

def test_plan_success():
    skill = PlanSkill()
    result = skill.execute(goal="Build a todo app")
    assert result.success
    output = str(result.output)
    assert "todo app" in output.lower()


def test_plan_requires_goal():
    skill = PlanSkill()
    result = skill.execute()
    assert not result.success


def test_plan_max_tickets():
    skill = PlanSkill()
    result = skill.execute(goal="Build something", max_tickets=2)
    assert result.success
    # Should have at most 2 sub-ticket lines
    lines = [line for line in str(result.output).split("\n") if line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6."))]
    assert len(lines) <= 2


# ---------------------------------------------------------------------------
# TestWriteSkill
# ---------------------------------------------------------------------------

def test_test_write_success():
    skill = TestWriteSkill()
    result = skill.execute(target="my_function")
    assert result.success
    assert "my_function" in str(result.output).lower()


def test_test_write_requires_target():
    skill = TestWriteSkill()
    result = skill.execute()
    assert not result.success
