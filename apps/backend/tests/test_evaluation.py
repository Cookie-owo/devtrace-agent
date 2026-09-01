from __future__ import annotations

from typing import Any

import pytest

from super_ai.evaluation import (
    EvaluationCase,
    EvaluationRunner,
    compare_metrics,
    load_builtin_dataset,
)
from super_ai.evaluation.metrics import evaluate_case


def test_builtin_dataset_has_twenty_cases_and_negative_cases() -> None:
    dataset = load_builtin_dataset()
    assert len(dataset) >= 20
    assert len({case.category for case in dataset}) >= 6
    assert any(not case.should_confirm for case in dataset)


def test_metrics_are_deterministic_and_grounded() -> None:
    case = load_builtin_dataset()[0]
    trace = {
        "report": {
            "confirmed": True,
            "rootCause": "DTO field contract mismatch",
            "evidenceIds": ["e1"],
        },
        "evidence": [{"id": "e1", "type": "test_log"}],
        "tool_calls": [{"toolName": "read_test_log", "status": "ok"}],
    }
    result = evaluate_case(case, trace)
    assert result["rootCauseMatch"] is True
    assert result["groundedness"] is True


@pytest.mark.asyncio
async def test_batch_runner_and_comparison() -> None:
    async def executor(case: EvaluationCase) -> dict[str, Any]:
        return {
            "report": {
                "confirmed": case.should_confirm,
                "rootCause": case.expected_root_cause,
                "evidenceIds": ["e1"],
            },
            "evidence": [{"id": "e1", "type": case.expected_evidence_types[0]}],
            "tool_calls": [],
            "status": "completed",
            "latency": 0.1,
            "stepCount": 1,
            "toolCallCount": 0,
        }

    run = await EvaluationRunner(executor).run()
    assert len(run.case_results) == 20
    assert 0 <= run.metrics.confirmation_accuracy <= 1
    comparison = compare_metrics(run.metrics, run.metrics)
    assert all(value["delta"] == 0 for value in comparison.values())
