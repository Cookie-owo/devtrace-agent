from __future__ import annotations

from typing import Any, cast
from uuid import uuid4

from fastapi import APIRouter, Request

from .dataset import load_builtin_dataset

router = APIRouter(prefix="/evaluation", tags=["evaluation"])
def _run_payload(row: Any) -> dict[str, object]:
    return {
        "runId": row.id,
        "datasetId": row.dataset_id,
        "datasetVersion": row.dataset_version,
        "runName": row.run_name,
        "model": row.model,
        "promptVersion": row.prompt_version,
        "workflowVersion": row.workflow_version,
        "status": row.status,
        "metrics": row.metrics,
        "report": row.report,
        "createdAt": row.created_at.isoformat() if row.created_at else None,
        "completedAt": row.completed_at.isoformat() if row.completed_at else None,
    }


@router.get("/datasets")
async def datasets() -> dict[str, object]:
    dataset = load_builtin_dataset()
    return {
        "ok": True,
        "data": {
            "items": [
                {
                    "version": "builtin-v1",
                    "caseCount": len(dataset),
                    "categories": sorted({case.category for case in dataset}),
                }
            ]
        },
    }


@router.post("/runs", status_code=202)
async def create_run(request: Request, payload: dict[str, object]) -> dict[str, object]:
    run_id = f"eval_{uuid4().hex}"
    repository = request.app.state.evaluation_repository
    await repository.create_run(
        run_id=run_id,
        dataset_id="builtin",
        dataset_version="builtin-v1",
        run_name=str(payload.get("run_name", run_id)),
        model=payload.get("model") if isinstance(payload.get("model"), str) else None,
        prompt_version=payload.get("prompt_version")
        if isinstance(payload.get("prompt_version"), str)
        else None,
        workflow_version=payload.get("workflow_version")
        if isinstance(payload.get("workflow_version"), str)
        else None,
    )
    await request.app.state.memory_repositories.background_jobs.enqueue(
        owner_user_id="evaluation",
        job_id=f"job_{uuid4().hex}",
        kind="evaluation_run",
        resource_type="evaluation_run",
        resource_id=run_id,
        payload={"runId": run_id},
        max_attempts=1,
        timeout_seconds=600,
    )
    await request.app.state.background_job_runtime.start()
    row = await repository.get_run(run_id)
    return {"ok": True, "data": _run_payload(row)}


@router.get("/runs")
async def list_runs(request: Request) -> dict[str, object]:
    rows = await request.app.state.evaluation_repository.list_runs()
    return {
        "ok": True,
        "data": {
            "items": [
                _run_payload(row)
                for row in rows
            ]
        },
    }


@router.get("/runs/{run_id}")
async def get_run(request: Request, run_id: str) -> dict[str, object]:
    row = await request.app.state.evaluation_repository.get_run(run_id)
    if row is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return {"ok": True, "data": _run_payload(row)}


@router.get("/runs/{run_id}/cases")
async def get_run_cases(request: Request, run_id: str) -> dict[str, object]:
    if await request.app.state.evaluation_repository.get_run(run_id) is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    rows = await request.app.state.evaluation_repository.list_cases(run_id)
    return {
        "ok": True,
        "data": {
            "items": [
                {
                    "caseId": row.case_id,
                    "category": row.category,
                    "status": row.status,
                    "expectedResult": row.expected_result,
                    "actualResult": row.actual_result,
                    "confirmed": row.confirmed,
                    "executionMode": row.execution_mode,
                    "evidenceTypes": row.evidence_types,
                    "toolCalls": row.tool_calls,
                    "metrics": row.metrics,
                }
                for row in rows
            ]
        },
    }


@router.get("/runs/{run_id}/metrics")
async def get_run_metrics(request: Request, run_id: str) -> dict[str, object]:
    row = await request.app.state.evaluation_repository.get_run(run_id)
    if row is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return {"ok": True, "data": row.metrics}


@router.post("/compare")
async def compare_runs(request: Request, payload: dict[str, str]) -> dict[str, object]:
    repository = request.app.state.evaluation_repository
    baseline = await repository.get_run(payload["baselineRunId"])
    candidate = await repository.get_run(payload["candidateRunId"])
    if baseline is None or candidate is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    baseline_metrics = cast(dict[str, Any], baseline.metrics or {})
    candidate_metrics = cast(dict[str, Any], candidate.metrics or {})
    keys = sorted(set(baseline_metrics) | set(candidate_metrics))
    delta = {
        key: (candidate_metrics.get(key, 0) - baseline_metrics.get(key, 0))
        for key in keys
        if isinstance(candidate_metrics.get(key, 0), (int, float))
        and isinstance(baseline_metrics.get(key, 0), (int, float))
    }
    return {
        "ok": True,
        "data": {"baseline": baseline_metrics, "candidate": candidate_metrics, "delta": delta},
    }
