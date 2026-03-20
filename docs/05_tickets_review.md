# Tickets Review

**Reviewing:** `docs/04_tickets.md`  
**Date:** 2026-03-20

---

## Per-ticket review

### T-001 ✅ Good
Clear scope, good entry point. No issues.

### T-002 ✅ Good
Ticket model is well-defined. One addition: the description should mention that `updated_at` is updated every time status changes.

### T-003 ⚠️ Gap
The storage layer doesn't mention **locking** for concurrent writes. When two workers finish at the same time and both call `save_ticket()`, there could be a write collision. Add a `threading.Lock` to `Storage`.

### T-004 ✅ Good
Skill decomposition is clear. Minor: add `TestWriteSkill` to the list (mentioned in plan but missing from ticket).

### T-005 ⚠️ Gap
`execute_ticket()` only uses `skills_required[0]`. What if the ticket has no `skills_required`? Should fall back to a default skill or raise a clear error.

### T-006 ⚠️ Gap
Dependency resolution algorithm is not described precisely. If T-003 depends on T-002, and T-002 is `in_progress`, should the pipeline wait or skip? Recommendation: skip and re-queue at end of round.

### T-007 ✅ Good
Worker is thin – good. No issues.

### T-008 ✅ Good
CLI commands are comprehensive. One addition: `agentpipe ticket update <id> --description "..."` would be useful.

### T-009 ✅ Good
README scope is clear.

---

## Summary of issues

| # | Ticket | Issue |
|---|--------|-------|
| I-1 | T-003 | Add `threading.Lock` for concurrent storage writes |
| I-2 | T-004 | Add `TestWriteSkill` to skills list |
| I-3 | T-005 | Handle empty `skills_required` in `execute_ticket()` |
| I-4 | T-006 | Specify dependency wait/skip behaviour explicitly |
| I-5 | T-008 | Add `ticket update` command |

---

## Overall Assessment

Tickets are well-scoped and sequenced. The dependency chain is logical. Issues are minor. **Score: 9/10 – proceed after improvements.**
