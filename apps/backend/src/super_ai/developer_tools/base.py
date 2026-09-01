"""Common tool result and execution boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ToolResult:
    status: str
    summary: str
    data: dict[str, Any]
    error: str | None
    duration: float
    truncated: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "data": self.data,
            "error": self.error,
            "duration": self.duration,
            "truncated": self.truncated,
        }


class DeveloperTool(Protocol):
    name: str

    async def run(self, **arguments: Any) -> ToolResult: ...
