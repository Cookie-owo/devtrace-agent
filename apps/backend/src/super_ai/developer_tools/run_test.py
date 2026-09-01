"""Bounded, read-only test execution tool."""

from __future__ import annotations

import asyncio
from pathlib import Path
from time import monotonic
from typing import Any

from .base import ToolResult
from .workspace import WorkspaceGuard, WorkspaceViolation


class SafeTestRunner:
    """Execute only approved test runners without invoking a shell."""

    name = "run_test"
    _allowed = {"pytest", "python", "python.exe", "pytest.exe"}

    def __init__(
        self, guard: WorkspaceGuard, *, timeout_seconds: float = 30.0, max_output: int = 12000
    ) -> None:
        self._guard = guard
        self._timeout = timeout_seconds
        self._max_output = max_output

    async def run(self, **arguments: Any) -> ToolResult:
        started = monotonic()
        try:
            repository = self._guard.resolve_repository(str(arguments["repository_path"]))
            command = str(arguments.get("command", "pytest"))
            test_path = str(arguments.get("test_path", ""))
            if command not in self._allowed or not test_path or Path(test_path).is_absolute():
                return self._error(
                    "invalid_test_command",
                    started,
                    "Only pytest/python with a relative test path is allowed.",
                )
            candidate = (repository / test_path).resolve()
            if not candidate.is_file() or not candidate.is_relative_to(repository):
                return self._error(
                    "workspace_violation", started, "Test path is outside the workspace."
                )
            args = (
                [command, "-m", "pytest", test_path]
                if command.startswith("python")
                else [command, test_path]
            )
            process = await asyncio.create_subprocess_exec(
                *args,
                cwd=str(repository),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                shell=False,
            )
            try:
                output_bytes, _ = await asyncio.wait_for(
                    process.communicate(), timeout=self._timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return self._error("test_timeout", started, "Test execution timed out.")
            output = output_bytes.decode("utf-8", errors="replace")
            truncated = len(output) > self._max_output
            output = output[: self._max_output]
            status = "ok" if process.returncode == 0 else "error"
            return ToolResult(
                status,
                "Test execution completed.",
                {"command": args, "exitCode": process.returncode, "output": output},
                None if status == "ok" else "test_failed",
                monotonic() - started,
                truncated,
            )
        except (KeyError, WorkspaceViolation, OSError) as exc:
            return self._error("test_runner_error", started, str(exc))

    def _error(self, code: str, started: float, summary: str) -> ToolResult:
        return ToolResult("error", summary, {}, code, monotonic() - started, False)
