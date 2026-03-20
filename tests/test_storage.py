"""Tests for the Storage layer."""

import pytest

from agentpipe.storage import Storage
from agentpipe.ticket import Ticket


@pytest.fixture
def storage(tmp_path):
    return Storage(root=tmp_path / ".agentpipe")


def test_init_project_creates_dirs(storage, tmp_path):
    storage.init_project(name="test-project")
    assert (tmp_path / ".agentpipe").exists()
    assert (tmp_path / ".agentpipe" / "tickets").exists()
    assert (tmp_path / ".agentpipe" / "agents").exists()
    assert (tmp_path / ".agentpipe" / "config.json").exists()


def test_is_not_initialised_before_init(storage):
    assert not storage.is_initialised()


def test_is_initialised_after_init(storage):
    storage.init_project()
    assert storage.is_initialised()


def test_save_and_load_ticket(storage):
    storage.init_project()
    t = Ticket(title="Test task")
    storage.save_ticket(t)
    loaded = storage.load_ticket(t.id)
    assert loaded is not None
    assert loaded.id == t.id
    assert loaded.title == t.title


def test_list_tickets_empty(storage):
    storage.init_project()
    assert storage.list_tickets() == []


def test_list_tickets_returns_all(storage):
    storage.init_project()
    t1 = Ticket(title="Task 1")
    t2 = Ticket(title="Task 2")
    storage.save_ticket(t1)
    storage.save_ticket(t2)
    tickets = storage.list_tickets()
    assert len(tickets) == 2


def test_delete_ticket(storage):
    storage.init_project()
    t = Ticket(title="Disposable")
    storage.save_ticket(t)
    assert storage.load_ticket(t.id) is not None
    assert storage.delete_ticket(t.id)
    assert storage.load_ticket(t.id) is None


def test_load_nonexistent_ticket(storage):
    storage.init_project()
    assert storage.load_ticket("notexist") is None


def test_save_and_load_agent(storage):
    storage.init_project()
    agent_dict = {"name": "coder", "description": "Writes code", "skills": ["code_write"]}
    storage.save_agent(agent_dict)
    loaded = storage.load_agent("coder")
    assert loaded == agent_dict


def test_list_agents(storage):
    storage.init_project()
    storage.save_agent({"name": "agent1", "skills": []})
    storage.save_agent({"name": "agent2", "skills": []})
    agents = storage.list_agents()
    assert len(agents) == 2


def test_save_and_load_config(storage):
    storage.init_project(name="my-proj")
    config = storage.load_config()
    assert config["name"] == "my-proj"

    storage.save_config({"name": "updated"})
    config2 = storage.load_config()
    assert config2["name"] == "updated"


def test_concurrent_saves(storage):
    """Storage should handle concurrent saves via threading.Lock."""
    import concurrent.futures

    storage.init_project()
    tickets = [Ticket(title=f"Ticket {i}") for i in range(20)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(storage.save_ticket, t) for t in tickets]
        for f in concurrent.futures.as_completed(futures):
            f.result()  # should not raise

    loaded = storage.list_tickets()
    assert len(loaded) == 20
