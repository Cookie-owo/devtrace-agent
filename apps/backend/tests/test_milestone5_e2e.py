from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from super_ai.ci_diagnosis.repository import SQLiteCiDiagnosticRepository
from super_ai.ci_diagnosis.workflow import CiDiagnosisWorkflow
from super_ai.developer_tools import (
    GitDiffTool,
    GitLogTool,
    ReadFileTool,
    ReadTestLogTool,
    SearchCodeTool,
    WorkspaceGuard,
)
from super_ai.memory.database import create_memory_engine, create_memory_session_factory
from super_ai.repair import ControlledRepairService


@pytest.fixture
def migrated_database_url(tmp_path: Path) -> str:
    database = tmp_path / "milestone5.sqlite3"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{database}")
    command.upgrade(config, "head")
    return f"sqlite+aiosqlite:///{database}"


def _fixture(root: Path) -> tuple[Path, str]:
    repo = root / "order-service"
    (repo / "src" / "order").mkdir(parents=True)
    (repo / "tests").mkdir()
    (repo / "src" / "order" / "dto.py").write_text(
        "class Request:\n    user_id: str\n", encoding="utf-8"
    )
    (repo / "tests" / "test_order.py").write_text(
        "def test_create_order():\n    payload = {'user_id': 'u-001'}\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(repo), "init"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True
    )
    (repo / "src" / "order" / "dto.py").write_text(
        "class Request:\n    uid: str\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "dto change"], check=True, capture_output=True
    )
    sha = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    return repo, sha


@pytest.mark.asyncio
async def test_golden_path_diagnosis_verification_repair(
    migrated_database_url: str, tmp_path: Path
) -> None:
    repo, sha = _fixture(tmp_path)
    engine = create_memory_engine(migrated_database_url)
    try:
        factory = create_memory_session_factory(engine)
        persistence = SQLiteCiDiagnosticRepository(factory)
        task_id = "milestone5-golden"
        log = (
            "FAILED test_create_order\nActual: 422\n"
            '{"loc": ["body", "uid"], "msg": "Field required"}'
        )
        await persistence.create_task(
            owner_user_id="demo",
            task_id=task_id,
            repository_path=str(repo),
            failure_summary="422",
            test_log=log,
            commit_sha=sha,
        )
        guard = WorkspaceGuard([tmp_path])
        tools = {
            "read_test_log": ReadTestLogTool(),
            "git_diff": GitDiffTool(guard),
            "git_log": GitLogTool(guard),
            "read_file": ReadFileTool(guard),
            "search_code": SearchCodeTool(guard),
        }
        result = await CiDiagnosisWorkflow(repository=persistence, tools=tools).run(
            task_id=task_id,
            owner_user_id="demo",
            tenant_id="tenant",
            repository_path=str(repo),
            failure_summary="422",
            test_log=log,
            commit_sha=sha,
        )
        assert result["report"]["confirmed"] is True
        repair = await ControlledRepairService(tmp_path).repair_golden_dto(repo)
        assert repair.status == "verified"
        assert (repo / "tests" / "test_order.py").read_text(encoding="utf-8").find("user_id") >= 0
    finally:
        await engine.dispose()
