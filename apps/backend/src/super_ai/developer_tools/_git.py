"""Safe subprocess boundary for fixed read-only Git commands."""

from __future__ import annotations

import asyncio
import subprocess
from collections.abc import Sequence
from pathlib import Path


async def git_read(repository: Path, arguments: Sequence[str], timeout_seconds: float) -> str:
    def run() -> str:
        completed = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "Git read operation failed.")
        return completed.stdout

    return await asyncio.to_thread(run)
