from __future__ import annotations

# The test exercises dynamic FastAPI wiring and intentionally uses fixture helpers.
# pyright: reportPrivateUsage=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownLambdaType=false, reportPossiblyUnboundVariable=false, reportUnusedImport=false
# ruff: noqa: E501,F401,F811
import asyncio
from pathlib import Path
from typing import cast

import httpx
import pytest

from super_ai.api.app import MilvusHealthCheckProvider, create_app
from test_ci_workflow import _golden_repository, migrated_database_url


@pytest.mark.asyncio
async def test_http_sse_golden_path_and_owner_isolation(
    tmp_path: Path, migrated_database_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository_path, commit_sha = _golden_repository(tmp_path)
    config = {"backend": {"workspaceRoots": [str(tmp_path)]}}
    monkeypatch.setattr(
        "super_ai.ci_diagnosis.api.load_project_config", lambda *_args, **_kwargs: config
    )

    class VectorStore:
        def health_check(self):
            return None

    app = create_app(
        database_url=migrated_database_url,
        vector_store=cast(MilvusHealthCheckProvider, VectorStore()),
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        first = await client.post(
            "/auth/register",
            json={"email": "ci-a@example.com", "displayName": "A", "password": "password-123"},
        )
        second = await client.post(
            "/auth/register",
            json={"email": "ci-b@example.com", "displayName": "B", "password": "password-123"},
        )
        token_a = first.json()["data"]["accessToken"]
        token_b = second.json()["data"]["accessToken"]
        log = 'FAILED tests/test_order.py::test_create_order\nExpected: 200\nActual: 422\nresponse: {"loc": ["body", "uid"], "msg": "Field required"}'
        response = await client.post(
            "/ci-diagnosis/tasks",
            headers={"Authorization": f"Bearer {token_a}"},
            json={
                "repositoryPath": str(repository_path),
                "failureSummary": "test_create_order returns 422",
                "testLog": log,
                "commitSha": commit_sha,
            },
        )
        assert response.status_code == 202, response.text
        task_id = response.json()["data"]["taskId"]
        assert (
            await client.get(
                f"/ci-diagnosis/tasks/{task_id}", headers={"Authorization": f"Bearer {token_b}"}
            )
        ).status_code == 404
        for _ in range(60):
            task_response = await client.get(
                f"/ci-diagnosis/tasks/{task_id}", headers={"Authorization": f"Bearer {token_a}"}
            )
            task = task_response.json()["data"]
            if task["status"] in {"completed", "failed"}:
                break
            await asyncio.sleep(0.05)
        assert task["status"] == "completed", task
        evidence = (
            await client.get(
                f"/ci-diagnosis/tasks/{task_id}/evidence",
                headers={"Authorization": f"Bearer {token_a}"},
            )
        ).json()["data"]["items"]
        tools = (
            await client.get(
                f"/ci-diagnosis/tasks/{task_id}/tool-calls",
                headers={"Authorization": f"Bearer {token_a}"},
            )
        ).json()["data"]["items"]
        assert {item["type"] for item in evidence} >= {"test_log", "git_diff"}
        assert {item["type"] for item in evidence} & {"source_code", "code_search"}
        report = task["result_payload"]["report"]
        assert report["confirmed"] is True
        assert set(report["evidenceIds"]).issubset({item["id"] for item in evidence})
        assert tools
        event_response = await client.get(
            f"/ci-diagnosis/tasks/{task_id}/events",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        event_text = event_response.text
        for event_name in (
            "ci.diagnosis.started",
            "ci.plan.created",
            "ci.tool.completed",
            "ci.evidence.created",
            "ci.verification.completed",
            "ci.report.created",
            "complete",
        ):
            assert event_name in event_text
