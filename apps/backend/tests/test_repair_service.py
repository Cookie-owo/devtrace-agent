from __future__ import annotations

from pathlib import Path

import pytest

from super_ai.repair import ControlledRepairService


@pytest.mark.asyncio
async def test_golden_repair_is_verified_without_touching_source(tmp_path: Path) -> None:
    repository = tmp_path / "order-service"
    (repository / "tests").mkdir(parents=True)
    (repository / "tests" / "test_order.py").write_text(
        "def test_create_order():\n    payload = {'user_id': 'u-001'}\n",
        encoding="utf-8",
    )
    original = (repository / "tests" / "test_order.py").read_text(encoding="utf-8")
    outcome = await ControlledRepairService(tmp_path).repair_golden_dto(repository)
    assert outcome.status == "verified"
    assert outcome.attempts == 1
    assert outcome.changed_files == ("tests/test_order.py",)
    assert (repository / "tests" / "test_order.py").read_text(encoding="utf-8") == original


@pytest.mark.asyncio
async def test_repair_failure_is_bounded(tmp_path: Path) -> None:
    repository = tmp_path / "order-service"
    (repository / "tests").mkdir(parents=True)
    (repository / "tests" / "test_order.py").write_text(
        "def test_create_order():\n    assert False\n",
        encoding="utf-8",
    )
    outcome = await ControlledRepairService(tmp_path, max_attempts=2).repair_golden_dto(repository)
    assert outcome.status in {"patch_rejected", "verification_failed"}
    assert outcome.attempts <= 2
