"""Tests for the CLI using click.testing.CliRunner."""

import pytest
from click.testing import CliRunner

from agentpipe.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def proj(runner, tmp_path):
    """Initialise a project in an isolated temp directory."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["init", "test-project"])
        assert result.exit_code == 0, result.output
        yield runner


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

def test_init_creates_project(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["init", "my-project"])
        assert result.exit_code == 0
        assert "Initialised" in result.output


def test_init_idempotent(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "already initialised" in result.output


def test_no_project_fails(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["status"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def test_status(proj):
    result = proj.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "todo" in result.output


# ---------------------------------------------------------------------------
# ticket
# ---------------------------------------------------------------------------

def test_ticket_add(proj):
    result = proj.invoke(cli, ["ticket", "add", "My ticket"])
    assert result.exit_code == 0
    assert "created" in result.output


def test_ticket_list(proj):
    proj.invoke(cli, ["ticket", "add", "Task A"])
    proj.invoke(cli, ["ticket", "add", "Task B"])
    result = proj.invoke(cli, ["ticket", "list"])
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" in result.output


def test_ticket_show(proj):
    add_result = proj.invoke(cli, ["ticket", "add", "Show me"])
    ticket_id = add_result.output.split("[")[1].split("]")[0]
    result = proj.invoke(cli, ["ticket", "show", ticket_id])
    assert result.exit_code == 0
    assert "Show me" in result.output


def test_ticket_done(proj):
    add_result = proj.invoke(cli, ["ticket", "add", "Finish this"])
    ticket_id = add_result.output.split("[")[1].split("]")[0]
    result = proj.invoke(cli, ["ticket", "done", ticket_id])
    assert result.exit_code == 0
    assert "DONE" in result.output


def test_ticket_fail(proj):
    add_result = proj.invoke(cli, ["ticket", "add", "This fails"])
    ticket_id = add_result.output.split("[")[1].split("]")[0]
    result = proj.invoke(cli, ["ticket", "fail", ticket_id])
    assert result.exit_code == 0
    assert "FAILED" in result.output


def test_ticket_update(proj):
    add_result = proj.invoke(cli, ["ticket", "add", "Old title"])
    ticket_id = add_result.output.split("[")[1].split("]")[0]
    result = proj.invoke(cli, ["ticket", "update", ticket_id, "--title", "New title"])
    assert result.exit_code == 0
    assert "updated" in result.output


def test_ticket_assign(proj):
    add_result = proj.invoke(cli, ["ticket", "add", "Assign this"])
    ticket_id = add_result.output.split("[")[1].split("]")[0]
    result = proj.invoke(cli, ["ticket", "assign", ticket_id, "coder"])
    assert result.exit_code == 0
    assert "assigned" in result.output


def test_ticket_show_not_found(proj):
    result = proj.invoke(cli, ["ticket", "show", "notexist"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# agent
# ---------------------------------------------------------------------------

def test_agent_list(proj):
    result = proj.invoke(cli, ["agent", "list"])
    assert result.exit_code == 0
    assert "coder" in result.output


def test_agent_add(proj):
    result = proj.invoke(cli, ["agent", "add", "mybot", "--skills", "code_write,search"])
    assert result.exit_code == 0
    assert "registered" in result.output


def test_agent_skills(proj):
    result = proj.invoke(cli, ["agent", "skills"])
    assert result.exit_code == 0
    assert "code_write" in result.output


def test_agent_skills_for_specific_agent(proj):
    result = proj.invoke(cli, ["agent", "skills", "coder"])
    assert result.exit_code == 0
    assert "code_write" in result.output


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

def test_run_sequential(proj):
    proj.invoke(cli, ["ticket", "add", "Task 1", "--skills", "code_write"])
    result = proj.invoke(cli, ["run"])
    assert result.exit_code == 0
    assert "DONE" in result.output


def test_run_parallel(proj):
    proj.invoke(cli, ["ticket", "add", "Task A", "--skills", "code_write"])
    proj.invoke(cli, ["ticket", "add", "Task B", "--skills", "code_write"])
    result = proj.invoke(cli, ["run", "--parallel", "--agents", "2"])
    assert result.exit_code == 0
    assert "DONE" in result.output


def test_run_dry_run(proj):
    proj.invoke(cli, ["ticket", "add", "No execute", "--skills", "code_write"])
    result = proj.invoke(cli, ["run", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


# ---------------------------------------------------------------------------
# plan
# ---------------------------------------------------------------------------

def test_plan_generates_tickets(proj):
    result = proj.invoke(cli, ["plan", "Build a REST API"])
    assert result.exit_code == 0
    assert "Created" in result.output

    list_result = proj.invoke(cli, ["ticket", "list"])
    assert "REST API" in list_result.output
