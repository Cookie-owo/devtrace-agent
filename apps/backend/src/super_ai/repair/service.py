"""Bounded patch-apply and verification service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from super_ai.developer_tools import SafeTestRunner, WorkspaceGuard

from .generator import PatchGenerator
from .patching import IsolatedWorkspace, StructuredPatch


@dataclass(frozen=True, slots=True)
class RepairOutcome:
    status: str
    attempts: int
    changed_files: tuple[str, ...]
    patch: StructuredPatch | None
    test_result: dict[str, object] | None
    error: str | None

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "attempts": self.attempts,
            "changedFiles": list(self.changed_files),
            "patch": {
                "allowedPaths": list(self.patch.allowed_paths),
                "operations": [
                    {"path": item.path, "oldText": item.old_text, "newText": item.new_text}
                    for item in self.patch.operations
                ],
            }
            if self.patch
            else None,
            "testResult": self.test_result,
            "error": self.error,
        }


class ControlledRepairService:
    """Apply a generated patch only in a temporary copy and run one bounded test."""

    def __init__(self, workspace_root: str | Path, *, max_attempts: int = 2) -> None:
        self._guard = WorkspaceGuard([workspace_root])
        self._generator = PatchGenerator()
        self._max_attempts = max_attempts

    async def repair_golden_dto(self, repository_path: str | Path) -> RepairOutcome:
        patch = self._generator.generate_dto_test_patch()
        attempts = 0
        with IsolatedWorkspace(repository_path, self._guard) as workspace:
            while attempts < self._max_attempts:
                attempts += 1
                applied = workspace.apply(patch)
                if applied.status != "applied":
                    return RepairOutcome(
                        "patch_rejected",
                        attempts,
                        applied.changed_files,
                        patch,
                        None,
                        applied.error,
                    )
                result = await SafeTestRunner(WorkspaceGuard([workspace.path])).run(
                    repository_path=str(workspace.path),
                    command="pytest",
                    test_path="tests/test_order.py",
                )
                payload = result.as_dict()
                if result.status == "ok":
                    return RepairOutcome(
                        "verified", attempts, applied.changed_files, patch, payload, None
                    )
                if attempts >= self._max_attempts:
                    return RepairOutcome(
                        "verification_failed",
                        attempts,
                        applied.changed_files,
                        patch,
                        payload,
                        result.error,
                    )
        return RepairOutcome(
            "budget_exhausted", attempts, (), patch, None, "repair_budget_exhausted"
        )
