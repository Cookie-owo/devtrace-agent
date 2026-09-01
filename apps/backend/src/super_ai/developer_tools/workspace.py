"""Workspace root and sensitive-file guard."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


class WorkspaceViolation(ValueError):
    """Raised when a developer tool leaves the configured workspace."""


class WorkspaceGuard:
    def __init__(self, roots: Iterable[str | Path]) -> None:
        resolved = tuple(Path(root).expanduser().resolve() for root in roots)
        if not resolved:
            raise ValueError("At least one workspace root is required.")
        self._roots = resolved

    @property
    def roots(self) -> tuple[Path, ...]:
        return self._roots

    def resolve_repository(self, repository_path: str | Path) -> Path:
        path = Path(repository_path).expanduser().resolve()
        if not path.is_dir() or not self._inside(path, exact_root_allowed=True):
            raise WorkspaceViolation("Repository path is outside the configured workspace roots.")
        return path

    def resolve_file(self, repository_path: str | Path, relative_path: str | Path) -> Path:
        repository = self.resolve_repository(repository_path)
        candidate = (repository / Path(relative_path)).resolve()
        if not self._inside(candidate, exact_root_allowed=False) or not candidate.is_file():
            raise WorkspaceViolation(
                "File path is outside the repository workspace or unavailable."
            )
        if candidate.name.lower() in {".env", ".env.local", "project.json", "user.project.json"}:
            raise WorkspaceViolation("Sensitive configuration files cannot be read.")
        return candidate

    def _inside(self, path: Path, *, exact_root_allowed: bool) -> bool:
        for root in self._roots:
            try:
                path.relative_to(root)
            except ValueError:
                continue
            if exact_root_allowed or path != root:
                return True
        return False
