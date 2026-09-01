"""Bounded literal source search inside an approved workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from super_ai.developer_tools._common import guarded_call
from super_ai.developer_tools.base import ToolResult
from super_ai.developer_tools.workspace import WorkspaceGuard


class SearchCodeTool:
    name = "search_code"
    _ignored = {".git", ".venv", "node_modules", "__pycache__", "dist", "build"}

    def __init__(
        self, guard: WorkspaceGuard, *, timeout_seconds: float = 10, max_results: int = 100
    ) -> None:
        self._guard = guard
        self._timeout_seconds = timeout_seconds
        self._max_results = max_results

    async def run(
        self,
        *,
        repository_path: str | Path,
        query: str,
        paths: list[str] | None = None,
        max_results: int = 50,
        **_: Any,
    ) -> ToolResult:
        async def operation() -> dict[str, Any]:
            if not query or len(query) > 500:
                raise ValueError("Search query must contain 1 to 500 characters.")
            if not 1 <= max_results <= self._max_results:
                raise ValueError(f"max_results must be between 1 and {self._max_results}.")
            repository = self._guard.resolve_repository(repository_path)
            candidates = [repository / item for item in (paths or ["."])]
            matches: list[dict[str, Any]] = []
            for candidate in candidates:
                resolved = candidate.resolve()
                if not self._inside(resolved, repository):
                    raise ValueError("Search path is outside the repository workspace.")
                files = [resolved] if resolved.is_file() else resolved.rglob("*")
                for file_path in files:
                    if len(matches) >= max_results:
                        break
                    if not file_path.is_file() or any(
                        part in self._ignored for part in file_path.parts
                    ):
                        continue
                    try:
                        text = file_path.read_text(encoding="utf-8")
                    except (UnicodeDecodeError, OSError):
                        continue
                    for line_number, line in enumerate(text.splitlines(), 1):
                        if query in line:
                            matches.append(
                                {
                                    "path": str(file_path.relative_to(repository)),
                                    "line": line_number,
                                    "text": line[:1000],
                                }
                            )
                            if len(matches) >= max_results:
                                break
            return {
                "query": query,
                "matches": matches,
                "matchCount": len(matches),
                "_truncated": len(matches) >= max_results,
            }

        result = await guarded_call(
            operation,
            timeout_seconds=self._timeout_seconds,
            success_summary="Source search completed.",
        )
        truncated = bool(result.data.pop("_truncated", False)) if result.status == "ok" else False
        return ToolResult(
            result.status, result.summary, result.data, result.error, result.duration, truncated
        )

    @staticmethod
    def _inside(path: Path, repository: Path) -> bool:
        try:
            path.relative_to(repository)
        except ValueError:
            return False
        return True
