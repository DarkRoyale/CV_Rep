"""AgentPipe CLI – manage AI agent pipelines from the command line."""

from __future__ import annotations

import sys

import click

from agentpipe.pipeline import Pipeline
from agentpipe.skills import SKILL_REGISTRY
from agentpipe.storage import Storage
from agentpipe.ticket import Ticket, TicketPriority, TicketStatus

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_STATUS_EMOJI = {
    "todo": "○",
    "in_progress": "⏳",
    "review": "👁",
    "done": "✓",
    "failed": "✗",
    "blocked": "⛔",
}

_PRIORITY_EMOJI = {
    "low": "↓",
    "medium": "→",
    "high": "↑",
    "critical": "!!",
}


def _get_storage() -> Storage:
    storage = Storage()
    if not storage.is_initialised():
        click.echo("❌  Not an agentpipe project. Run `agentpipe init` first.", err=True)
        sys.exit(1)
    return storage


def _fmt_ticket_row(ticket: Ticket) -> str:
    s = _STATUS_EMOJI.get(str(ticket.status.value if hasattr(ticket.status, "value") else ticket.status), "?")
    p = _PRIORITY_EMOJI.get(str(ticket.priority.value if hasattr(ticket.priority, "value") else ticket.priority), "?")
    title = ticket.title[:55] + "…" if len(ticket.title) > 55 else ticket.title
    assigned = ticket.assigned_to or "-"
    return f"  {p} [{ticket.id}] {s} {title:<58} {assigned}"


def _build_default_agents() -> list[dict]:
    return [
        {"name": "planner", "description": "Plans and decomposes goals into tickets", "skills": ["plan", "search"]},
        {"name": "coder", "description": "Writes code and implements features", "skills": ["code_write", "file_ops"]},
        {"name": "reviewer", "description": "Reviews code and gives feedback", "skills": ["code_review", "search"]},
        {"name": "tester", "description": "Writes tests and validates functionality", "skills": ["test_write", "code_review"]},
    ]


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option("0.1.0", prog_name="agentpipe")
def cli() -> None:
    """AgentPipe – run AI agent pipelines with parallel ticket execution."""


# ---------------------------------------------------------------------------
# agentpipe init
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("name", default="my-project")
def init(name: str) -> None:
    """Initialise a new agentpipe project in the current directory."""
    storage = Storage()
    if storage.is_initialised():
        click.echo("ℹ  Project already initialised.")
        return

    storage.init_project(name=name)

    # Register default agents
    for agent_dict in _build_default_agents():
        storage.save_agent(agent_dict)

    click.echo(f"✅  Initialised project '{name}'  →  .agentpipe/")
    click.echo("   Default agents: planner, coder, reviewer, tester")
    click.echo("   Run `agentpipe agent list` to see them.")


# ---------------------------------------------------------------------------
# agentpipe status
# ---------------------------------------------------------------------------

@cli.command()
def status() -> None:
    """Show a summary of all tickets grouped by status."""
    storage = _get_storage()
    tickets = storage.list_tickets()
    config = storage.load_config()

    click.echo(f"\n📋  Project: {config.get('name', 'unknown')}")
    click.echo(f"    Total tickets: {len(tickets)}\n")

    counts: dict[str, int] = {}
    for t in tickets:
        key = str(t.status.value if hasattr(t.status, "value") else t.status)
        counts[key] = counts.get(key, 0) + 1

    for status_key in ("todo", "in_progress", "review", "done", "failed", "blocked"):
        n = counts.get(status_key, 0)
        emoji = _STATUS_EMOJI.get(status_key, "?")
        click.echo(f"  {emoji}  {status_key:<12} {n}")

    click.echo()


# ---------------------------------------------------------------------------
# agentpipe ticket *
# ---------------------------------------------------------------------------

@cli.group()
def ticket() -> None:
    """Manage tickets."""


@ticket.command("add")
@click.argument("title")
@click.option("--description", "-d", default="", help="Ticket description")
@click.option("--priority", "-p",
              type=click.Choice(["low", "medium", "high", "critical"]),
              default="medium")
@click.option("--skills", "-s", default="", help="Comma-separated required skills")
@click.option("--depends-on", default="", help="Comma-separated ticket IDs this depends on")
def ticket_add(title: str, description: str, priority: str, skills: str, depends_on: str) -> None:
    """Add a new ticket."""
    storage = _get_storage()
    t = Ticket(
        title=title,
        description=description,
        priority=TicketPriority(priority),
        skills_required=[s.strip() for s in skills.split(",") if s.strip()],
        depends_on=[d.strip() for d in depends_on.split(",") if d.strip()],
    )
    storage.save_ticket(t)
    click.echo(f"✅  Ticket [{t.id}] created: {title!r}")


@ticket.command("list")
@click.option("--status", "filter_status", default="all",
              help="Filter by status (todo|in_progress|review|done|failed|blocked|all)")
def ticket_list(filter_status: str) -> None:
    """List all tickets."""
    storage = _get_storage()
    tickets = storage.list_tickets()

    if filter_status != "all":
        tickets = [t for t in tickets if str(
            t.status.value if hasattr(t.status, "value") else t.status
        ) == filter_status]

    if not tickets:
        click.echo("  No tickets found.")
        return

    click.echo(f"\n  {'P'} {'ID':^8} {'S'} {'Title':<58} {'Agent'}")
    click.echo("  " + "-" * 80)
    for t in tickets:
        click.echo(_fmt_ticket_row(t))
    click.echo()


@ticket.command("show")
@click.argument("ticket_id")
def ticket_show(ticket_id: str) -> None:
    """Show full details of a ticket."""
    storage = _get_storage()
    t = storage.load_ticket(ticket_id)
    if t is None:
        click.echo(f"❌  Ticket '{ticket_id}' not found.", err=True)
        sys.exit(1)

    click.echo(f"\n  ID:          {t.id}")
    click.echo(f"  Title:       {t.title}")
    click.echo(f"  Description: {t.description or '-'}")
    click.echo(f"  Status:      {t.status.value if hasattr(t.status, 'value') else t.status}")
    click.echo(f"  Priority:    {t.priority.value if hasattr(t.priority, 'value') else t.priority}")
    click.echo(f"  Assigned to: {t.assigned_to or '-'}")
    click.echo(f"  Skills req:  {', '.join(t.skills_required) or '-'}")
    click.echo(f"  Depends on:  {', '.join(t.depends_on) or '-'}")
    click.echo(f"  Retry count: {t.retry_count}")
    click.echo(f"  Created:     {t.created_at}")
    click.echo(f"  Updated:     {t.updated_at}")
    if t.result:
        click.echo(f"\n  Result:\n{t.result}")
    click.echo()


@ticket.command("assign")
@click.argument("ticket_id")
@click.argument("agent_name")
def ticket_assign(ticket_id: str, agent_name: str) -> None:
    """Manually assign a ticket to an agent."""
    storage = _get_storage()
    t = storage.load_ticket(ticket_id)
    if t is None:
        click.echo(f"❌  Ticket '{ticket_id}' not found.", err=True)
        sys.exit(1)
    t.assigned_to = agent_name
    t.touch()
    storage.save_ticket(t)
    click.echo(f"✅  Ticket [{ticket_id}] assigned to '{agent_name}'")


@ticket.command("done")
@click.argument("ticket_id")
def ticket_done(ticket_id: str) -> None:
    """Mark a ticket as done."""
    storage = _get_storage()
    t = storage.load_ticket(ticket_id)
    if t is None:
        click.echo(f"❌  Ticket '{ticket_id}' not found.", err=True)
        sys.exit(1)
    t.set_status(TicketStatus.DONE)
    storage.save_ticket(t)
    click.echo(f"✅  Ticket [{ticket_id}] marked as DONE")


@ticket.command("fail")
@click.argument("ticket_id")
def ticket_fail(ticket_id: str) -> None:
    """Mark a ticket as failed."""
    storage = _get_storage()
    t = storage.load_ticket(ticket_id)
    if t is None:
        click.echo(f"❌  Ticket '{ticket_id}' not found.", err=True)
        sys.exit(1)
    t.set_status(TicketStatus.FAILED)
    storage.save_ticket(t)
    click.echo(f"✅  Ticket [{ticket_id}] marked as FAILED")


@ticket.command("update")
@click.argument("ticket_id")
@click.option("--title", default=None)
@click.option("--description", "-d", default=None)
@click.option("--priority", "-p",
              type=click.Choice(["low", "medium", "high", "critical"]),
              default=None)
@click.option("--skills", "-s", default=None, help="Comma-separated required skills (replaces existing)")
def ticket_update(ticket_id: str, title: str | None, description: str | None,
                  priority: str | None, skills: str | None) -> None:
    """Update ticket fields."""
    storage = _get_storage()
    t = storage.load_ticket(ticket_id)
    if t is None:
        click.echo(f"❌  Ticket '{ticket_id}' not found.", err=True)
        sys.exit(1)

    if title is not None:
        t.title = title
    if description is not None:
        t.description = description
    if priority is not None:
        t.priority = TicketPriority(priority)
    if skills is not None:
        t.skills_required = [s.strip() for s in skills.split(",") if s.strip()]
    t.touch()
    storage.save_ticket(t)
    click.echo(f"✅  Ticket [{ticket_id}] updated")


# ---------------------------------------------------------------------------
# agentpipe agent *
# ---------------------------------------------------------------------------

@cli.group()
def agent() -> None:
    """Manage agents."""


@agent.command("list")
def agent_list() -> None:
    """List all registered agents."""
    storage = _get_storage()
    agents = storage.list_agents()
    if not agents:
        click.echo("  No agents registered. Run `agentpipe init` to create defaults.")
        return
    click.echo(f"\n  {'Name':<16} {'Skills':<40} Description")
    click.echo("  " + "-" * 80)
    for a in agents:
        skills_str = ", ".join(a.get("skills", []))
        desc = a.get("description", "")[:30]
        click.echo(f"  {a['name']:<16} {skills_str:<40} {desc}")
    click.echo()


@agent.command("add")
@click.argument("name")
@click.option("--skills", "-s", required=True, help="Comma-separated skill names")
@click.option("--description", "-d", default="", help="Agent description")
def agent_add(name: str, skills: str, description: str) -> None:
    """Register a new agent."""
    storage = _get_storage()
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    unknown = [s for s in skill_list if s not in SKILL_REGISTRY]
    if unknown:
        click.echo(f"⚠  Unknown skills: {unknown}. Available: {list(SKILL_REGISTRY.keys())}", err=True)

    agent_dict = {"name": name, "description": description, "skills": skill_list}
    storage.save_agent(agent_dict)
    click.echo(f"✅  Agent '{name}' registered with skills: {skill_list}")


@agent.command("skills")
@click.argument("name", default="")
def agent_skills(name: str) -> None:
    """Show skills of a specific agent, or list all available skills."""
    storage = _get_storage()

    if name:
        agent_dict = storage.load_agent(name)
        if agent_dict is None:
            click.echo(f"❌  Agent '{name}' not found.", err=True)
            sys.exit(1)
        click.echo(f"\n  Agent: {name}")
        for s in agent_dict.get("skills", []):
            skill_cls = SKILL_REGISTRY.get(s)
            desc = skill_cls().description if skill_cls else "(unknown)"
            click.echo(f"    • {s:<20} {desc}")
    else:
        click.echo("\n  All available skills:")
        for skill_name, skill_cls in SKILL_REGISTRY.items():
            skill = skill_cls()
            click.echo(f"    • {skill_name:<20} {skill.description}")
    click.echo()


# ---------------------------------------------------------------------------
# agentpipe run
# ---------------------------------------------------------------------------

@cli.command("run")
@click.option("--parallel", is_flag=True, default=False, help="Run tickets in parallel")
@click.option("--agents", "max_workers", default=4, show_default=True,
              help="Number of parallel workers (only with --parallel)")
@click.option("--dry-run", is_flag=True, default=False, help="Print plan without executing")
@click.option("--retry-failed", is_flag=True, default=False, help="Reset failed tickets to TODO and retry")
def run(parallel: bool, max_workers: int, dry_run: bool, retry_failed: bool) -> None:
    """Run the pipeline (execute all TODO tickets)."""
    storage = _get_storage()
    pipeline = Pipeline(storage=storage)
    pipeline.load_agents()

    if not pipeline.agents:
        click.echo("❌  No agents found. Run `agentpipe init` or `agentpipe agent add`.", err=True)
        sys.exit(1)

    pipeline.run(
        parallel=parallel,
        max_workers=max_workers,
        dry_run=dry_run,
        retry_failed=retry_failed,
        log=click.echo,
    )


# ---------------------------------------------------------------------------
# agentpipe plan
# ---------------------------------------------------------------------------

@cli.command("plan")
@click.argument("goal")
@click.option("--max-tickets", default=5, show_default=True, help="Max number of sub-tickets to generate")
@click.option("--priority", "-p",
              type=click.Choice(["low", "medium", "high", "critical"]),
              default="medium")
@click.option("--skills", "-s", default="", help="Skills required for generated tickets")
def plan(goal: str, max_tickets: int, priority: str, skills: str) -> None:
    """Auto-generate tickets from a high-level goal using the PlanSkill."""
    storage = _get_storage()
    from agentpipe.skills.plan import PlanSkill

    planner = PlanSkill()
    result = planner.execute(goal=goal, max_tickets=max_tickets)

    if not result.success:
        click.echo(f"❌  Planning failed: {result.error}", err=True)
        sys.exit(1)

    skill_list = [s.strip() for s in skills.split(",") if s.strip()]

    # Parse ticket titles from output
    lines = str(result.output).split("\n")
    titles = [
        line.lstrip(" 0123456789.").strip()
        for line in lines
        if line.strip() and not line.startswith("[plan]") and not line.startswith("---")
    ]

    click.echo(f"\n[plan] Goal: {goal!r}")
    click.echo(f"[plan] Generating {len(titles)} ticket(s)…\n")

    created = []
    for title in titles[:max_tickets]:
        if not title:
            continue
        t = Ticket(
            title=title,
            description=f"Auto-generated for goal: {goal}",
            priority=TicketPriority(priority),
            skills_required=skill_list,
        )
        storage.save_ticket(t)
        created.append(t)
        click.echo(f"  ✅  [{t.id}] {title}")

    click.echo(f"\n  Created {len(created)} ticket(s). Run `agentpipe run` to execute them.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    cli()


if __name__ == "__main__":
    main()
