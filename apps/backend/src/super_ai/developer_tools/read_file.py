"""Read bounded source files inside an approved workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from super_ai.developer_tools._common import guarded_call, trim_text
from super_ai.developer_tools.base import ToolResult
from super_ai.developer_tools.workspace import WorkspaceGuard


class ReadFileTool:
    name = "read_file"

    def __init__(
        self, guard: WorkspaceGuard, *, timeout_seconds: float = 5, max_chars: int = 40_000
    ) -> None:
        self._guard = guard
        self._timeout_seconds = timeout_seconds
        self._max_chars = max_chars

    async def run(
        self,
        *,
        repository_path: str | Path,
        path: str | Path,
        start_line: int = 1,
        end_line: int | None = None,
        **_: Any,
    ) -> ToolResult:
        async def operation() -> dict[str, Any]:
            if start_line < 1 or (end_line is not None and end_line < start_line):
                raise ValueError("Invalid line range.")
            file_path = self._guard.resolve_file(repository_path, path)
            lines = file_path.read_text(encoding="utf-8").splitlines()
            selected = lines[start_line - 1 : end_line]
            content, truncated = trim_text("\n".join(selected), self._max_chars)
            return {
                "path": str(file_path),
                "content": content,
                "startLine": start_line,
                "endLine": min(end_line or len(lines), len(lines)),
                "_truncated": truncated,
            }

        result = await guarded_call(
            operation, timeout_seconds=self._timeout_seconds, success_summary="Source file read."
        )
        truncated = bool(result.data.pop("_truncated", False)) if result.status == "ok" else False
        return ToolResult(
            result.status, result.summary, result.data, result.error, result.duration, truncated
        )
