"""Owner-scoped CI diagnosis persistence boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from super_ai.ci_diagnosis.models import (
    CiDiagnosticEvidenceModel,
    CiDiagnosticStepModel,
    CiDiagnosticTaskModel,
    CiToolCallModel,
)
from super_ai.memory.models import utc_now

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class CiDiagnosticTaskRecord:
    id: str
    owner_user_id: str
    tenant_id: str | None
    repository_path: str
    failure_summary: str
    test_log: str
    test_name: str | None
    commit_sha: str | None
    base_commit_sha: str | None
    status: str
    workflow_version: str
    model_name: str | None
    prompt_version: str | None
    result_payload: JsonObject
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


@dataclass(frozen=True, slots=True)
class CiDiagnosticStepRecord:
    id: str
    owner_user_id: str
    task_id: str
    sequence: int
    node: str
    action: str
    status: str
    payload: JsonObject
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CiDiagnosticEvidenceRecord:
    id: str
    owner_user_id: str
    task_id: str
    step_id: str | None
    tool_call_id: str | None
    type: str
    source: str
    summary: str
    content: str
    metadata: JsonObject
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CiToolCallRecord:
    id: str
    owner_user_id: str
    task_id: str
    tool_name: str
    status: str
    arguments: JsonObject
    result: JsonObject
    error: str | None
    duration_ms: int | None
    truncated: bool
    created_at: datetime


class CiDiagnosticRepository(Protocol):
    async def update_task(
        self,
        *,
        owner_user_id: str,
        task_id: str,
        status: str | None = None,
        result_payload: JsonObject | None = None,
        started_at: datetime | None = None,
        completed_at: datetime | None = None,
    ) -> CiDiagnosticTaskRecord | None: ...

    async def create_evidence(
        self,
        *,
        owner_user_id: str,
        evidence_id: str,
        task_id: str,
        type: str,
        source: str,
        summary: str,
        content: str,
        metadata: JsonObject | None = None,
        step_id: str | None = None,
        tool_call_id: str | None = None,
    ) -> CiDiagnosticEvidenceRecord: ...

    async def create_tool_call(
        self,
        *,
        owner_user_id: str,
        call_id: str,
        task_id: str,
        tool_name: str,
        status: str,
        arguments: JsonObject | None = None,
        result: JsonObject | None = None,
        error: str | None = None,
        duration_ms: int | None = None,
        truncated: bool = False,
    ) -> CiToolCallRecord: ...


class SQLiteCiDiagnosticRepository:
    """SQLite implementation with owner and task scope on every read."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_task(
        self,
        *,
        owner_user_id: str,
        task_id: str,
        repository_path: str,
        failure_summary: str,
        test_log: str,
        status: str = "queued",
        tenant_id: str | None = None,
        test_name: str | None = None,
        commit_sha: str | None = None,
        base_commit_sha: str | None = None,
        workflow_version: str = "ci-diagnosis-v1",
        model_name: str | None = None,
        prompt_version: str | None = None,
        result_payload: JsonObject | None = None,
        created_at: datetime | None = None,
    ) -> CiDiagnosticTaskRecord:
        row = CiDiagnosticTaskModel(
            id=task_id,
            owner_user_id=owner_user_id,
            tenant_id=tenant_id,
            repository_path=repository_path,
            failure_summary=failure_summary,
            test_log=test_log,
            test_name=test_name,
            commit_sha=commit_sha,
            base_commit_sha=base_commit_sha,
            status=status,
            workflow_version=workflow_version,
            model_name=model_name,
            prompt_version=prompt_version,
            result_payload=result_payload or {},
            created_at=created_at or utc_now(),
        )
        async with self._session_factory() as session:
            session.add(row)
            await session.commit()
        return _task_record(row)

    async def get_task(self, *, owner_user_id: str, task_id: str) -> CiDiagnosticTaskRecord | None:
        stmt = select(CiDiagnosticTaskModel).where(
            CiDiagnosticTaskModel.id == task_id,
            CiDiagnosticTaskModel.owner_user_id == owner_user_id,
        )
        async with self._session_factory() as session:
            row = (await session.scalars(stmt)).one_or_none()
        return _task_record(row) if row is not None else None

    async def update_task(
        self,
        *,
        owner_user_id: str,
        task_id: str,
        status: str | None = None,
        result_payload: JsonObject | None = None,
        started_at: datetime | None = None,
        completed_at: datetime | None = None,
    ) -> CiDiagnosticTaskRecord | None:
        async with self._session_factory() as session:
            row = await _require_task(session, owner_user_id, task_id)
            if status is not None:
                row.status = status
            if result_payload is not None:
                row.result_payload = result_payload
            if started_at is not None:
                row.started_at = started_at
            if completed_at is not None:
                row.completed_at = completed_at
            await session.commit()
        return _task_record(row)

    async def list_tasks(self, *, owner_user_id: str) -> list[CiDiagnosticTaskRecord]:
        stmt = (
            select(CiDiagnosticTaskModel)
            .where(CiDiagnosticTaskModel.owner_user_id == owner_user_id)
            .order_by(CiDiagnosticTaskModel.created_at.desc())
        )
        async with self._session_factory() as session:
            rows = list((await session.scalars(stmt)).all())
        return [_task_record(row) for row in rows]

    async def create_step(
        self,
        *,
        owner_user_id: str,
        step_id: str,
        task_id: str,
        sequence: int,
        node: str,
        action: str,
        status: str,
        payload: JsonObject | None = None,
    ) -> CiDiagnosticStepRecord:
        row = CiDiagnosticStepModel(
            id=step_id,
            owner_user_id=owner_user_id,
            task_id=task_id,
            sequence=sequence,
            node=node,
            action=action,
            status=status,
            payload=payload or {},
            created_at=utc_now(),
        )
        async with self._session_factory() as session:
            await _require_task(session, owner_user_id, task_id)
            session.add(row)
            await session.commit()
        return _step_record(row)

    async def list_steps(self, *, owner_user_id: str, task_id: str) -> list[CiDiagnosticStepRecord]:
        stmt = (
            select(CiDiagnosticStepModel)
            .where(
                CiDiagnosticStepModel.owner_user_id == owner_user_id,
                CiDiagnosticStepModel.task_id == task_id,
            )
            .order_by(CiDiagnosticStepModel.sequence.asc())
        )
        async with self._session_factory() as session:
            rows = list((await session.scalars(stmt)).all())
        return [_step_record(row) for row in rows]

    async def create_evidence(
        self,
        *,
        owner_user_id: str,
        evidence_id: str,
        task_id: str,
        type: str,
        source: str,
        summary: str,
        content: str,
        metadata: JsonObject | None = None,
        step_id: str | None = None,
        tool_call_id: str | None = None,
    ) -> CiDiagnosticEvidenceRecord:
        row = CiDiagnosticEvidenceModel(
            id=evidence_id,
            owner_user_id=owner_user_id,
            task_id=task_id,
            step_id=step_id,
            tool_call_id=tool_call_id,
            type=type,
            source=source,
            summary=summary,
            content=content,
            metadata_json=metadata or {},
            created_at=utc_now(),
        )
        async with self._session_factory() as session:
            await _require_task(session, owner_user_id, task_id)
            session.add(row)
            await session.commit()
        return _evidence_record(row)

    async def list_evidence(
        self, *, owner_user_id: str, task_id: str
    ) -> list[CiDiagnosticEvidenceRecord]:
        stmt = (
            select(CiDiagnosticEvidenceModel)
            .where(
                CiDiagnosticEvidenceModel.owner_user_id == owner_user_id,
                CiDiagnosticEvidenceModel.task_id == task_id,
            )
            .order_by(CiDiagnosticEvidenceModel.created_at.asc())
        )
        async with self._session_factory() as session:
            rows = list((await session.scalars(stmt)).all())
        return [_evidence_record(row) for row in rows]

    async def create_tool_call(
        self,
        *,
        owner_user_id: str,
        call_id: str,
        task_id: str,
        tool_name: str,
        status: str,
        arguments: JsonObject | None = None,
        result: JsonObject | None = None,
        error: str | None = None,
        duration_ms: int | None = None,
        truncated: bool = False,
    ) -> CiToolCallRecord:
        row = CiToolCallModel(
            id=call_id,
            owner_user_id=owner_user_id,
            task_id=task_id,
            tool_name=tool_name,
            status=status,
            arguments=arguments or {},
            result=result or {},
            error=error,
            duration_ms=duration_ms,
            truncated=truncated,
            created_at=utc_now(),
        )
        async with self._session_factory() as session:
            await _require_task(session, owner_user_id, task_id)
            session.add(row)
            await session.commit()
        return _tool_call_record(row)

    async def list_tool_calls(self, *, owner_user_id: str, task_id: str) -> list[CiToolCallRecord]:
        stmt = (
            select(CiToolCallModel)
            .where(
                CiToolCallModel.owner_user_id == owner_user_id,
                CiToolCallModel.task_id == task_id,
            )
            .order_by(CiToolCallModel.created_at.asc())
        )
        async with self._session_factory() as session:
            rows = list((await session.scalars(stmt)).all())
        return [_tool_call_record(row) for row in rows]


async def _require_task(
    session: AsyncSession, owner_user_id: str, task_id: str
) -> CiDiagnosticTaskModel:
    row = (
        await session.scalars(
            select(CiDiagnosticTaskModel).where(
                CiDiagnosticTaskModel.id == task_id,
                CiDiagnosticTaskModel.owner_user_id == owner_user_id,
            )
        )
    ).one_or_none()
    if row is None:
        raise LookupError("CI diagnostic task is unavailable in the current owner scope.")
    return row


def _task_record(row: CiDiagnosticTaskModel) -> CiDiagnosticTaskRecord:
    return CiDiagnosticTaskRecord(
        id=row.id,
        owner_user_id=row.owner_user_id,
        tenant_id=row.tenant_id,
        repository_path=row.repository_path,
        failure_summary=row.failure_summary,
        test_log=row.test_log,
        test_name=row.test_name,
        commit_sha=row.commit_sha,
        base_commit_sha=row.base_commit_sha,
        status=row.status,
        workflow_version=row.workflow_version,
        model_name=row.model_name,
        prompt_version=row.prompt_version,
        result_payload=dict(row.result_payload),
        created_at=row.created_at,
        started_at=row.started_at,
        completed_at=row.completed_at,
    )


def _step_record(row: CiDiagnosticStepModel) -> CiDiagnosticStepRecord:
    return CiDiagnosticStepRecord(
        row.id,
        row.owner_user_id,
        row.task_id,
        row.sequence,
        row.node,
        row.action,
        row.status,
        dict(row.payload),
        row.created_at,
    )


def _evidence_record(row: CiDiagnosticEvidenceModel) -> CiDiagnosticEvidenceRecord:
    return CiDiagnosticEvidenceRecord(
        row.id,
        row.owner_user_id,
        row.task_id,
        row.step_id,
        row.tool_call_id,
        row.type,
        row.source,
        row.summary,
        row.content,
        dict(row.metadata_json),
        row.created_at,
    )


def _tool_call_record(row: CiToolCallModel) -> CiToolCallRecord:
    return CiToolCallRecord(
        row.id,
        row.owner_user_id,
        row.task_id,
        row.tool_name,
        row.status,
        dict(row.arguments),
        dict(row.result),
        row.error,
        row.duration_ms,
        row.truncated,
        row.created_at,
    )
