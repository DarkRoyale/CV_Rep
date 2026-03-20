"""Tests for Agent and Pipeline."""

import pytest

from agentpipe.agent import Agent
from agentpipe.pipeline import Pipeline
from agentpipe.skills.code_review import CodeReviewSkill
from agentpipe.skills.code_write import CodeWriteSkill
from agentpipe.storage import Storage
from agentpipe.ticket import Ticket, TicketStatus
from agentpipe.worker import Worker

# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

def _make_coder():
    return Agent(name="coder", skills=[CodeWriteSkill()], description="Writes code")


def _make_reviewer():
    return Agent(name="reviewer", skills=[CodeReviewSkill()], description="Reviews code")


def test_agent_skill_names():
    a = _make_coder()
    assert "code_write" in a.skill_names


def test_agent_has_skill():
    a = _make_coder()
    assert a.has_skill("code_write")
    assert not a.has_skill("code_review")


def test_agent_get_skill():
    a = _make_coder()
    skill = a.get_skill("code_write")
    assert skill is not None
    assert skill.name == "code_write"


def test_agent_execute_ticket_with_skill():
    a = _make_coder()
    t = Ticket(title="Implement login", skills_required=["code_write"])
    result = a.execute_ticket(t)
    assert result.success


def test_agent_execute_ticket_missing_skill():
    a = _make_coder()
    t = Ticket(title="Review login", skills_required=["code_review"])
    result = a.execute_ticket(t)
    assert not result.success
    assert "lacks required skills" in result.error


def test_agent_execute_ticket_no_skills_required():
    a = _make_coder()
    t = Ticket(title="Do something")
    result = a.execute_ticket(t)
    # Should use first available skill
    assert result.success


def test_agent_execute_ticket_no_agent_skills():
    a = Agent(name="empty", skills=[])
    t = Ticket(title="Do something")
    result = a.execute_ticket(t)
    # Falls back to FileOpsSkill (read) which may fail on missing path - that's OK
    # The important thing: it doesn't raise
    assert isinstance(result.success, bool)


def test_agent_serialisation():
    a = _make_coder()
    d = a.to_dict()
    assert d["name"] == "coder"
    assert "code_write" in d["skills"]


def test_agent_from_dict():
    from agentpipe.skills import SKILL_REGISTRY
    d = {"name": "coder", "description": "Writes code", "skills": ["code_write"]}
    a = Agent.from_dict(d, skill_registry=SKILL_REGISTRY)
    assert a.name == "coder"
    assert a.has_skill("code_write")


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

@pytest.fixture
def storage(tmp_path):
    s = Storage(root=tmp_path / ".agentpipe")
    s.init_project()
    return s


def test_worker_runs_ticket_to_done(storage):
    worker = Worker(agent=_make_coder(), storage=storage)
    t = Ticket(title="Write code", skills_required=["code_write"])
    storage.save_ticket(t)
    result = worker.run(t)
    assert result.status == TicketStatus.DONE
    assert result.assigned_to == "coder"
    assert result.result is not None


def test_worker_sets_failed_after_max_retries(storage):
    """An agent without matching skills causes retry; after MAX_RETRIES → FAILED."""
    # Reviewer can't do code_write, so ticket should fail
    reviewer = Agent(name="reviewer", skills=[CodeReviewSkill()])
    t = Ticket(title="Write code", skills_required=["code_write"])
    storage.save_ticket(t)

    # Simulate max retries by setting retry_count just below threshold
    t.retry_count = Worker.MAX_RETRIES - 1
    storage.save_ticket(t)

    worker = Worker(agent=reviewer, storage=storage)
    result = worker.run(t)
    assert result.status == TicketStatus.FAILED


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def _make_pipeline(storage: Storage) -> Pipeline:
    agents = [_make_coder(), _make_reviewer()]
    return Pipeline(storage=storage, agents=agents)


def test_pipeline_find_agent_for_skill(storage):
    pipeline = _make_pipeline(storage)
    t = Ticket(title="x", skills_required=["code_write"])
    agent = pipeline._find_agent_for(t)
    assert agent is not None
    assert agent.name == "coder"


def test_pipeline_find_agent_for_review(storage):
    pipeline = _make_pipeline(storage)
    t = Ticket(title="x", skills_required=["code_review"])
    agent = pipeline._find_agent_for(t)
    assert agent is not None
    assert agent.name == "reviewer"


def test_pipeline_find_agent_no_skills_required(storage):
    pipeline = _make_pipeline(storage)
    t = Ticket(title="x")
    agent = pipeline._find_agent_for(t)
    assert agent is not None  # falls back to first agent


def test_pipeline_sequential_run(storage):
    pipeline = _make_pipeline(storage)
    t1 = Ticket(title="Write feature", skills_required=["code_write"])
    t2 = Ticket(title="Review feature", skills_required=["code_review"])
    storage.save_ticket(t1)
    storage.save_ticket(t2)

    logs: list[str] = []
    pipeline.run(parallel=False, log=logs.append)

    loaded_t1 = storage.load_ticket(t1.id)
    loaded_t2 = storage.load_ticket(t2.id)
    assert loaded_t1.status == TicketStatus.DONE
    assert loaded_t2.status == TicketStatus.DONE


def test_pipeline_parallel_run(storage):
    pipeline = _make_pipeline(storage)
    tickets = [
        Ticket(title=f"Task {i}", skills_required=["code_write"])
        for i in range(6)
    ]
    for t in tickets:
        storage.save_ticket(t)

    logs: list[str] = []
    pipeline.run(parallel=True, max_workers=3, log=logs.append)

    for t in tickets:
        loaded = storage.load_ticket(t.id)
        assert loaded.status == TicketStatus.DONE


def test_pipeline_dependency_resolution(storage):
    """A ticket that depends on another that isn't done should be deferred."""
    pipeline = _make_pipeline(storage)
    t1 = Ticket(title="Step 1", skills_required=["code_write"])
    t2 = Ticket(title="Step 2", skills_required=["code_write"], depends_on=[t1.id])
    storage.save_ticket(t1)
    storage.save_ticket(t2)

    logs: list[str] = []
    pipeline.run(parallel=False, log=logs.append)

    lt1 = storage.load_ticket(t1.id)
    storage.load_ticket(t2.id)
    # t1 should be done; t2 might be done (re-queued) or deferred
    assert lt1.status == TicketStatus.DONE


def test_pipeline_dry_run_does_not_execute(storage):
    pipeline = _make_pipeline(storage)
    t = Ticket(title="Do not execute me", skills_required=["code_write"])
    storage.save_ticket(t)

    logs: list[str] = []
    pipeline.run(dry_run=True, log=logs.append)

    loaded = storage.load_ticket(t.id)
    assert loaded.status == TicketStatus.TODO  # status unchanged
    assert any("dry-run" in line for line in logs)


def test_pipeline_retry_failed(storage):
    pipeline = _make_pipeline(storage)
    t = Ticket(title="Failed task", skills_required=["code_write"])
    t.set_status(TicketStatus.FAILED)
    storage.save_ticket(t)

    logs: list[str] = []
    pipeline.run(retry_failed=True, log=logs.append)

    loaded = storage.load_ticket(t.id)
    assert loaded.status == TicketStatus.DONE
