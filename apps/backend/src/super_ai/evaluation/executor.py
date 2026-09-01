from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, cast
from uuid import uuid4

from super_ai.ci_diagnosis.repository import SQLiteCiDiagnosticRepository
from super_ai.ci_diagnosis.workflow import CiDiagnosisWorkflow
from super_ai.developer_tools import (
    GitDiffTool,
    GitLogTool,
    ReadFileTool,
    ReadTestLogTool,
    SearchCodeTool,
    WorkspaceGuard,
)

from .dataset import EvaluationCase


class EvaluationWorkflowExecutor:
    def __init__(self, ci_repository: SQLiteCiDiagnosticRepository, workspace_root: Path) -> None:
        self.repository = ci_repository
        self.guard = WorkspaceGuard([workspace_root])
        self.workspace_root = workspace_root

    async def execute(self, case: EvaluationCase) -> dict[str, Any]:
        started_at = monotonic()
        task_id = f"eval_task_{uuid4().hex}"
        repository_path = str(self.workspace_root)
        log = case.test_log
        await self.repository.create_task(
            owner_user_id="evaluation",
            task_id=task_id,
            repository_path=repository_path,
            failure_summary=case.failure_summary,
            test_log=log,
        )
        tools = {
            "read_test_log": ReadTestLogTool(),
            "git_diff": GitDiffTool(self.guard),
            "git_log": GitLogTool(self.guard),
            "read_file": ReadFileTool(self.guard),
            "search_code": SearchCodeTool(self.guard),
        }
        result = dict(
            await CiDiagnosisWorkflow(repository=self.repository, tools=tools).run(
                task_id=task_id,
                owner_user_id="evaluation",
                tenant_id=None,
                repository_path=repository_path,
                failure_summary=case.failure_summary,
                test_log=log,
            )
        )
        result["status"] = "completed"
        result["stepCount"] = len(cast(list[object], result.get("completed_steps", [])))
        result["toolCallCount"] = len(cast(list[object], result.get("tool_calls", [])))
        result["latency"] = monotonic() - started_at
        result["executionMode"] = case.execution_mode
        return result
