# AgentPipe

> 🤖 **CLI-first AI agent pipeline** – run multiple AI agents in parallel on your project tickets.

Inspired by QUAD Code and vibe-coding setups where agents independently pick up tickets, write code, review, test, and collaborate – all concurrently.

---

## What is AgentPipe?

AgentPipe is a **Python CLI tool** that lets you:

- 📋 **Manage tickets** (create, assign, track status)
- 🤖 **Define AI agents** with specific skills
- ⚡ **Run pipelines** – agents execute tickets concurrently using `ThreadPoolExecutor`
- 🔌 **Plug in real AI** – skill stubs are ready to swap for OpenAI / Anthropic / Ollama calls

---

## Installation

```bash
pip install -e .
```

Requires Python ≥ 3.11.

---

## Quick Start

```bash
# 1. Initialise a project
agentpipe init my-project

# 2. See default agents
agentpipe agent list

# 3. Add tickets
agentpipe ticket add "Build user auth" --skills code_write --priority high
agentpipe ticket add "Review auth module" --skills code_review
agentpipe ticket add "Write auth tests" --skills test_write

# 4. Run pipeline (all tickets in parallel)
agentpipe run --parallel

# 5. Check status
agentpipe status
```

### Or – auto-generate tickets from a goal

```bash
agentpipe plan "Build a REST API with JWT authentication" --max-tickets 6
agentpipe run --parallel --agents 4
```

---

## Command Reference

### Project

| Command | Description |
|---------|-------------|
| `agentpipe init [name]` | Initialise project in current directory |
| `agentpipe status` | Show ticket count summary |

### Tickets

| Command | Description |
|---------|-------------|
| `agentpipe ticket add <title>` | Create a ticket |
| `agentpipe ticket list [--status=todo]` | List tickets (optionally filtered) |
| `agentpipe ticket show <id>` | Full ticket details including result |
| `agentpipe ticket assign <id> <agent>` | Manually assign to an agent |
| `agentpipe ticket done <id>` | Mark as done |
| `agentpipe ticket fail <id>` | Mark as failed |
| `agentpipe ticket update <id> [--title] [--description] [--priority] [--skills]` | Update fields |

**Ticket options for `add`:**

```bash
agentpipe ticket add "My task" \
  --skills code_write,test_write \   # required agent skills
  --priority high \                  # low | medium | high | critical
  --description "Details here" \
  --depends-on abc12345,def67890     # IDs this ticket depends on
```

### Agents

| Command | Description |
|---------|-------------|
| `agentpipe agent list` | List all agents |
| `agentpipe agent add <name> --skills a,b,c` | Register a new agent |
| `agentpipe agent skills [name]` | List all skills, or show specific agent's skills |

### Pipeline

| Command | Description |
|---------|-------------|
| `agentpipe run` | Execute all TODO tickets sequentially |
| `agentpipe run --parallel` | Execute concurrently (default 4 workers) |
| `agentpipe run --agents 8` | Set worker count |
| `agentpipe run --dry-run` | Preview what would run without executing |
| `agentpipe run --retry-failed` | Reset failed tickets to TODO and retry |

### Planning

```bash
agentpipe plan "Build a data pipeline" --max-tickets 5 --priority high
```

---

## Built-in Skills

| Skill | Description |
|-------|-------------|
| `code_write` | Writes code for a task (stub → swap for LLM) |
| `code_review` | Reviews code for bugs/style |
| `file_ops` | Reads, writes, appends files |
| `search` | Searches for information (stub → swap for SerpAPI/Tavily) |
| `plan` | Decomposes a goal into sub-tickets |
| `test_write` | Writes pytest tests (stub → swap for LLM) |

---

## Default Agents

| Agent | Skills | Description |
|-------|--------|-------------|
| `planner` | plan, search | Decomposes goals into tickets |
| `coder` | code_write, file_ops | Writes and saves code |
| `reviewer` | code_review, search | Reviews and researches |
| `tester` | test_write, code_review | Writes and reviews tests |

---

## Architecture

```
agentpipe/
├── cli.py           ← click CLI entry point
├── pipeline.py      ← Pipeline orchestrator
│   ├── _find_agent_for()    skill-based routing
│   ├── _deps_satisfied()    dependency resolution
│   ├── _run_sequential()    queue-based execution
│   └── _run_parallel()      ThreadPoolExecutor
├── worker.py        ← Wraps Agent for executor
├── agent.py         ← Agent with skill registry
├── ticket.py        ← Ticket model + enums
├── storage.py       ← Thread-safe JSON storage
└── skills/
    ├── base.py      ← BaseSkill ABC + SkillResult
    ├── code_write.py
    ├── code_review.py
    ├── file_ops.py
    ├── search.py
    ├── plan.py
    └── test_write.py
```

**Parallel execution model:**

```
Pipeline.run(parallel=True, max_workers=4)
  └── ThreadPoolExecutor(max_workers=4)
       ├── Worker(coder).run(ticket_1)     → DONE
       ├── Worker(reviewer).run(ticket_2)  → DONE
       ├── Worker(tester).run(ticket_3)    → DONE
       └── Worker(coder).run(ticket_4)     → DONE
```

**Dependency resolution:**
- Deps all `done` → execute  
- Any dep `in_progress` → defer to next round  
- Any dep `failed` → mark as `blocked`

---

## Extending with Real AI

Each skill has a `_simulate_*` method. Replace it with a real LLM call:

```python
from agentpipe.skills.code_write import CodeWriteSkill
from agentpipe.skills.base import SkillResult
import openai

class GPTCodeWriteSkill(CodeWriteSkill):
    def _simulate_code(self, task: str, language: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Write {language} code."},
                {"role": "user", "content": task},
            ],
        )
        return response.choices[0].message.content
```

Register it with any agent and run – the rest of the pipeline is unchanged.

---

## Storage Layout

All state lives in `.agentpipe/` (git-ignorable):

```
.agentpipe/
├── config.json
├── tickets/
│   ├── abc12345.json
│   └── def67890.json
└── agents/
    ├── planner.json
    └── coder.json
```

Add `.agentpipe/` to `.gitignore` or commit it to share project state with your team.

---

## Running Tests

```bash
pytest tests/ -v
```

75 tests covering tickets, storage, skills, agent, pipeline, worker, and CLI.
