# Plan Review

**Reviewing:** `docs/01_plan.md`  
**Date:** 2026-03-20

---

## ✅ Strengths

1. **Clear component breakdown** – The table mapping components to responsibilities is immediately understandable.
2. **Parallel execution model** is explicitly ASCII-diagrammed – good for communicating the architecture.
3. **CLI interface** covers all key user flows (init → add tickets → run → status).
4. **Storage model** using a `.agentpipe/` directory is pragmatic and self-contained.
5. **Skill system** with swappable backends is future-proof.

## ⚠️ Gaps & Issues

### G-1: No error handling strategy
The plan doesn't describe what happens when an agent fails mid-execution. Should failed tickets be retried? Moved to a `failed` state?

### G-2: No ticket dependency model
Tickets can depend on each other (e.g., "write tests" depends on "write code"). Without this, parallel execution could produce race conditions.

### G-3: Skill routing not specified
The plan mentions `skills_required` on tickets but doesn't describe *how* the pipeline matches tickets to agents. A ticket requiring `code_review` should only go to an agent that has `code_review`.

### G-4: No output capture model
When an agent executes a ticket, where does the output go? It should be stored back on the ticket (`result` field) and optionally written to a file.

### G-5: Missing `ticket done` / `ticket fail` commands
CLI should allow manually marking tickets as done or failed.

### G-6: No `--dry-run` flag
Users should be able to see what *would* be executed without actually running.

### G-7: Agent `add` command needs clarification
How are skills specified? As a comma-separated list? As a config file?

---

## 📝 Recommendations

| # | Recommendation |
|---|---------------|
| R-1 | Add `failed` ticket status + retry logic |
| R-2 | Add `depends_on: list[str]` to Ticket model |
| R-3 | Add skill-based routing: `pipeline._find_agent_for(ticket)` |
| R-4 | Ensure `SkillResult.output` is stored back to ticket's `result` field |
| R-5 | Add `agentpipe ticket done <id>` and `ticket fail <id>` commands |
| R-6 | Add `agentpipe run --dry-run` flag |
| R-7 | Agent skills specified as `--skills "code_write,code_review"` flag |

---

## Overall Assessment

The plan is **solid and complete** at a high level. The identified gaps are refinements rather than fundamental flaws. Proceed with improvements, then break into tickets.

**Score: 8/10**
