"""CI Diagnosis API and durable job adapter."""
# FastAPI dependency defaults are intentional route declarations.
# ruff: noqa: B008
# FastAPI discovers route functions through decorators.
# pyright: reportUnusedFunction=false

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from typing import cast
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

from super_ai.auth.repositories import UserRecord
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
from super_ai.jobs import BackgroundJobContext, JobCancelled
from super_ai.memory.repositories import BackgroundJobRepository
from super_ai.project_config import load_project_config

bearer = HTTPBearer(auto_error=False)


class CiDiagnosisTaskRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    repository_path: str = Field(alias="repositoryPath", min_length=1)
    failure_summary: str = Field(alias="failureSummary", min_length=1)
    test_log: str = Field(alias="testLog", min_length=1)
    test_name: str | None = Field(default=None, alias="testName")
    commit_sha: str | None = Field(default=None, alias="commitSha")
    base_commit_sha: str | None = Field(default=None, alias="baseCommitSha")


def register_ci_routes(app: FastAPI) -> APIRouter:
    router = APIRouter(prefix="/ci-diagnosis", tags=["ci-diagnosis"])

    async def current_user(
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    ) -> UserRecord:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Authentication required.")
        service = request.app.state.auth_service
        user = await service.authenticate_token(credentials.credentials)
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication required.")
        return user

    def repository(request: Request) -> SQLiteCiDiagnosticRepository:
        return cast(SQLiteCiDiagnosticRepository, request.app.state.ci_diagnosis_repository)

    def jobs(request: Request) -> BackgroundJobRepository:
        return cast(BackgroundJobRepository, request.app.state.memory_repositories.background_jobs)

    def workspace_guard(request: Request) -> WorkspaceGuard:
        config = load_project_config(request.app.state.project_config_path)
        backend = cast(Mapping[str, object], config.get("backend", {}))
        roots = backend.get("workspaceRoots", [])
        root_values = cast(list[object], roots) if isinstance(roots, list) else []
        if not roots or not all(isinstance(root_value, str) for root_value in root_values):
            raise HTTPException(status_code=500, detail="Workspace configuration is invalid.")
        try:
            return WorkspaceGuard(cast(list[str], roots))
        except ValueError as exc:
            raise HTTPException(status_code=500, detail="Workspace is not configured.") from exc

    async def task_for_user(request: Request, task_id: str, user: UserRecord):
        task = await repository(request).get_task(owner_user_id=user.id, task_id=task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        return task

    @router.post("/tasks", status_code=202)
    async def create_task(
        request: Request,
        body: CiDiagnosisTaskRequest,
        user: UserRecord = Depends(current_user),
    ):
        guard = workspace_guard(request)
        try:
            path = guard.resolve_repository(body.repository_path)
        except ValueError as exc:
            raise HTTPException(
                status_code=400, detail="Repository path is outside workspace."
            ) from exc
        task_id = f"ci_{uuid4().hex}"
        job_id = f"job_{uuid4().hex}"
        await repository(request).create_task(
            owner_user_id=user.id,
            task_id=task_id,
            repository_path=str(path),
            failure_summary=body.failure_summary,
            test_log=body.test_log,
            test_name=body.test_name,
            commit_sha=body.commit_sha,
            base_commit_sha=body.base_commit_sha,
        )
        job = await jobs(request).enqueue(
            owner_user_id=user.id,
            job_id=job_id,
            kind="ci_diagnosis",
            resource_type="ci_diagnosis_task",
            resource_id=task_id,
            payload={"taskId": task_id},
            max_attempts=3,
            timeout_seconds=120,
        )
        await request.app.state.background_job_runtime.start()
        return {"ok": True, "data": {"taskId": task_id, "status": "queued", "jobId": job.id}}

    @router.get("/tasks/{task_id}")
    async def get_task(request: Request, task_id: str, user: UserRecord = Depends(current_user)):
        task = await task_for_user(request, task_id, user)
        return {"ok": True, "data": _record_payload(task)}

    @router.get("/tasks/{task_id}/steps")
    async def get_steps(request: Request, task_id: str, user: UserRecord = Depends(current_user)):
        await task_for_user(request, task_id, user)
        return {
            "ok": True,
            "data": {
                "items": [
                    asdict(record)
                    for record in await repository(request).list_steps(
                        owner_user_id=user.id, task_id=task_id
                    )
                ]
            },
        }

    @router.get("/tasks/{task_id}/evidence")
    async def get_evidence(
        request: Request, task_id: str, user: UserRecord = Depends(current_user)
    ):
        await task_for_user(request, task_id, user)
        return {
            "ok": True,
            "data": {
                "items": [
                    asdict(record)
                    for record in await repository(request).list_evidence(
                        owner_user_id=user.id, task_id=task_id
                    )
                ]
            },
        }

    @router.get("/tasks/{task_id}/tool-calls")
    async def get_tool_calls(
        request: Request, task_id: str, user: UserRecord = Depends(current_user)
    ):
        await task_for_user(request, task_id, user)
        return {
            "ok": True,
            "data": {
                "items": [
                    asdict(record)
                    for record in await repository(request).list_tool_calls(
                        owner_user_id=user.id, task_id=task_id
                    )
                ]
            },
        }

    @router.get("/tasks/{task_id}/events")
    async def get_events(
        request: Request,
        task_id: str,
        user: UserRecord = Depends(current_user),
        after_sequence: int = Query(0, alias="afterSequence"),
    ) -> StreamingResponse:
        task = await task_for_user(request, task_id, user)
        job = await jobs(request).find_for_resource(
            owner_user_id=user.id, resource_type="ci_diagnosis_task", resource_id=task.id
        )
        events = (
            []
            if job is None
            else await jobs(request).list_events(
                owner_user_id=user.id, job_id=job.id, after_sequence=after_sequence
            )
        )

        async def stream():
            for record in events:
                payload = dict(record.payload)
                event_type = str(payload.get("type", "ci.diagnosis.event"))
                envelope = {
                    "id": str(payload.get("event_id", record.id)),
                    "type": event_type,
                    "channel": "aiops",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "sequence": record.sequence,
                    "data": payload.get("data", {}),
                }
                encoded = json.dumps(envelope, ensure_ascii=False)
                yield f"id: {record.sequence}\nevent: {event_type}\ndata: {encoded}\n\n"

        return StreamingResponse(stream(), media_type="text/event-stream")

    @router.post("/tasks/{task_id}:cancel")
    async def cancel_task(request: Request, task_id: str, user: UserRecord = Depends(current_user)):
        task = await task_for_user(request, task_id, user)
        if task.status == "completed":
            raise HTTPException(status_code=409, detail="Task is already completed.")
        job = await jobs(request).find_for_resource(
            owner_user_id=user.id, resource_type="ci_diagnosis_task", resource_id=task_id
        )
        if job is None:
            raise HTTPException(status_code=404, detail="Task job not found.")
        updated = await jobs(request).request_cancel(owner_user_id=user.id, job_id=job.id)
        return {
            "ok": True,
            "data": {
                "taskId": task_id,
                "status": updated.status if updated else "cancel_requested",
            },
        }

    @router.post("/tasks/{task_id}:repair", status_code=202)
    async def repair_task(request: Request, task_id: str, user: UserRecord = Depends(current_user)):
        task = await task_for_user(request, task_id, user)
        if task.status != "completed":
            raise HTTPException(status_code=409, detail="Diagnosis must complete before repair.")
        job_id = f"job_{uuid4().hex}"
        await jobs(request).enqueue(
            owner_user_id=user.id,
            job_id=job_id,
            kind="ci_repair",
            resource_type="ci_diagnosis_task",
            resource_id=task_id,
            payload={"taskId": task_id},
            max_attempts=1,
            timeout_seconds=120,
        )
        await request.app.state.background_job_runtime.start()
        return {"ok": True, "data": {"taskId": task_id, "status": "repair_queued", "jobId": job_id}}

    return router


def build_ci_job_handler(app: FastAPI):
    async def handle(context: BackgroundJobContext) -> None:
        task_id = str(context.job.payload.get("taskId", ""))
        repository = cast(SQLiteCiDiagnosticRepository, app.state.ci_diagnosis_repository)
        task = await repository.get_task(owner_user_id=context.job.owner_user_id, task_id=task_id)
        if task is None:
            raise LookupError("CI diagnostic task not found.")
        if task.status == "completed":
            return
        await context.raise_if_cancelled()
        await repository.update_task(
            owner_user_id=task.owner_user_id, task_id=task.id, status="running"
        )
        config = load_project_config(app.state.project_config_path)
        backend = cast(Mapping[str, object], config.get("backend", {}))
        roots = cast(list[str], backend.get("workspaceRoots", []))
        guard = WorkspaceGuard(roots)
        tools = {
            "read_test_log": ReadTestLogTool(),
            "git_diff": GitDiffTool(guard),
            "git_log": GitLogTool(guard),
            "read_file": ReadFileTool(guard),
            "search_code": SearchCodeTool(guard),
        }
        workflow = CiDiagnosisWorkflow(repository=repository, tools=tools)
        await context.append_event(
            {
                "event_id": f"evt_{uuid4().hex}",
                "task_id": task.id,
                "type": "ci.diagnosis.started",
                "data": {"status": "running"},
            }
        )
        try:
            result = await workflow.run(
                task_id=task.id,
                owner_user_id=task.owner_user_id,
                tenant_id=task.tenant_id,
                repository_path=task.repository_path,
                failure_summary=task.failure_summary,
                test_log=task.test_log,
                test_name=task.test_name,
                commit_sha=task.commit_sha,
                base_commit_sha=task.base_commit_sha,
            )
        except JobCancelled:
            await context.append_event(
                {
                    "event_id": f"evt_{uuid4().hex}",
                    "task_id": task.id,
                    "type": "ci.diagnosis.cancelled",
                    "data": {},
                }
            )
            raise
        except Exception as exc:
            await context.append_event(
                {
                    "event_id": f"evt_{uuid4().hex}",
                    "task_id": task.id,
                    "type": "ci.diagnosis.failed",
                    "data": {"error": exc.__class__.__name__},
                }
            )
            raise
        trace = result.get("trace", {})
        events = [
            ("ci.plan.created", {"plan": result.get("plan", [])}),
            ("ci.tool.completed", {"toolCalls": result.get("tool_calls", [])}),
            ("ci.evidence.created", {"evidence": result.get("evidence", [])}),
            ("ci.verification.completed", {"verification": result.get("verification_result", {})}),
            ("ci.report.created", {"report": result.get("report", {})}),
            ("complete", result.get("report", {})),
        ]
        for event_type, data in events:
            await context.append_event(
                {
                    "event_id": f"evt_{uuid4().hex}",
                    "task_id": task.id,
                    "type": event_type,
                    "data": data,
                    "trace": trace,
                }
            )

    return handle


def build_ci_repair_job_handler(app: FastAPI):
    async def handle(context: BackgroundJobContext) -> None:
        from super_ai.repair import ControlledRepairService

        task_id = str(context.job.payload.get("taskId", ""))
        repository = cast(SQLiteCiDiagnosticRepository, app.state.ci_diagnosis_repository)
        task = await repository.get_task(owner_user_id=context.job.owner_user_id, task_id=task_id)
        if task is None:
            raise LookupError("CI diagnostic task not found.")
        config = load_project_config(app.state.project_config_path)
        backend = cast(Mapping[str, object], config.get("backend", {}))
        roots = cast(list[str], backend.get("workspaceRoots", []))
        outcome = await ControlledRepairService(roots[0]).repair_golden_dto(task.repository_path)
        payload = dict(task.result_payload or {})
        payload["repair"] = outcome.as_dict()
        await repository.update_task(
            owner_user_id=task.owner_user_id,
            task_id=task.id,
            status="completed",
            result_payload=payload,
            completed_at=None,
        )

    return handle


def _record_payload(task: object) -> dict[str, object]:
    record = task
    return {
        key: getattr(record, key)
        for key in (
            "id",
            "owner_user_id",
            "tenant_id",
            "repository_path",
            "failure_summary",
            "test_name",
            "commit_sha",
            "status",
            "result_payload",
            "created_at",
            "completed_at",
        )
    }
