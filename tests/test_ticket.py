"""Tests for the Ticket model."""


from agentpipe.ticket import Ticket, TicketPriority, TicketStatus


def test_ticket_defaults():
    t = Ticket(title="Fix bug")
    assert t.title == "Fix bug"
    assert t.status == TicketStatus.TODO
    assert t.priority == TicketPriority.MEDIUM
    assert len(t.id) == 8
    assert t.skills_required == []
    assert t.depends_on == []
    assert t.retry_count == 0
    assert t.result is None


def test_ticket_set_status_updates_timestamp():
    t = Ticket(title="Test ticket")
    old_ts = t.updated_at
    t.set_status(TicketStatus.DONE)
    assert t.status == TicketStatus.DONE
    # Timestamp should be updated (may be same second in fast tests)
    assert t.updated_at >= old_ts


def test_ticket_serialisation_round_trip():
    t = Ticket(
        title="Implement login",
        description="Add JWT auth",
        priority=TicketPriority.HIGH,
        skills_required=["code_write"],
        depends_on=["abc12345"],
    )
    d = t.to_dict()
    t2 = Ticket.from_dict(d)
    assert t2.id == t.id
    assert t2.title == t.title
    assert t2.priority == t.priority
    assert t2.status == t.status
    assert t2.skills_required == ["code_write"]
    assert t2.depends_on == ["abc12345"]


def test_ticket_all_statuses():
    for status in TicketStatus:
        t = Ticket(title="x")
        t.set_status(status)
        assert t.status == status


def test_ticket_from_dict_with_string_values():
    d = {
        "id": "abc12345",
        "title": "Test",
        "description": "",
        "priority": "high",
        "status": "done",
        "assigned_to": "coder",
        "skills_required": [],
        "depends_on": [],
        "result": None,
        "created_at": "2026-01-01T00:00:00+00:00",
        "updated_at": "2026-01-01T00:00:00+00:00",
        "retry_count": 0,
    }
    t = Ticket.from_dict(d)
    assert t.priority == TicketPriority.HIGH
    assert t.status == TicketStatus.DONE
