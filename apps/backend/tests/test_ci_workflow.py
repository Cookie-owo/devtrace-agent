from __future__ import annotations

import subprocess
from pathlib import Path
from typing import cast

import pytest
from alembic import command
from alembic.config import Config

from super_ai.ci_diagnosis.repository import SQLiteCiDiagnosticRepository
from super_ai.ci_diagnosis.workflow import CiDiagnosisWorkflow, DiagnosisBudget
from super_ai.developer_tools import (
    GitDiffTool,
    GitLogTool,
    ReadFileTool,
    ReadTestLogTool,
    SearchCodeTool,
    WorkspaceGuard,
)
from super_ai.developer_tools.base import ToolResult
from super_ai.memory.database import create_memory_engine, create_memory_session_factory


@pytest.fixture
def migrated_database_url(tmp_path: Path) -> str:
    database_path = tmp_path / "ci-workflow.sqlite3"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{database_path}")
    command.upgrade(config, "head")
    return f"sqlite+aiosqlite:///{database_path}"


def _git(repository: Path, *arguments: str) -> str:
    return subprocess.check_output(["git", "-C", str(repository), *arguments], text=True).strip()


def _golden_repository(root: Path) -> tuple[Path, str]:
    repository = root / "order-service"
    (repository / "src" / "order").mkdir(parents=True)
    (repository / "tests").mkdir()
    (repository / "src" / "order" / "dto.py").write_text(
        "class CreateOrderRequest:\n    user_id: str\n", encoding="utf-8"
    )
    (repository / "tests" / "test_order.py").write_text(
        "def test_create_order():\n    payload = {'user_id': 'u-001'}\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(repository), "init"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repository), "config", "user.email", "test@example.com"], check=True
    )
    subprocess.run(["git", "-C", str(repository), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repository), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "initial dto"],
        check=True,
        capture_output=True,
    )
    (repository / "src" / "order" / "dto.py").write_text(
        "class CreateOrderRequest:\n    uid: str\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(repository), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "update dto"],
        check=True,
        capture_output=True,
    )
    return repository, _git(repository, "rev-parse", "HEAD")


def _workflow(
    repository: SQLiteCiDiagnosticRepository, root: Path, *, budget: DiagnosisBudget | None = None
) -> CiDiagnosisWorkflow:
    guard = WorkspaceGuard([root])
    tools = {
        "read_test_log": ReadTestLogTool(),
        "git_diff": GitDiffTool(guard),
        "git_log": GitLogTool(guard),
        "read_file": ReadFileTool(guard),
        "search_code": SearchCodeTool(guard),
    }
    return CiDiagnosisWorkflow(repository=repository, tools=tools, budget=budget)


class _FailingGitDiff:
    name = "git_diff"

    async def run(self, **arguments: object) -> ToolResult:
        return ToolResult("error", "git diff unavailable", {}, "git_failure", 0.001, False)


@pytest.mark.asyncio
async def test_golden_case_is_confirmed_with_independent_evidence(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        await repository.create_task(
            owner_user_id="user-a",
            task_id="ci-golden",
            repository_path=str(repository_path),
            failure_summary="test_create_order returns 422",
            test_log="""FAILED tests/test_order.py::test_create_order
Expected: 200
Actual: 422
response: {\"loc\": [\"body\", \"uid\"], \"msg\": \"Field required\"}
""",
            test_name="test_create_order",
            commit_sha=commit_sha,
        )
        result = await _workflow(repository, tmp_path).run(
            task_id="ci-golden",
            owner_user_id="user-a",
            tenant_id="tenant-a",
            repository_path=str(repository_path),
            failure_summary="test_create_order returns 422",
            test_log="""FAILED tests/test_order.py::test_create_order
Expected: 200
Actual: 422
response: {\"loc\": [\"body\", \"uid\"], \"msg\": \"Field required\"}
""",
            test_name="test_create_order",
            commit_sha=commit_sha,
        )
        report = result["report"]
        evidence = result["evidence"]
        assert report["confirmed"] is True
        assert "user_id" in report["rootCause"] and "uid" in report["rootCause"]
        assert len(evidence) >= 3
        assert {item["type"] for item in evidence} >= {"test_log", "git_diff"}
        assert {item["id"] for item in evidence} >= set(report["evidenceIds"])
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_negative_case_without_git_or_source_evidence_is_hypothesis(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path = tmp_path / "empty-repository"
    repository_path.mkdir()
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        negative_log = (
            "FAILED tests/test_order.py::test_create_order\nActual: 422\nuid Field required"
        )
        await repository.create_task(
            owner_user_id="user-a",
            task_id="ci-negative",
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log=negative_log,
        )
        result = await _workflow(repository, tmp_path).run(
            task_id="ci-negative",
            owner_user_id="user-a",
            tenant_id=None,
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log=negative_log,
        )
        assert result["report"]["confirmed"] is False
        assert result["report"]["rootCauseType"] == "hypothesis"
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_budget_prevents_repeated_tool_loop(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        await repository.create_task(
            owner_user_id="user-a",
            task_id="ci-budget",
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log="Actual: 422\nuid Field required",
        )
        result = await _workflow(
            repository, tmp_path, budget=DiagnosisBudget(max_steps=2, max_tool_calls=2)
        ).run(
            task_id="ci-budget",
            owner_user_id="user-a",
            tenant_id=None,
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log="Actual: 422\nuid Field required",
            commit_sha=commit_sha,
        )
        assert result["diagnosis_budget"]["toolCallsUsed"] <= 2
        assert result["report"]["confirmed"] is False
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_replanner_adds_missing_evidence_step(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        tools = {
            "read_test_log": ReadTestLogTool(),
            "git_diff": GitDiffTool(WorkspaceGuard([tmp_path])),
            "search_code": SearchCodeTool(WorkspaceGuard([tmp_path])),
        }
        workflow = CiDiagnosisWorkflow(repository=repository, tools=tools)
        state = {
            "task_id": "ci-replan",
            "repository_path": str(repository_path),
            "commit_sha": commit_sha,
            "evidence": [{"type": "test_log"}, {"type": "git_diff"}],
            "plan": [],
            "current_step_index": 0,
            "diagnosis_budget": DiagnosisBudget().initial(),
        }
        replanned = await workflow._replanner(state)  # type: ignore[arg-type]
        assert replanned["should_continue"] is True
        assert replanned["plan"][0]["expectedEvidenceType"] == "code_search"
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_tool_failure_is_normalized_and_not_confirmed(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        await repository.create_task(
            owner_user_id="user-a",
            task_id="ci-tool-failure",
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log="Actual: 422 uid Field required",
        )
        tools = {
            "read_test_log": ReadTestLogTool(),
            "git_diff": _FailingGitDiff(),
            "git_log": GitLogTool(WorkspaceGuard([tmp_path])),
            "read_file": ReadFileTool(WorkspaceGuard([tmp_path])),
            "search_code": SearchCodeTool(WorkspaceGuard([tmp_path])),
        }
        result = await CiDiagnosisWorkflow(repository=repository, tools=tools).run(
            task_id="ci-tool-failure",
            owner_user_id="user-a",
            tenant_id=None,
            repository_path=str(repository_path),
            failure_summary="test failed",
            test_log="Actual: 422 uid Field required",
            commit_sha=commit_sha,
        )
        assert result["report"]["confirmed"] is False
        assert any(
            call["status"] == "error" and call["result"]["error"] == "git_failure"
            for call in result["tool_calls"]
        )
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_golden_case_determinism_five_runs(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        repository = SQLiteCiDiagnosticRepository(create_memory_session_factory(engine))
        workflow = _workflow(repository, tmp_path)
        log = (
            "FAILED tests/test_order.py::test_create_order\nExpected: 200\nActual: 422\n"
            'response: {"loc": ["body", "uid"], "msg": "Field required"}\n'
        )
        outcomes: list[dict[str, object]] = []
        for index in range(5):
            task_id = f"ci-determinism-{index}"
            await repository.create_task(
                owner_user_id="user-a",
                task_id=task_id,
                repository_path=str(repository_path),
                failure_summary="test_create_order returns 422",
                test_log=log,
                commit_sha=commit_sha,
            )
            result = await workflow.run(
                task_id=task_id,
                owner_user_id="user-a",
                tenant_id="tenant-a",
                repository_path=str(repository_path),
                failure_summary="test_create_order returns 422",
                test_log=log,
                commit_sha=commit_sha,
            )
            report = result["report"]
            outcomes.append(
                {
                    "run": index + 1,
                    "confirmed": report["confirmed"],
                    "root_cause": report["rootCause"],
                    "evidence_types": sorted({item["type"] for item in result["evidence"]}),
                    "tool_calls": len(result["tool_calls"]),
                    "steps": len(result["completed_steps"]),
                    "duration": result["trace"]["latency"],
                }
            )
        assert sum(bool(item["confirmed"]) for item in outcomes) >= 4
        for item in outcomes:
            if item["confirmed"]:
                evidence_types = cast(list[str], item["evidence_types"])
                assert "test_log" in evidence_types
                assert "git_diff" in evidence_types
                assert "source_code" in evidence_types or "code_search" in evidence_types
                assert cast(int, item["tool_calls"]) <= 12
                assert cast(int, item["steps"]) <= 8
    finally:
        await engine.dispose()
