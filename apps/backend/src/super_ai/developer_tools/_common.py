"""Internal helpers shared by read-only developer tools."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from time import monotonic
from typing import Any

from super_ai.developer_tools.base import ToolResult


async def guarded_call(
    operation: Callable[[], Awaitable[dict[str, Any]]],
    *,
    timeout_seconds: float,
    success_summary: str,
    truncated: bool = False,
) -> ToolResult:
    started = monotonic()
    try:
        data = await asyncio.wait_for(operation(), timeout=timeout_seconds)
    except asyncio.TimeoutError:
        return ToolResult(
            "error", "Developer tool timed out.", {}, "timeout", monotonic() - started, False
        )
    except Exception as exc:
        return ToolResult(
            "error",
            "Developer tool failed.",
            {},
            _normalize_error(exc),
            monotonic() - started,
            False,
        )
    return ToolResult("ok", success_summary, data, None, monotonic() - started, truncated)


def _normalize_error(error: Exception) -> str:
    return (str(error).strip() or error.__class__.__name__)[:500]


def trim_text(value: str, max_chars: int) -> tuple[str, bool]:
    if len(value) <= max_chars:
        return value, False
    return value[:max_chars], True
