from __future__ import annotations

from pathlib import Path

import pytest

from super_ai.developer_tools import WorkspaceGuard
from super_ai.developer_tools.workspace import WorkspaceViolation
from super_ai.repair import IsolatedWorkspace, PatchOperation, StructuredPatch


def test_patch_applies_only_in_isolated_workspace(tmp_path: Path) -> None:
    source = tmp_path / "repo"
    source.mkdir()
    target = source / "test.py"
    target.write_text("value = 'old'\n", encoding="utf-8")
    patch = StructuredPatch((PatchOperation("test.py", "'old'", "'new'"),), ("test.py",))
    with IsolatedWorkspace(source, WorkspaceGuard([tmp_path])) as workspace:
        result = workspace.apply(patch)
        assert result.status == "applied"
        assert (workspace.path / "test.py").read_text(encoding="utf-8") == "value = 'new'\n"
    assert target.read_text(encoding="utf-8") == "value = 'old'\n"


def test_patch_conflict_and_traversal_are_rejected(tmp_path: Path) -> None:
    source = tmp_path / "repo"
    source.mkdir()
    (source / "test.py").write_text("value = 'old'\n", encoding="utf-8")
    with IsolatedWorkspace(source, WorkspaceGuard([tmp_path])) as workspace:
        conflict = workspace.apply(
            StructuredPatch((PatchOperation("test.py", "missing", "new"),), ("test.py",))
        )
        assert conflict.status == "rejected"
        with pytest.raises(WorkspaceViolation):
            workspace.apply(
                StructuredPatch((PatchOperation("../secret", "old", "new"),), ("../secret",))
            )
