from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureCategory = Literal[
    "api_dto",
    "assertion",
    "test_data",
    "dependency",
    "configuration",
    "environment",
    "database",
    "build",
    "timeout",
    "insufficient_evidence",
]
ExecutionMode = Literal["real_fixture", "controlled_fixture", "fault_injection"]


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    case_id: str
    category: FailureCategory
    repository_fixture: str
    failure_summary: str
    test_log: str
    expected_root_cause: str
    expected_root_cause_type: Literal["confirmed", "hypothesis"]
    expected_evidence_types: tuple[str, ...]
    acceptable_tools: tuple[str, ...]
    should_confirm: bool
    execution_mode: ExecutionMode = "controlled_fixture"


_CATEGORIES: tuple[FailureCategory, ...] = (
    "api_dto",
    "assertion",
    "test_data",
    "dependency",
    "configuration",
    "environment",
    "database",
    "build",
    "timeout",
    "insufficient_evidence",
)


def load_builtin_dataset() -> tuple[EvaluationCase, ...]:
    cases: list[EvaluationCase] = []
    for index in range(20):
        category = _CATEGORIES[index % len(_CATEGORIES)]
        # 当前内置 Fixture 只有 DTO 契约变更具备完整 Git/源码证据；其余类别
        # 暂以“证据不足”运行，避免把共享仓库中的模板日志误标为已确认根因。
        confirmed = category == "api_dto"
        execution_mode: ExecutionMode = (
            "real_fixture" if category == "api_dto" else "controlled_fixture"
        )
        cases.append(
            EvaluationCase(
                case_id=f"golden-{index + 1:02d}",
                category=category,
                repository_fixture="golden-order-service",
                failure_summary=f"{category} failure case {index + 1}",
                test_log="FAILED test_case\nActual: 422\nField required",
                expected_root_cause="DTO field contract mismatch"
                if category == "api_dto"
                else "证据不足，无法确认根因",
                expected_root_cause_type="confirmed" if confirmed else "hypothesis",
                expected_evidence_types=("test_log", "git_diff", "source_code")
                if confirmed
                else ("test_log",),
                acceptable_tools=(
                    "read_test_log",
                    "git_diff",
                    "search_code",
                    "read_file",
                    "git_log",
                ),
                should_confirm=confirmed,
                execution_mode=execution_mode,
            )
        )
    return tuple(cases)
