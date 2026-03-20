"""Worker – wraps an Agent for concurrent execution via ThreadPoolExecutor."""

from __future__ import annotations

import traceback

from agentpipe.agent import Agent
from agentpipe.storage import Storage
from agentpipe.ticket import Ticket, TicketStatus


class Worker:
    """Executes a single ticket using an agent and persists the result."""

    MAX_RETRIES = 3

    def __init__(self, agent: Agent, storage: Storage) -> None:
        self.agent = agent
        self.storage = storage

    def run(self, ticket: Ticket) -> Ticket:
        """Execute *ticket* and save updated state back to storage.

        Returns the mutated ticket (with updated status / result / retry_count).
        """
        ticket.set_status(TicketStatus.IN_PROGRESS)
        ticket.assigned_to = self.agent.name
        self.storage.save_ticket(ticket)

        try:
            result = self.agent.execute_ticket(ticket)
        except Exception:  # noqa: BLE001
            result_text = traceback.format_exc()
            ticket.result = result_text
            ticket.retry_count += 1
            if ticket.retry_count >= self.MAX_RETRIES:
                ticket.set_status(TicketStatus.FAILED)
            else:
                ticket.set_status(TicketStatus.TODO)
            self.storage.save_ticket(ticket)
            return ticket

        if result.success:
            ticket.result = str(result.output)
            ticket.set_status(TicketStatus.DONE)
        else:
            ticket.result = result.error or "unknown error"
            ticket.retry_count += 1
            if ticket.retry_count >= self.MAX_RETRIES:
                ticket.set_status(TicketStatus.FAILED)
            else:
                ticket.set_status(TicketStatus.TODO)

        self.storage.save_ticket(ticket)
        return ticket
