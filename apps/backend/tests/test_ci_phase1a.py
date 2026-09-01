from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from super_ai.ci_diagnosis.repository import SQLiteCiDiagnosticRepository
from super_ai.developer_tools import (
    GitDiffTool,
    GitLogTool,
    ReadFileTool,
    ReadTestLogTool,
    SearchCodeTool,
    WorkspaceGuard,
)
from super_ai.memory.database import create_memory_engine, create_memory_session_factory


@pytest.fixture
def migrated_database_url(tmp_path: Path) -> str:
    database_path = tmp_path / "ci-diagnosis.sqlite3"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{database_path}")
    command.upgrade(config, "head")
    return f"sqlite+aiosqlite:///{database_path}"


@pytest.mark.asyncio
async def test_ci_repository_is_owner_scoped(migrated_database_url: str) -> None:
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        await repository.create_task(
            owner_user_id="user-a",
            task_id="ci-a",
            repository_path="/workspace/a",
            failure_summary="failed",
            test_log="log",
        )
        await repository.create_step(
            owner_user_id="user-a",
            step_id="step-a",
            task_id="ci-a",
            sequence=1,
            node="planner",
            action="inspect",
            status="completed",
        )
        evidence = await repository.create_evidence(
            owner_user_id="user-a",
            evidence_id="evidence-a",
            task_id="ci-a",
            type="test_log",
            source="test_log",
            summary="failure",
            content="uid Field required",
            step_id="step-a",
        )
        await repository.create_tool_call(
            owner_user_id="user-a",
            call_id="call-a",
            task_id="ci-a",
            tool_name="read_test_log",
            status="ok",
            result={"summary": evidence.summary},
            duration_ms=2,
        )
        assert await repository.get_task(owner_user_id="user-b", task_id="ci-a") is None
        assert await repository.list_evidence(owner_user_id="user-b", task_id="ci-a") == []
        assert (await repository.list_evidence(owner_user_id="user-a", task_id="ci-a"))[
            0
        ].type == "test_log"
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_read_only_tools_return_structured_results(tmp_path: Path) -> None:
    repository = tmp_path / "repo"
    repository.mkdir()
    source = repository / "dto.py"
    source.write_text("class OrderDto:\n    uid: str\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "init"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repository), "config", "user.email", "test@example.com"], check=True
    )
    subprocess.run(["git", "-C", str(repository), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repository), "add", "dto.py"], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "rename field"],
        check=True,
        capture_output=True,
    )
    source.write_text("class OrderDto:\n    uid: str\n    status: str\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "add", "dto.py"], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "add status"],
        check=True,
        capture_output=True,
    )

    guard = WorkspaceGuard([tmp_path])
    results = [
        await ReadTestLogTool().run(
            test_log="422 uid Field required", test_name="test_create_order"
        ),
        await ReadFileTool(guard).run(repository_path=repository, path="dto.py"),
        await SearchCodeTool(guard).run(repository_path=repository, query="uid"),
        await GitLogTool(guard).run(repository_path=repository),
    ]
    results.append(
        await GitDiffTool(guard).run(
            repository_path=repository,
            commit_sha=subprocess.check_output(
                ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True
            ).strip(),
        )
    )
    for result in results:
        assert result.status == "ok"
        assert isinstance(result.summary, str)
        assert isinstance(result.data, dict)
        assert result.error is None
        assert result.duration >= 0
        assert isinstance(result.truncated, bool)


@pytest.mark.asyncio
async def test_git_diff_and_workspace_guard_reject_escape(tmp_path: Path) -> None:
    repository = tmp_path / "repo"
    repository.mkdir()
    (repository / "file.txt").write_text("content", encoding="utf-8")
    guard = WorkspaceGuard([tmp_path])
    result = await ReadFileTool(guard).run(repository_path=repository, path="../outside.txt")
    assert result.status == "error"
    assert result.error
    outside = await ReadFileTool(guard).run(repository_path=tmp_path / "..", path="outside.txt")
    assert outside.status == "error"


@pytest.mark.asyncio
async def test_read_test_log_truncates_without_exposing_root_cause() -> None:
    result = await ReadTestLogTool(max_chars=5).run(test_log="uid Field required")
    assert result.status == "ok"
    assert result.truncated is True
    assert result.data["content"] == "uid F"
