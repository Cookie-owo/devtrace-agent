from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .dataset import EvaluationCase, load_builtin_dataset
from .metrics import EvaluationMetrics, aggregate_results, evaluate_case

TraceExecutor = Callable[[EvaluationCase], Awaitable[dict[str, Any]]]


@dataclass(frozen=True, slots=True)
class EvaluationRun:
    run_id: str
    dataset_version: str
    started_at: datetime
    completed_at: datetime
    case_results: tuple[dict[str, Any], ...]
    metrics: EvaluationMetrics


class EvaluationRunner:
    def __init__(
        self, executor: TraceExecutor, dataset: tuple[EvaluationCase, ...] | None = None
    ) -> None:
        self._executor = executor
        self._dataset = dataset or load_builtin_dataset()

    async def run(self) -> EvaluationRun:
        started = datetime.now(timezone.utc)
        results = [evaluate_case(case, await self._executor(case)) for case in self._dataset]
        completed = datetime.now(timezone.utc)
        return EvaluationRun(
            f"eval_{uuid4().hex}",
            "builtin-v1",
            started,
            completed,
            tuple(results),
            aggregate_results(self._dataset, results),
        )
