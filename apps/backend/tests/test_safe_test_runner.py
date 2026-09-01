from __future__ import annotations

from pathlib import Path

import pytest

from super_ai.developer_tools import SafeTestRunner, WorkspaceGuard


@pytest.mark.asyncio
async def test_runner_rejects_shell_and_outside_path(tmp_path: Path) -> None:
    runner = SafeTestRunner(WorkspaceGuard([tmp_path]))
    result = await runner.run(repository_path=str(tmp_path), command="bash", test_path="x.sh")
    assert result.error == "invalid_test_command"
    result = await runner.run(repository_path=str(tmp_path), command="pytest", test_path="../x.py")
    assert result.error == "workspace_violation"


@pytest.mark.asyncio
async def test_runner_timeout_is_normalized(tmp_path: Path) -> None:
    test_file = tmp_path / "test_sleep.py"
    test_file.write_text("import time\ntime.sleep(2)\n", encoding="utf-8")
    runner = SafeTestRunner(WorkspaceGuard([tmp_path]), timeout_seconds=0.01)
    result = await runner.run(
        repository_path=str(tmp_path), command="pytest", test_path=test_file.name
    )
    assert result.error == "test_timeout"


@pytest.mark.asyncio
async def test_runner_reports_pass_and_failure(tmp_path: Path) -> None:
    passed = tmp_path / "test_pass.py"
    passed.write_text("def test_ok():\n    assert 1 == 1\n", encoding="utf-8")
    failed = tmp_path / "test_fail.py"
    failed.write_text("def test_bad():\n    assert 1 == 2\n", encoding="utf-8")
    runner = SafeTestRunner(WorkspaceGuard([tmp_path]))
    ok = await runner.run(repository_path=str(tmp_path), command="pytest", test_path=passed.name)
    bad = await runner.run(repository_path=str(tmp_path), command="pytest", test_path=failed.name)
    assert ok.status == "ok" and ok.data["exitCode"] == 0
    assert bad.status == "error" and bad.error == "test_failed"
