"""Structured, workspace-isolated patch application."""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from super_ai.developer_tools.workspace import WorkspaceGuard, WorkspaceViolation


@dataclass(frozen=True, slots=True)
class PatchOperation:
    path: str
    old_text: str
    new_text: str


@dataclass(frozen=True, slots=True)
class StructuredPatch:
    operations: tuple[PatchOperation, ...]
    allowed_paths: tuple[str, ...]

    def validate(self) -> None:
        for operation in self.operations:
            candidate = Path(operation.path)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise WorkspaceViolation("Patch path is outside the allowed workspace.")
            if operation.path not in self.allowed_paths:
                raise WorkspaceViolation("Patch path is not in the allowed file list.")
            if not operation.old_text or operation.old_text == operation.new_text:
                raise ValueError("Patch operation must replace non-empty content.")


@dataclass(frozen=True, slots=True)
class PatchApplyResult:
    status: str
    changed_files: tuple[str, ...]
    before_diff: str
    after_diff: str
    error: str | None = None


class IsolatedWorkspace:
    """Copy a repository into a temporary directory and apply structured patches only."""

    def __init__(self, source: str | Path, guard: WorkspaceGuard) -> None:
        self._source = guard.resolve_repository(source)
        self._guard = guard
        self._temporary: Path | None = None

    @property
    def path(self) -> Path:
        if self._temporary is None:
            raise RuntimeError("Workspace has not been opened.")
        return self._temporary

    def __enter__(self) -> IsolatedWorkspace:
        self._temporary = Path(tempfile.mkdtemp(prefix="devpilot-repair-")) / self._source.name
        shutil.copytree(self._source, self._temporary)
        return self

    def __exit__(self, *_: object) -> None:
        if self._temporary is not None:
            shutil.rmtree(self._temporary.parent, ignore_errors=True)
            self._temporary = None

    def apply(self, patch: StructuredPatch) -> PatchApplyResult:
        patch.validate()
        before: dict[str, str] = {}
        changed: list[str] = []
        try:
            for operation in patch.operations:
                target = (self.path / operation.path).resolve()
                target.relative_to(self.path)
                if not target.is_file():
                    raise FileNotFoundError(operation.path)
                content = target.read_text(encoding="utf-8")
                before[operation.path] = content
                if content.count(operation.old_text) != 1:
                    raise ValueError(f"Patch context is not unique: {operation.path}")
                target.write_text(
                    content.replace(operation.old_text, operation.new_text, 1), encoding="utf-8"
                )
                changed.append(operation.path)
            return PatchApplyResult("applied", tuple(changed), "", "", None)
        except (OSError, ValueError, WorkspaceViolation) as exc:
            for path, content in before.items():
                (self.path / path).write_text(content, encoding="utf-8")
            return PatchApplyResult("rejected", tuple(changed), "", "", str(exc))
