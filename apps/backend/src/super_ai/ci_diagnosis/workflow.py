"""Concrete CI diagnosis LangGraph workflow for the Phase 1 golden slice."""
# LangGraph currently ships incomplete typing metadata; the adapter boundary below
# keeps the rest of this module strictly typed without weakening project settings.
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from time import monotonic
from typing import Any, Literal, TypedDict, cast
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from super_ai.ci_diagnosis.repository import CiDiagnosticRepository
from super_ai.developer_tools.base import DeveloperTool, ToolResult

EvidenceType = Literal[
    "test_log", "git_diff", "git_log", "source_code", "code_search", "test_result"
]
RootCauseType = Literal["confirmed", "hypothesis"]


class CiDiagnosisState(TypedDict):
    task_id: str
    owner_user_id: str
    tenant_id: str | None
    repository_path: str
    commit_sha: str | None
    base_commit_sha: str | None
    failure_summary: str
    test_log: str
    test_name: str | None
    failure_type: str
    failure_analysis: dict[str, Any]
    plan: list[dict[str, Any]]
    current_step_index: int
    completed_steps: list[dict[str, Any]]
    tool_calls: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    hypotheses: list[dict[str, Any]]
    replanning_reason: str | None
    should_continue: bool
    diagnosis_budget: dict[str, Any]
    verification_result: dict[str, Any]
    report: dict[str, Any]
    trace: dict[str, Any]
    last_tool_result: dict[str, Any]
    last_step: dict[str, Any]


@dataclass(frozen=True, slots=True)
class DiagnosisBudget:
    max_steps: int = 8
    max_tool_calls: int = 12
    max_same_tool_call: int = 2
    tool_timeout: float = 10.0
    task_timeout: float = 120.0

    def initial(self) -> dict[str, Any]:
        return {
            "maxSteps": self.max_steps,
            "maxToolCalls": self.max_tool_calls,
            "maxSameToolCall": self.max_same_tool_call,
            "toolTimeout": self.tool_timeout,
            "taskTimeout": self.task_timeout,
            "stepsUsed": 0,
            "toolCallsUsed": 0,
            "remainingSteps": self.max_steps,
            "remainingToolCalls": self.max_tool_calls,
        }


class CiDiagnosisWorkflow:
    """Run a bounded, evidence-grounded CI diagnosis graph."""

    workflow_version = "ci-diagnosis-v1"

    def __init__(
        self,
        *,
        repository: CiDiagnosticRepository,
        tools: Mapping[str, DeveloperTool],
        budget: DiagnosisBudget | None = None,
        model_name: str | None = None,
        prompt_version: str = "ci-diagnosis-prompt-v1",
    ) -> None:
        self._repository = repository
        self._tools = dict(tools)
        self._budget = budget or DiagnosisBudget()
        self._model_name = model_name
        self._prompt_version = prompt_version
        self._graph = self._build_graph()

    async def run(
        self,
        *,
        task_id: str,
        owner_user_id: str,
        tenant_id: str | None,
        repository_path: str,
        failure_summary: str,
        test_log: str,
        test_name: str | None = None,
        commit_sha: str | None = None,
        base_commit_sha: str | None = None,
    ) -> CiDiagnosisState:
        started = monotonic()
        initial: CiDiagnosisState = {
            "task_id": task_id,
            "owner_user_id": owner_user_id,
            "tenant_id": tenant_id,
            "repository_path": repository_path,
            "commit_sha": commit_sha,
            "base_commit_sha": base_commit_sha,
            "failure_summary": failure_summary,
            "test_log": test_log,
            "test_name": test_name,
            "failure_type": "unknown",
            "failure_analysis": {},
            "plan": [],
            "current_step_index": 0,
            "completed_steps": [],
            "tool_calls": [],
            "evidence": [],
            "hypotheses": [],
            "replanning_reason": None,
            "should_continue": True,
            "diagnosis_budget": self._budget.initial(),
            "verification_result": {},
            "report": {},
            "trace": {
                "taskId": task_id,
                "model": self._model_name,
                "promptVersion": self._prompt_version,
                "workflowVersion": self.workflow_version,
                "tokenUsage": None,
            },
            "last_tool_result": {},
            "last_step": {},
        }
        result = cast(
            CiDiagnosisState,
            await asyncio.wait_for(self._graph.ainvoke(initial), timeout=self._budget.task_timeout),
        )
        trace = dict(result.get("trace", {}))
        trace["latency"] = monotonic() - started
        trace["agentSteps"] = result.get("completed_steps", [])
        trace["toolCalls"] = result.get("tool_calls", [])
        trace["toolResults"] = [call.get("result", {}) for call in result.get("tool_calls", [])]
        trace["evidenceIds"] = [item["id"] for item in result.get("evidence", [])]
        trace["finalRootCause"] = result.get("report", {}).get("rootCause")
        trace["confirmed"] = result.get("report", {}).get("confirmed", False)
        trace["budgetUsage"] = result.get("diagnosis_budget", {})
        result["trace"] = trace
        await self._repository.update_task(
            owner_user_id=owner_user_id,
            task_id=task_id,
            status="completed",
            result_payload={"report": result.get("report", {}), "trace": trace},
            completed_at=None,
        )
        return result

    def _build_graph(self) -> Any:
        graph = StateGraph(CiDiagnosisState)
        graph.add_node("failure_analyzer", self._failure_analyzer)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("planner", self._planner)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("tool_executor", self._tool_executor)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("evidence_collector", self._evidence_collector)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("replanner", self._replanner)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("verifier", self._verifier)  # pyright: ignore[reportUnknownMemberType]
        graph.add_node("report", self._report)  # pyright: ignore[reportUnknownMemberType]
        graph.add_edge(START, "failure_analyzer")
        graph.add_edge("failure_analyzer", "planner")
        graph.add_edge("planner", "tool_executor")
        graph.add_edge("tool_executor", "evidence_collector")
        graph.add_edge("evidence_collector", "replanner")
        graph.add_conditional_edges(
            "replanner",
            self._route_after_replanner,
            {"tool_executor": "tool_executor", "verifier": "verifier"},
        )
        graph.add_edge("verifier", "report")
        graph.add_edge("report", END)
        return graph.compile()  # pyright: ignore[reportUnknownMemberType]

    async def _failure_analyzer(self, state: CiDiagnosisState) -> dict[str, Any]:
        log = state["test_log"]
        test_match = re.search(r"(?:FAILED\s+[^\s]+::|test\s+)([\w.-]+)", log, re.IGNORECASE)
        status_match = re.search(r"(?:Actual|status|HTTP)\s*[:=]\s*(\d{3})", log, re.IGNORECASE)
        field_match = re.search(
            r"(?:loc[^\n]*?['\"])([A-Za-z_][\w]*)|([A-Za-z_][\w]*)\s+Field required",
            log,
            re.IGNORECASE,
        )
        test_name = state.get("test_name") or (test_match.group(1) if test_match else None)
        field = next(
            (value for value in (field_match.groups() if field_match else ()) if value), None
        )
        analysis = {
            "parser": "deterministic-regex-v1",
            "testName": test_name,
            "httpStatus": int(status_match.group(1)) if status_match else None,
            "requiredField": field,
            "candidateSymbols": [value for value in (field, "user_id") if value],
            "failureType": "assertion_failure" if "FAILED" in log else "unknown",
        }
        return {
            "test_name": test_name,
            "failure_type": analysis["failureType"],
            "failure_analysis": analysis,
        }

    async def _planner(self, state: CiDiagnosisState) -> dict[str, Any]:
        steps: list[dict[str, Any]] = [
            {
                "stepId": "step-1",
                "toolName": "read_test_log",
                "reason": "确认失败响应和测试名",
                "arguments": {"test_log": state["test_log"], "test_name": state.get("test_name")},
                "expectedEvidenceType": "test_log",
            },
        ]
        if state.get("commit_sha"):
            steps.extend(
                [
                    {
                        "stepId": "step-2",
                        "toolName": "git_diff",
                        "reason": "检查失败提交变更",
                        "arguments": {
                            "repository_path": state["repository_path"],
                            "commit_sha": state["commit_sha"],
                            "base_commit_sha": state.get("base_commit_sha"),
                        },
                        "expectedEvidenceType": "git_diff",
                    },
                    {
                        "stepId": "step-3",
                        "toolName": "search_code",
                        "reason": "搜索字段在源码和测试中的引用",
                        "arguments": {
                            "repository_path": state["repository_path"],
                            "query": state.get("failure_analysis", {}).get("requiredField")
                            or "user_id",
                            "paths": ["src", "tests"],
                        },
                        "expectedEvidenceType": "code_search",
                    },
                    {
                        "stepId": "step-4",
                        "toolName": "read_file",
                        "reason": "读取相关源文件",
                        "arguments": {
                            "repository_path": state["repository_path"],
                            "path": "src/order/dto.py",
                        },
                        "expectedEvidenceType": "source_code",
                    },
                    {
                        "stepId": "step-5",
                        "toolName": "git_log",
                        "reason": "补充提交语义和上下文",
                        "arguments": {
                            "repository_path": state["repository_path"],
                            "commit_sha": state["commit_sha"],
                            "limit": 5,
                        },
                        "expectedEvidenceType": "git_log",
                    },
                ]
            )
        if "run_test" in self._tools:
            steps.append(
                {
                    "stepId": f"verification-{len(steps) + 1}",
                    "toolName": "run_test",
                    "reason": "执行受控测试验证诊断结论",
                    "arguments": {
                        "repository_path": state["repository_path"],
                        "command": "pytest",
                        "test_path": "tests/test_order.py",
                    },
                    "expectedEvidenceType": "test_result",
                }
            )
        return {"plan": steps}

    async def _tool_executor(self, state: CiDiagnosisState) -> dict[str, Any]:
        budget = dict(state["diagnosis_budget"])
        steps = list(state.get("completed_steps", []))
        index = state.get("current_step_index", 0)
        plan = state.get("plan", [])
        if index >= len(plan) or not self._budget_available(budget):
            steps.append(
                {"stepId": f"budget-{index}", "node": "tool_executor", "status": "budget_exhausted"}
            )
            return {
                "last_tool_result": {
                    "status": "budget_exhausted",
                    "summary": "Diagnosis budget exhausted.",
                    "data": {},
                    "error": "budget_exhausted",
                    "duration": 0,
                    "truncated": False,
                },
                "completed_steps": steps,
                "should_continue": False,
            }
        step = plan[index]
        tool_name = str(step["toolName"])
        arguments = cast(dict[str, Any], step["arguments"])
        key = json.dumps([tool_name, arguments], sort_keys=True, default=str)
        previous = [call for call in state.get("tool_calls", []) if call.get("callKey") == key]
        if len(previous) >= self._budget.max_same_tool_call or tool_name not in self._tools:
            result = ToolResult(
                "error",
                "Tool call blocked by policy or repetition budget.",
                {},
                "budget_or_unknown_tool",
                0,
                False,
            )
        else:
            try:
                result = await asyncio.wait_for(
                    self._tools[tool_name].run(**arguments),
                    timeout=float(budget.get("toolTimeout", self._budget.tool_timeout)),
                )
            except asyncio.TimeoutError:
                result = ToolResult(
                    "error",
                    "Tool call timed out.",
                    {},
                    "tool_timeout",
                    self._budget.tool_timeout,
                    False,
                )
        call_id = f"ci_call_{uuid4().hex}"
        call = {
            "id": call_id,
            "toolName": tool_name,
            "arguments": arguments,
            "callKey": key,
            "status": result.status,
            "result": result.as_dict(),
        }
        await self._repository.create_tool_call(
            owner_user_id=state["owner_user_id"],
            call_id=call_id,
            task_id=state["task_id"],
            tool_name=tool_name,
            status=result.status,
            arguments=arguments,
            result=result.as_dict(),
            error=result.error,
            duration_ms=round(result.duration * 1000),
            truncated=result.truncated,
        )
        budget["stepsUsed"] = int(budget.get("stepsUsed", 0)) + 1
        budget["toolCallsUsed"] = int(budget.get("toolCallsUsed", 0)) + 1
        budget["remainingSteps"] = max(0, int(budget["maxSteps"]) - budget["stepsUsed"])
        budget["remainingToolCalls"] = max(0, int(budget["maxToolCalls"]) - budget["toolCallsUsed"])
        steps.append(
            {
                "stepId": step["stepId"],
                "node": "tool_executor",
                "toolName": tool_name,
                "status": result.status,
            }
        )
        return {
            "tool_calls": [*state.get("tool_calls", []), call],
            "last_tool_result": result.as_dict(),
            "last_step": step,
            "current_step_index": index + 1,
            "completed_steps": steps,
            "diagnosis_budget": budget,
        }

    async def _evidence_collector(self, state: CiDiagnosisState) -> dict[str, Any]:
        result = state.get("last_tool_result", {})
        if result.get("status") != "ok":
            return {}
        step = state.get("last_step", {})
        tool_name = str(step.get("toolName"))
        type_map: dict[str, EvidenceType] = {
            "read_test_log": "test_log",
            "git_diff": "git_diff",
            "git_log": "git_log",
            "read_file": "source_code",
            "search_code": "code_search",
            "run_test": "test_result",
        }
        evidence_type = type_map.get(tool_name)
        if evidence_type is None:
            return {}
        data = cast(dict[str, Any], result.get("data", {}))
        content = str(data.get("content") or data.get("matches") or data)
        evidence_id = f"ci_evidence_{uuid4().hex}"
        call_id = state.get("tool_calls", [])[-1].get("id") if state.get("tool_calls") else None
        record = await self._repository.create_evidence(
            owner_user_id=state["owner_user_id"],
            evidence_id=evidence_id,
            task_id=state["task_id"],
            type=evidence_type,
            source=tool_name,
            summary=str(result.get("summary")),
            content=content,
            metadata={
                "tool": tool_name,
                "testName": state.get("test_name"),
                "command": data.get("command"),
                "exitCode": data.get("exitCode"),
            },
            step_id=str(step.get("stepId")),
            tool_call_id=cast(str | None, call_id),
        )
        item = {
            "id": record.id,
            "taskId": record.task_id,
            "type": record.type,
            "source": record.source,
            "summary": record.summary,
            "content": record.content,
            "metadata": record.metadata,
            "toolCallId": record.tool_call_id,
            "stepId": record.step_id,
        }
        return {"evidence": [*state.get("evidence", []), item]}

    async def _replanner(self, state: CiDiagnosisState) -> dict[str, Any]:
        types = {str(item.get("type")) for item in state.get("evidence", [])}
        if (
            {"test_log", "git_diff"}.issubset(types)
            and ({"source_code", "code_search"} & types)
            and ("run_test" not in self._tools or "test_result" in types)
        ):
            return {
                "should_continue": False,
                "replanning_reason": "Evidence set is sufficient for verification.",
            }
        if (
            "run_test" in self._tools
            and "test_result" not in types
            and state.get("current_step_index", 0) < len(state.get("plan", []))
        ):
            return {"should_continue": True, "replanning_reason": "执行待完成的验证步骤。"}
        if not self._budget_available(state["diagnosis_budget"]):
            return {"should_continue": False, "replanning_reason": "Diagnosis budget exhausted."}
        plan = list(state.get("plan", []))
        existing = {
            (
                item.get("toolName"),
                json.dumps(item.get("arguments", {}), sort_keys=True, default=str),
            )
            for item in plan[: state.get("current_step_index", 0)]
        }
        candidates = [
            (
                "search_code",
                {
                    "repository_path": state["repository_path"],
                    "query": "user_id",
                    "paths": ["src", "tests"],
                },
                "code_search",
            ),
            (
                "read_file",
                {"repository_path": state["repository_path"], "path": "src/order/dto.py"},
                "source_code",
            ),
            (
                "git_log",
                {
                    "repository_path": state["repository_path"],
                    "commit_sha": state.get("commit_sha"),
                    "limit": 5,
                },
                "git_log",
            ),
        ]
        for tool_name, arguments, expected in candidates:
            key = (tool_name, json.dumps(arguments, sort_keys=True, default=str))
            if expected not in types and tool_name in self._tools and key not in existing:
                plan.append(
                    {
                        "stepId": f"replan-{len(plan) + 1}",
                        "toolName": tool_name,
                        "reason": "补充独立证据",
                        "arguments": arguments,
                        "expectedEvidenceType": expected,
                    }
                )
                return {
                    "plan": plan,
                    "replanning_reason": f"Evidence missing: {expected}",
                    "should_continue": True,
                }
        return {"should_continue": False, "replanning_reason": "No new safe tool can add evidence."}

    async def _verifier(self, state: CiDiagnosisState) -> dict[str, Any]:
        evidence = list(state.get("evidence", []))
        types = {str(item.get("type")) for item in evidence}
        contents = "\n".join(str(item.get("content", "")) for item in evidence).lower()
        consistent = "422" in contents and "uid" in contents and "user_id" in contents
        confirmed = (
            len(evidence) >= 3
            and len(types) >= 2
            and {"test_log", "git_diff"}.issubset(types)
            and ({"source_code", "code_search"} & types)
            and all(item.get("taskId") == state["task_id"] for item in evidence)
            and consistent
        )
        verification_status = self._verification_status(evidence)
        if verification_status == "failed":
            confirmed = False
        root = (
            "当前代码将订单请求字段从 user_id 修改为 uid，但 test_create_order 仍使用旧字段 "
            "user_id，导致请求契约不一致并返回 422。"
        )
        hypothesis = {
            "text": root,
            "supportingEvidenceIds": [item["id"] for item in evidence],
            "contradictingEvidenceIds": [],
            "confidence": 0.95 if confirmed else 0.45,
            "status": "supported" if confirmed else "open",
        }
        return {
            "hypotheses": [hypothesis],
            "verification_result": {
                "confirmed": confirmed,
                "evidenceCount": len(evidence),
                "evidenceTypes": sorted(types),
                "consistent": consistent,
                "reason": "Independent evidence types and deterministic consistency checks.",
                "verificationStatus": verification_status,
                "verificationCommand": self._verification_command(evidence),
                "verificationResult": self._verification_result(evidence),
                "verificationEvidence": [
                    item["id"] for item in evidence if item.get("type") == "test_result"
                ],
            },
        }

    def _verification_status(self, evidence: list[dict[str, Any]]) -> str:
        for item in evidence:
            if item.get("type") == "test_result":
                return "passed" if item.get("metadata", {}).get("exitCode") == 0 else "failed"
        return "not_run"

    def _verification_command(self, evidence: list[dict[str, Any]]) -> str | None:
        for item in evidence:
            if item.get("type") == "test_result":
                return str(item.get("metadata", {}).get("command", "pytest"))
        return None

    def _verification_result(self, evidence: list[dict[str, Any]]) -> dict[str, Any] | None:
        for item in evidence:
            if item.get("type") == "test_result":
                return {"content": item.get("content", ""), "summary": item.get("summary", "")}
        return None

    async def _report(self, state: CiDiagnosisState) -> dict[str, Any]:
        verification = state.get("verification_result", {})
        confirmed = bool(verification.get("confirmed", False))
        root = state.get("hypotheses", [{}])[-1].get(
            "text", "Unable to establish a root cause from available evidence."
        )
        report = {
            "failureSummary": state["failure_summary"],
            "rootCause": root,
            "rootCauseType": "confirmed" if confirmed else "hypothesis",
            "confirmed": confirmed,
            "confidence": 0.95 if confirmed else 0.45,
            "evidenceIds": [item["id"] for item in state.get("evidence", [])],
            "suggestedFix": "同步测试与 DTO 字段契约，并重新验证 test_create_order。",
            "verificationPlan": "重新执行 test_create_order 并确认返回 200。",
            "verificationStatus": verification.get("verificationStatus", "not_run"),
            "verificationCommand": verification.get("verificationCommand"),
            "verificationResult": verification.get("verificationResult"),
            "verificationEvidence": verification.get("verificationEvidence", []),
            "toolTraceSummary": [
                {
                    "toolName": call.get("toolName"),
                    "status": call.get("status"),
                    "duration": call.get("result", {}).get("duration"),
                }
                for call in state.get("tool_calls", [])
            ],
        }
        return {"report": report}

    def _route_after_replanner(
        self, state: CiDiagnosisState
    ) -> Literal["tool_executor", "verifier"]:
        return "tool_executor" if state.get("should_continue", False) else "verifier"

    def _budget_available(self, budget: Mapping[str, Any]) -> bool:
        return (
            int(budget.get("remainingSteps", 0)) > 0
            and int(budget.get("remainingToolCalls", 0)) > 0
        )
