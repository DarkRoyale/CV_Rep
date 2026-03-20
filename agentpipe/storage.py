"""Thread-safe JSON file storage for tickets, agents, and project config."""

from __future__ import annotations

import json
import threading
from pathlib import Path

from agentpipe.ticket import Ticket

_AGENTPIPE_DIR = ".agentpipe"


class Storage:
    """Persist tickets and agents as JSON files inside `.agentpipe/`."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = Path(root) if root else Path.cwd() / _AGENTPIPE_DIR
        self._tickets_dir = self._root / "tickets"
        self._agents_dir = self._root / "agents"
        self._config_file = self._root / "config.json"
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Project initialisation
    # ------------------------------------------------------------------

    def init_project(self, name: str = "my-project") -> None:
        """Create the `.agentpipe/` directory structure."""
        self._tickets_dir.mkdir(parents=True, exist_ok=True)
        self._agents_dir.mkdir(parents=True, exist_ok=True)
        if not self._config_file.exists():
            self.save_config({"name": name, "version": "0.1.0"})

    def is_initialised(self) -> bool:
        return self._root.exists() and self._config_file.exists()

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------

    def load_config(self) -> dict:
        with self._lock:
            if not self._config_file.exists():
                return {}
            return json.loads(self._config_file.read_text(encoding="utf-8"))

    def save_config(self, config: dict) -> None:
        with self._lock:
            self._config_file.write_text(
                json.dumps(config, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    # ------------------------------------------------------------------
    # Tickets
    # ------------------------------------------------------------------

    def save_ticket(self, ticket: Ticket) -> None:
        with self._lock:
            path = self._tickets_dir / f"{ticket.id}.json"
            path.write_text(
                json.dumps(ticket.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def load_ticket(self, ticket_id: str) -> Ticket | None:
        path = self._tickets_dir / f"{ticket_id}.json"
        if not path.exists():
            return None
        return Ticket.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_tickets(self) -> list[Ticket]:
        if not self._tickets_dir.exists():
            return []
        tickets = []
        for path in sorted(self._tickets_dir.glob("*.json")):
            tickets.append(Ticket.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return tickets

    def delete_ticket(self, ticket_id: str) -> bool:
        path = self._tickets_dir / f"{ticket_id}.json"
        if path.exists():
            with self._lock:
                path.unlink()
            return True
        return False

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    def save_agent(self, agent_dict: dict) -> None:
        with self._lock:
            path = self._agents_dir / f"{agent_dict['name']}.json"
            path.write_text(
                json.dumps(agent_dict, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def load_agent(self, name: str) -> dict | None:
        path = self._agents_dir / f"{name}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_agents(self) -> list[dict]:
        if not self._agents_dir.exists():
            return []
        agents = []
        for path in sorted(self._agents_dir.glob("*.json")):
            agents.append(json.loads(path.read_text(encoding="utf-8")))
        return agents
