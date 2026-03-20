# Tickets Breakdown

**Source:** `docs/03_plan_improved.md`  
**Date:** 2026-03-20  
**Total tickets:** 9

---

## T-001 · Package scaffold & pyproject.toml

**Priority:** critical  
**Skills required:** `file_ops`  
**Description:**  
Create the `agentpipe/` directory, `__init__.py`, `pyproject.toml`, `requirements.txt`, and `README_AGENTPIPE.md`. This is the foundation all other tickets depend on.

**Done when:** `pip install -e .` succeeds and `agentpipe --help` runs.

---

## T-002 · Ticket model (`ticket.py`)

**Priority:** high  
**Skills required:** `code_write`  
**Depends on:** T-001  
**Description:**  
Implement `TicketStatus` enum (`todo`, `in_progress`, `review`, `done`, `failed`, `blocked`), `TicketPriority` enum, and `Ticket` dataclass with all fields including `depends_on`, `retry_count`, `result`. Add `to_dict()` / `from_dict()` methods.

**Done when:** `from agentpipe.ticket import Ticket, TicketStatus` works.

---

## T-003 · Storage layer (`storage.py`)

**Priority:** high  
**Skills required:** `code_write`  
**Depends on:** T-002  
**Description:**  
Implement `Storage` class that reads/writes tickets and agents as JSON files in `.agentpipe/`. Methods: `init_project()`, `save_ticket()`, `load_ticket()`, `list_tickets()`, `save_agent()`, `load_agent()`, `list_agents()`, `load_config()`, `save_config()`.

**Done when:** Tickets persist across CLI invocations.

---

## T-004 · Skill system (`skills/`)

**Priority:** high  
**Skills required:** `code_write`  
**Depends on:** T-001  
**Description:**  
Implement `BaseSkill` ABC with `name`, `description`, `execute()`. Implement five skills:
- `CodeWriteSkill` – simulates writing code
- `CodeReviewSkill` – simulates reviewing code
- `FileOpsSkill` – reads/writes files
- `SearchSkill` – simulates searching
- `PlanSkill` – decomposes a goal into sub-tickets

**Done when:** All skills can be imported and `.execute()` returns a `SkillResult`.

---

## T-005 · Agent model (`agent.py`)

**Priority:** high  
**Skills required:** `code_write`  
**Depends on:** T-004  
**Description:**  
Implement `Agent` dataclass with `name`, `skills: list[BaseSkill]`, `skill_names` property, `has_skill()`, `execute_ticket()` method. `execute_ticket()` calls the appropriate skill based on `ticket.skills_required[0]` (first required skill wins).

**Done when:** An agent can be created with skills and can execute a ticket.

---

## T-006 · Pipeline orchestrator (`pipeline.py`)

**Priority:** high  
**Skills required:** `code_write`  
**Depends on:** T-003, T-005  
**Description:**  
Implement `Pipeline` class with `agents`, `storage`, `_find_agent_for()` (skill routing), `run()` (sequential), `run_parallel()` (ThreadPoolExecutor). Handle `depends_on` resolution and failed ticket retry logic. Emit progress events (print to stdout).

**Done when:** `Pipeline.run(parallel=True)` executes all TODO tickets concurrently.

---

## T-007 · Worker (`worker.py`)

**Priority:** medium  
**Skills required:** `code_write`  
**Depends on:** T-005  
**Description:**  
Implement `Worker` class wrapping an `Agent` for use with `ThreadPoolExecutor`. Has a `run(ticket, storage)` method that executes the ticket, updates status, saves result back to storage, and handles exceptions gracefully.

**Done when:** Worker can be submitted to a ThreadPoolExecutor.

---

## T-008 · CLI (`cli.py`)

**Priority:** critical  
**Skills required:** `code_write`  
**Depends on:** T-006, T-007  
**Description:**  
Implement all CLI commands using `click`:
- `init`, `status`
- `ticket add/list/show/assign/done/fail`
- `agent list/add/skills`
- `run [--parallel] [--agents N] [--dry-run] [--retry-failed]`
- `plan "<goal>"`

Use `rich` for table output. Register default agents (planner, coder, reviewer, tester) on `init`.

**Done when:** All commands work end-to-end.

---

## T-009 · README & docs (`README_AGENTPIPE.md`)

**Priority:** medium  
**Skills required:** `file_ops`  
**Depends on:** T-008  
**Description:**  
Write comprehensive README with: overview, installation, quick start, command reference, skill list, architecture diagram, and extension guide.

**Done when:** A new user can follow README to get started without reading source code.
