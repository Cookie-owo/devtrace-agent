from __future__ import annotations

from pathlib import Path

import pytest

from super_ai.developer_tools import WorkspaceGuard
from super_ai.developer_tools.workspace import WorkspaceViolation
from super_ai.repair import IsolatedWorkspace, PatchOperation, StructuredPatch


def test_sensitive_files_are_not_readable(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("SECRET=value", encoding="utf-8")
    guard = WorkspaceGuard([tmp_path])
    with pytest.raises(WorkspaceViolation):
        guard.resolve_file(tmp_path, ".env")


def test_patch_allowlist_blocks_other_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "src.py").write_text("x = 1", encoding="utf-8")
    patch = StructuredPatch(
        (PatchOperation("src.py", "x = 1", "x = 2"),),
        ("tests/test_order.py",),
    )
    with IsolatedWorkspace(repo, WorkspaceGuard([tmp_path])) as workspace:
        with pytest.raises(WorkspaceViolation):
            workspace.apply(patch)
