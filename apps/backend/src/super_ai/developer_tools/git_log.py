"""Read-only Git log tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from super_ai.developer_tools._common import guarded_call, trim_text
from super_ai.developer_tools._git import git_read
from super_ai.developer_tools.base import ToolResult
from super_ai.developer_tools.workspace import WorkspaceGuard


class GitLogTool:
    name = "git_log"

    def __init__(
        self, guard: WorkspaceGuard, *, timeout_seconds: float = 10, max_chars: int = 20_000
    ) -> None:
        self._guard = guard
        self._timeout_seconds = timeout_seconds
        self._max_chars = max_chars

    async def run(
        self,
        *,
        repository_path: str | Path,
        commit_sha: str | None = None,
        limit: int = 10,
        **_: Any,
    ) -> ToolResult:
        async def operation() -> dict[str, Any]:
            if not 1 <= limit <= 50:
                raise ValueError("Git log limit must be between 1 and 50.")
            repository = self._guard.resolve_repository(repository_path)
            arguments = ["log", f"-{limit}", "--no-decorate", "--format=%H%x09%s"]
            if commit_sha:
                arguments.append(commit_sha)
            content, truncated = trim_text(
                await git_read(repository, arguments, self._timeout_seconds), self._max_chars
            )
            return {"content": content, "commitSha": commit_sha, "_truncated": truncated}

        result = await guarded_call(
            operation, timeout_seconds=self._timeout_seconds + 1, success_summary="Git log read."
        )
        truncated = bool(result.data.pop("_truncated", False)) if result.status == "ok" else False
        return ToolResult(
            result.status, result.summary, result.data, result.error, result.duration, truncated
        )
