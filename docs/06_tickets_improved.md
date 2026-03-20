# Improved Tickets

**Version:** 1.1 (after review `05_tickets_review.md`)  
**Date:** 2026-03-20  
**Changes:** Addresses I-1 through I-5

---

## T-001 · Package scaffold & pyproject.toml *(unchanged)*

**Priority:** critical | **Skills:** `file_ops`

Create `agentpipe/` directory, `__init__.py`, `pyproject.toml`, `requirements.txt`, `README_AGENTPIPE.md`.

**Done when:** `pip install -e .` succeeds and `agentpipe --help` runs.

---

## T-002 · Ticket model (`ticket.py`) *(minor update)*

**Priority:** high | **Skills:** `code_write` | **Depends on:** T-001

Implement `TicketStatus`, `TicketPriority`, and `Ticket` dataclass.  
**Update:** Ensure `updated_at` is refreshed on every `status` change via a `__setattr__` override or a `touch()` helper.

**Done when:** `from agentpipe.ticket import Ticket, TicketStatus` works.

---

## T-003 · Storage layer (`storage.py`) *(updated)*

**Priority:** high | **Skills:** `code_write` | **Depends on:** T-002

Implement `Storage` class for JSON persistence.  
**Update (I-1):** Add `threading.Lock` (`_lock`) to all write operations (`save_ticket`, `save_agent`, `save_config`) to prevent concurrent write collisions.

**Done when:** Concurrent workers can safely call `storage.save_ticket()` without data corruption.

---

## T-004 · Skill system (`skills/`) *(updated)*

**Priority:** high | **Skills:** `code_write` | **Depends on:** T-001

Implement `BaseSkill` ABC and six skills:
- `CodeWriteSkill`
- `CodeReviewSkill`
- `FileOpsSkill`
- `SearchSkill`
- `PlanSkill`
- `TestWriteSkill`  ← **NEW (I-2)**

**Done when:** All six skills importable and `.execute()` returns `SkillResult`.

---

## T-005 · Agent model (`agent.py`) *(updated)*

**Priority:** high | **Skills:** `code_write` | **Depends on:** T-004

Implement `Agent` dataclass.  
**Update (I-3):** `execute_ticket()` handles empty `skills_required` by falling back to `FileOpsSkill` (a "do nothing but log" default), and raises `ValueError` with a clear message if the required skill is not in the agent's registry.

**Done when:** An agent can execute tickets with or without `skills_required`.

---

## T-006 · Pipeline orchestrator (`pipeline.py`) *(updated)*

**Priority:** high | **Skills:** `code_write` | **Depends on:** T-003, T-005

Implement `Pipeline` class.  
**Update (I-4):** Dependency resolution:
- If `depends_on` tickets are all `done` → execute
- If any are `in_progress` → skip this round, add to `deferred` list
- If any are `failed` → mark this ticket as `blocked`
- After each round, re-queue `deferred` tickets

**Done when:** `Pipeline.run(parallel=True)` correctly respects ticket dependencies.

---

## T-007 · Worker (`worker.py`) *(unchanged)*

**Priority:** medium | **Skills:** `code_write` | **Depends on:** T-005

Thin wrapper for `ThreadPoolExecutor` usage.

**Done when:** Worker can be submitted to a ThreadPoolExecutor.

---

## T-008 · CLI (`cli.py`) *(updated)*

**Priority:** critical | **Skills:** `code_write` | **Depends on:** T-006, T-007

Implement all CLI commands.  
**Update (I-5):** Add `agentpipe ticket update <id> [--title] [--description] [--priority] [--skills]` command.

**Done when:** All commands work end-to-end including `ticket update`.

---

## T-009 · README & docs *(unchanged)*

**Priority:** medium | **Skills:** `file_ops` | **Depends on:** T-008

Write comprehensive `README_AGENTPIPE.md`.

**Done when:** A new user can follow README without reading source code.
