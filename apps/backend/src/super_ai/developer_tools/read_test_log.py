"""Read a supplied CI test log without touching the filesystem."""

from __future__ import annotations

from typing import Any

from super_ai.developer_tools._common import guarded_call, trim_text
from super_ai.developer_tools.base import ToolResult


class ReadTestLogTool:
    name = "read_test_log"

    def __init__(self, *, timeout_seconds: float = 5, max_chars: int = 40_000) -> None:
        self._timeout_seconds = timeout_seconds
        self._max_chars = max_chars

    async def run(self, *, test_log: str, test_name: str | None = None, **_: Any) -> ToolResult:
        async def operation() -> dict[str, Any]:
            content, truncated = trim_text(test_log, self._max_chars)
            return {
                "content": content,
                "testName": test_name,
                "lineCount": len(content.splitlines()),
                "_truncated": truncated,
            }

        result = await guarded_call(
            operation, timeout_seconds=self._timeout_seconds, success_summary="Test log read."
        )
        if result.status == "ok" and result.data.pop("_truncated", False):
            return ToolResult(
                result.status, result.summary, result.data, result.error, result.duration, True
            )
        return result
