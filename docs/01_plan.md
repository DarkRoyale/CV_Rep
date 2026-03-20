# Plan: AgentPipe — AI Agent Pipeline CLI

**Version:** 1.0  
**Date:** 2026-03-20  
**Author:** GitHub Copilot

---

## 1. Goal

Build a **CLI-first AI agent pipeline** called `agentpipe` that enables multiple AI agents to:
- Work on software projects via a **ticket system**
- Execute tickets **in parallel** using a pool of workers
- Use a **skill system** that is pluggable and replaceable with real LLM backends
- Be run from the command line with simple, memorable commands

The vision is similar to QUAD Code / Vibe-coding setups on YouTube: a pipeline where agents with different specializations autonomously handle tickets, from planning to code writing, reviewing, and testing.

---

## 2. Core Components

| Component | Responsibility |
|-----------|---------------|
| **Ticket** | Unit of work with status, priority, assigned agent, skills required |
| **Agent** | Named entity with a set of skills; executes tickets |
| **Skill** | Pluggable capability (write code, review, search, plan, file ops) |
| **Pipeline** | Orchestrates the ticket queue and agent pool |
| **Worker** | Wraps an agent for concurrent/parallel execution |
| **Storage** | JSON file-based persistence in `.agentpipe/` |
| **CLI** | Click-based command interface |

---

## 3. Directory Layout

```
agentpipe/
├── __init__.py
├── cli.py           # Entry point: click commands
├── agent.py         # Agent class with skill registry
├── pipeline.py      # Pipeline orchestrator
├── ticket.py        # Ticket model + enums
├── worker.py        # ThreadPoolExecutor wrapper
├── storage.py       # JSON file storage
└── skills/
    ├── __init__.py
    ├── base.py       # BaseSkill ABC + SkillResult
    ├── code_write.py # Write code skill
    ├── code_review.py# Review code skill
    ├── file_ops.py   # File operations skill
    ├── search.py     # Search/research skill
    └── plan.py       # Planning / ticket decomposition skill
```

---

## 4. CLI Commands

```
agentpipe init                         Init project (create .agentpipe/)
agentpipe ticket add <title>           Add a ticket
agentpipe ticket list                  List all tickets
agentpipe ticket show <id>             Show ticket details
agentpipe ticket assign <id> <agent>   Assign ticket to agent
agentpipe agent list                   List available agents
agentpipe agent add <name> <skills>    Register a new agent
agentpipe agent skills <name>          Show agent's skills
agentpipe run                          Run pipeline (sequential)
agentpipe run --parallel               Run pipeline (parallel)
agentpipe run --agents N               Number of parallel agents
agentpipe status                       Show overall pipeline status
agentpipe plan "<goal>"                Auto-generate tickets from a goal
```

---

## 5. Skill System

Each skill:
- Inherits from `BaseSkill`
- Has `name`, `description`, `input_schema`
- Implements `execute(**kwargs) -> SkillResult`
- Is swappable with a real LLM backend

Default skills: `code_write`, `code_review`, `file_ops`, `search`, `plan`, `test_write`

---

## 6. Parallel Execution Model

```
Pipeline.run(parallel=True, max_workers=4)
  └── ThreadPoolExecutor(max_workers=4)
       ├── Worker(agent_1).execute(ticket_1)
       ├── Worker(agent_2).execute(ticket_2)
       ├── Worker(agent_3).execute(ticket_3)
       └── Worker(agent_4).execute(ticket_4)
```

---

## 7. Storage Model

All state stored in `.agentpipe/` (per-project):
```
.agentpipe/
├── config.json       # Project config
├── tickets/
│   ├── abc123.json   # One file per ticket
│   └── def456.json
└── agents/
    ├── planner.json  # Agent definition
    └── coder.json
```

---

## 8. Success Criteria

- [ ] `pip install -e .` works
- [ ] `agentpipe init` creates `.agentpipe/` correctly
- [ ] `agentpipe ticket add "Write tests"` works
- [ ] `agentpipe run --parallel` executes all TODO tickets concurrently
- [ ] `agentpipe status` shows a clear summary table
- [ ] Skills can be listed and described
- [ ] All code passes linting
