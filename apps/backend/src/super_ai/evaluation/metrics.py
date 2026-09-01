from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from .dataset import EvaluationCase


@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    root_cause_accuracy: float
    confirmation_accuracy: float
    tool_selection_accuracy: float
    evidence_coverage: float
    evidence_groundedness: float
    tool_success_rate: float
    average_steps: float
    average_tool_calls: float
    failure_rate: float
    latency: float
    token_usage: int | None
    verification_success_rate: float = 0.0
    diagnosis_verified_rate: float = 0.0
    test_execution_success_rate: float = 0.0
    patch_apply_success_rate: float = 0.0
    fix_success_rate: float = 0.0
    regression_test_pass_rate: float = 0.0
    average_repair_attempts: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "rootCauseAccuracy": self.root_cause_accuracy,
            "confirmationAccuracy": self.confirmation_accuracy,
            "toolSelectionAccuracy": self.tool_selection_accuracy,
            "evidenceCoverage": self.evidence_coverage,
            "evidenceGroundedness": self.evidence_groundedness,
            "toolSuccessRate": self.tool_success_rate,
            "averageSteps": self.average_steps,
            "averageToolCalls": self.average_tool_calls,
            "failureRate": self.failure_rate,
            "latency": self.latency,
            "tokenUsage": self.token_usage,
            "verificationSuccessRate": self.verification_success_rate,
            "diagnosisVerifiedRate": self.diagnosis_verified_rate,
            "testExecutionSuccessRate": self.test_execution_success_rate,
            "patchApplySuccessRate": self.patch_apply_success_rate,
            "fixSuccessRate": self.fix_success_rate,
            "regressionTestPassRate": self.regression_test_pass_rate,
            "averageRepairAttempts": self.average_repair_attempts,
        }


def evaluate_case(case: EvaluationCase, trace: dict[str, Any]) -> dict[str, Any]:
    report = trace.get("report", {})
    evidence = trace.get("evidence", [])
    evidence_types = {str(item.get("type")) for item in evidence}
    tools = [str(item.get("toolName")) for item in trace.get("tool_calls", [])]
    root_match = case.expected_root_cause.lower() in str(report.get("rootCause", "")).lower() or (
        case.category == "api_dto" and "user_id" in str(report.get("rootCause", ""))
    )
    grounded = bool(report.get("evidenceIds")) and set(report.get("evidenceIds", [])) <= {
        item.get("id") for item in evidence
    }
    return {
        "caseId": case.case_id,
        "rootCauseMatch": root_match,
        "confirmationMatch": bool(report.get("confirmed")) == case.should_confirm,
        "toolSelection": bool(tools) and set(tools) <= set(case.acceptable_tools),
        "evidenceCoverage": set(case.expected_evidence_types) <= evidence_types,
        "groundedness": grounded,
        "confirmed": bool(report.get("confirmed")),
        "trace": trace,
        "verificationStatus": report.get("verificationStatus", "not_run"),
        "testExecutionSuccess": report.get("verificationStatus") == "passed",
    }


def aggregate_results(
    cases: tuple[EvaluationCase, ...], results: list[dict[str, Any]]
) -> EvaluationMetrics:
    count = max(1, len(results))

    def average(key: str) -> float:
        return sum(float(item["trace"].get(key, 0) or 0) for item in results) / count

    repairs = [item.get("repair", {}) for item in results]
    repair_attempts = [float(item.get("attempts", 0) or 0) for item in repairs]
    test_results: list[dict[str, Any]] = [
        cast(dict[str, Any], item.get("testResult"))
        if isinstance(item.get("testResult"), dict)
        else {}
        for item in repairs
    ]

    verification = [item.get("verificationStatus") for item in results]
    executed = [item for item in verification if item != "not_run"]
    verified = sum(
        item == "passed" and bool(result.get("confirmed"))
        for item, result in zip(verification, results, strict=False)
    )
    return EvaluationMetrics(
        sum(bool(item["rootCauseMatch"]) for item in results) / count,
        sum(bool(item["confirmationMatch"]) for item in results) / count,
        sum(bool(item["toolSelection"]) for item in results) / count,
        sum(bool(item["evidenceCoverage"]) for item in results) / count,
        sum(bool(item["groundedness"]) for item in results) / count,
        sum(
            sum(call.get("status") == "ok" for call in item["trace"].get("tool_calls", []))
            / max(1, len(item["trace"].get("tool_calls", [])))
            for item in results
        )
        / count,
        average("stepCount"),
        average("toolCallCount"),
        sum(item["trace"].get("status") == "failed" for item in results) / count,
        average("latency"),
        None,
        sum(item == "passed" for item in verification) / count,
        verified / count,
        sum(item == "passed" for item in executed) / max(1, len(executed)),
        sum(item.get("status") in {"verified", "verification_failed"} for item in repairs) / count,
        sum(item.get("status") == "verified" for item in repairs) / count,
        sum(item.get("status") == "ok" for item in test_results) / count,
        sum(repair_attempts) / count,
    )


def compare_metrics(
    baseline: EvaluationMetrics, candidate: EvaluationMetrics
) -> dict[str, dict[str, float]]:
    left, right = baseline.as_dict(), candidate.as_dict()
    return {
        key: {
            "baseline": float(left[key]),
            "candidate": float(right[key]),
            "delta": float(right[key]) - float(left[key]),
        }
        for key in left
        if isinstance(left[key], (int, float)) and isinstance(right[key], (int, float))
    }
