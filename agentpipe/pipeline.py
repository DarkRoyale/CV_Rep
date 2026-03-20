"""Pipeline – orchestrates the ticket queue, agent pool, and execution."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from agentpipe.agent import Agent
from agentpipe.storage import Storage
from agentpipe.ticket import Ticket, TicketStatus
from agentpipe.worker import Worker


class Pipeline:
    """High-level orchestrator.

    Usage::

        pipeline = Pipeline(storage=storage)
        pipeline.load_agents()
        pipeline.run(parallel=True, max_workers=4, dry_run=False)
    """

    def __init__(self, storage: Storage, agents: list[Agent] | None = None) -> None:
        self.storage = storage
        self.agents: list[Agent] = agents or []

    # ------------------------------------------------------------------
    # Agent management
    # ------------------------------------------------------------------

    def load_agents(self) -> None:
        """Load agents from storage (merges with any pre-configured agents)."""
        for agent_dict in self.storage.list_agents():
            if not any(a.name == agent_dict["name"] for a in self.agents):
                self.agents.append(Agent.from_dict(agent_dict))

    def _find_agent_for(self, ticket: Ticket) -> Agent | None:
        """Return the first available agent that satisfies ALL required skills."""
        if not ticket.skills_required:
            return self.agents[0] if self.agents else None
        for agent in self.agents:
            if all(agent.has_skill(s) for s in ticket.skills_required):
                return agent
        # Partial match: agent has at least one required skill
        for agent in self.agents:
            if any(agent.has_skill(s) for s in ticket.skills_required):
                return agent
        return self.agents[0] if self.agents else None

    # ------------------------------------------------------------------
    # Dependency resolution
    # ------------------------------------------------------------------

    def _deps_satisfied(self, ticket: Ticket, tickets_by_id: dict[str, Ticket]) -> str:
        """Return 'ok' | 'wait' | 'block' based on dependency state."""
        for dep_id in ticket.depends_on:
            dep = tickets_by_id.get(dep_id)
            if dep is None:
                continue
            if dep.status == TicketStatus.FAILED:
                return "block"
            if dep.status != TicketStatus.DONE:
                return "wait"
        return "ok"

    # ------------------------------------------------------------------
    # Dry-run
    # ------------------------------------------------------------------

    def dry_run(self, log: Callable[[str], None] = print) -> None:
        """Print what *would* be executed without actually doing it."""
        tickets = [t for t in self.storage.list_tickets() if t.status == TicketStatus.TODO]
        tickets_by_id = {t.id: t for t in self.storage.list_tickets()}
        log(f"[dry-run] {len(tickets)} TODO ticket(s) would be processed:")
        for ticket in tickets:
            agent = self._find_agent_for(ticket)
            dep_state = self._deps_satisfied(ticket, tickets_by_id)
            agent_name = agent.name if agent else "NO AGENT FOUND"
            log(
                f"  [{ticket.id}] {ticket.title!r:40s} "
                f"→ agent={agent_name}  deps={dep_state}  "
                f"skills={ticket.skills_required}"
            )

    # ------------------------------------------------------------------
    # Sequential run
    # ------------------------------------------------------------------

    def run(
        self,
        parallel: bool = False,
        max_workers: int = 4,
        dry_run: bool = False,
        retry_failed: bool = False,
        log: Callable[[str], None] = print,
    ) -> None:
        """Run the pipeline.

        Args:
            parallel: Use ``ThreadPoolExecutor`` when True.
            max_workers: Thread pool size (only used when ``parallel=True``).
            dry_run: If True, print execution plan without running.
            retry_failed: If True, reset FAILED tickets back to TODO first.
            log: Callable used for progress messages.
        """
        if dry_run:
            self.dry_run(log=log)
            return

        if retry_failed:
            self._reset_failed_tickets()

        if parallel:
            self._run_parallel(max_workers=max_workers, log=log)
        else:
            self._run_sequential(log=log)

    # ------------------------------------------------------------------
    # Internal execution
    # ------------------------------------------------------------------

    def _reset_failed_tickets(self) -> None:
        for ticket in self.storage.list_tickets():
            if ticket.status == TicketStatus.FAILED:
                ticket.set_status(TicketStatus.TODO)
                ticket.retry_count = 0
                self.storage.save_ticket(ticket)

    def _run_sequential(self, log: Callable[[str], None] = print) -> None:
        all_tickets = {t.id: t for t in self.storage.list_tickets()}
        queue = [t for t in all_tickets.values() if t.status == TicketStatus.TODO]
        deferred: list[Ticket] = []

        log(f"[pipeline] Sequential run – {len(queue)} TODO ticket(s)")

        while queue:
            ticket = queue.pop(0)
            # Refresh from storage in case another process updated it
            all_tickets[ticket.id] = ticket

            dep_state = self._deps_satisfied(ticket, all_tickets)
            if dep_state == "wait":
                deferred.append(ticket)
                continue
            if dep_state == "block":
                ticket.set_status(TicketStatus.BLOCKED)
                self.storage.save_ticket(ticket)
                log(f"  [BLOCKED] {ticket.id} {ticket.title!r}")
                continue

            agent = self._find_agent_for(ticket)
            if agent is None:
                log(f"  [SKIP] {ticket.id} – no capable agent found")
                continue

            log(f"  [RUN] {ticket.id} {ticket.title!r} → {agent.name}")
            worker = Worker(agent=agent, storage=self.storage)
            result_ticket = worker.run(ticket)
            all_tickets[ticket.id] = result_ticket
            log(f"  [{'DONE' if result_ticket.status == TicketStatus.DONE else result_ticket.status.upper()}] {ticket.id}")

            # Re-queue deferred tickets that may now be unblocked
            queue.extend(deferred)
            deferred = []

        if deferred:
            log(f"[pipeline] {len(deferred)} ticket(s) deferred (unresolved deps)")

    def _run_parallel(self, max_workers: int = 4, log: Callable[[str], None] = print) -> None:
        all_tickets = {t.id: t for t in self.storage.list_tickets()}
        queue = [t for t in all_tickets.values() if t.status == TicketStatus.TODO]
        deferred: list[Ticket] = []

        log(f"[pipeline] Parallel run (max_workers={max_workers}) – {len(queue)} TODO ticket(s)")

        while queue:
            # Partition: ready vs deferred
            ready: list[tuple[Ticket, Agent]] = []
            for ticket in queue:
                dep_state = self._deps_satisfied(ticket, all_tickets)
                if dep_state == "wait":
                    deferred.append(ticket)
                elif dep_state == "block":
                    ticket.set_status(TicketStatus.BLOCKED)
                    self.storage.save_ticket(ticket)
                    log(f"  [BLOCKED] {ticket.id} {ticket.title!r}")
                else:
                    agent = self._find_agent_for(ticket)
                    if agent is None:
                        log(f"  [SKIP] {ticket.id} – no capable agent found")
                    else:
                        ready.append((ticket, agent))

            if not ready:
                # All remaining tickets are deferred – dependency cycle or unresolved
                log(f"[pipeline] {len(deferred)} ticket(s) deferred (unresolved deps or cycle)")
                break

            actual_workers = min(max_workers, len(ready))
            log(f"[pipeline] Submitting {len(ready)} ticket(s) to {actual_workers} worker(s)")

            with ThreadPoolExecutor(max_workers=actual_workers) as executor:
                futures = {
                    executor.submit(Worker(agent, self.storage).run, ticket): ticket
                    for ticket, agent in ready
                }
                for future in as_completed(futures):
                    orig = futures[future]
                    try:
                        result_ticket = future.result()
                        all_tickets[orig.id] = result_ticket
                        log(
                            f"  [{'DONE' if result_ticket.status == TicketStatus.DONE else result_ticket.status.upper()}]"
                            f" {orig.id} {orig.title!r} (by {result_ticket.assigned_to})"
                        )
                    except Exception as exc:  # noqa: BLE001
                        log(f"  [ERROR] {orig.id}: {exc}")

            queue = list(deferred)
            deferred = []
