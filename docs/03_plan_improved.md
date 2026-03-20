# Improved Plan: AgentPipe — AI Agent Pipeline CLI

**Version:** 1.1 (after review of v1.0)  
**Date:** 2026-03-20  
**Changes from v1.0:** Addresses all gaps G-1 through G-7 from `02_plan_review.md`

---

## 1. Goal *(unchanged)*

Build a **CLI-first AI agent pipeline** called `agentpipe` that enables multiple AI agents to work on software projects via a ticket system, run in parallel, use a pluggable skill system, and be operated from the command line.

---

## 2. Core Components *(updated)*

| Component | Responsibility |
|-----------|---------------|
| **Ticket** | Unit of work; statuses: `todo`, `in_progress`, `review`, `done`, `failed`, `blocked`; optional `depends_on` |
| **Agent** | Named entity with a skill registry; executes tickets it has skills for |
| **Skill** | Pluggable capability with `execute(**kwargs) → SkillResult` |
| **Pipeline** | Orchestrates queue, routes tickets to capable agents, handles retries |
| **Worker** | Wraps an agent for `ThreadPoolExecutor` |
| **Storage** | JSON file persistence in `.agentpipe/` |
| **CLI** | Click-based command interface |

---

## 3. Updated Ticket Model

```python
@dataclass
class Ticket:
    id: str              # 8-char UUID prefix
    title: str
    description: str = ""
    priority: TicketPriority = "medium"
    status: TicketStatus = "todo"      # NEW: also "failed"
    assigned_to: str | None = None
    skills_required: list[str] = []
    depends_on: list[str] = []         # NEW: ticket IDs this depends on
    result: str | None = None          # Captured output stored here
    created_at: str = ...
    updated_at: str = ...
    retry_count: int = 0               # NEW: how many times retried
```

---

## 4. Updated CLI Commands

```
agentpipe init                              Init project
agentpipe ticket add <title> [options]      Add ticket
agentpipe ticket list [--status=all]        List tickets
agentpipe ticket show <id>                  Show details
agentpipe ticket assign <id> <agent>        Assign ticket
agentpipe ticket done <id>                  Mark as done    ← NEW
agentpipe ticket fail <id>                  Mark as failed  ← NEW
agentpipe agent list                        List agents
agentpipe agent add <name> --skills a,b,c   Add agent       ← UPDATED
agentpipe agent skills <name>               Show skills
agentpipe run [--parallel] [--agents N]     Run pipeline
agentpipe run --dry-run                     Dry run         ← NEW
agentpipe status                            Summary table
agentpipe plan "<goal>"                     Auto-plan
```

---

## 5. Skill Routing (NEW)

```python
def _find_agent_for(self, ticket: Ticket) -> Agent | None:
    """Return first available agent that has ALL required skills."""
    for agent in self.agents:
        if all(s in agent.skill_names for s in ticket.skills_required):
            return agent
    return None  # ticket blocked if no capable agent found
```

---

## 6. Error Handling & Retry (NEW)

- If `skill.execute()` raises an exception → ticket moves to `failed`
- `agentpipe run --retry-failed` → re-queues failed tickets
- `MAX_RETRIES = 3` – after 3 failures, ticket stays `failed` permanently

---

## 7. Dependency Resolution (NEW)

Before executing a ticket, the pipeline checks that all `depends_on` tickets are `done`. If not, the ticket is skipped in this round and re-queued (status stays `todo`).

---

## 8. Updated Success Criteria

- [ ] `pip install -e .` works
- [ ] `agentpipe init` creates `.agentpipe/` correctly
- [ ] `agentpipe ticket add "Write tests" --skills code_write,test_write` works
- [ ] `agentpipe run --parallel --agents 4` executes concurrently with skill routing
- [ ] `agentpipe run --dry-run` prints plan without executing
- [ ] `agentpipe status` shows table with counts per status
- [ ] Failed tickets move to `failed` state, can be retried
- [ ] Ticket dependencies respected in execution order
- [ ] All code passes linting (`ruff`)
