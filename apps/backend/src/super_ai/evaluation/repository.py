from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import EvaluationCaseResultModel, EvaluationRunModel


class EvaluationRepository:
    def __init__(self, factory: async_sessionmaker[AsyncSession]) -> None:
        self.factory = factory

    async def create_run(
        self,
        *,
        run_id: str,
        dataset_id: str,
        dataset_version: str,
        run_name: str,
        model: str | None,
        prompt_version: str | None,
        workflow_version: str | None,
    ) -> EvaluationRunModel:
        row = EvaluationRunModel(
            id=run_id,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            run_name=run_name,
            model=model,
            prompt_version=prompt_version,
            workflow_version=workflow_version,
            status="queued",
            metrics={},
            report={},
        )
        async with self.factory() as session:
            session.add(row)
            await session.commit()
        return row

    async def get_run(self, run_id: str) -> EvaluationRunModel | None:
        async with self.factory() as session:
            return await session.get(EvaluationRunModel, run_id)

    async def list_runs(self) -> list[EvaluationRunModel]:
        async with self.factory() as session:
            return list(
                (
                    await session.scalars(
                        select(EvaluationRunModel).order_by(EvaluationRunModel.created_at.desc())
                    )
                ).all()
            )

    async def update_run(
        self,
        run_id: str,
        *,
        status: str,
        metrics: dict[str, Any] | None = None,
        report: dict[str, Any] | None = None,
        completed_at: datetime | None = None,
    ) -> EvaluationRunModel | None:
        async with self.factory() as session:
            row = await session.get(EvaluationRunModel, run_id)
            if row is None:
                return None
            row.status = status
            if metrics is not None:
                row.metrics = metrics
            if report is not None:
                row.report = report
            row.completed_at = completed_at
            await session.commit()
            return row

    async def add_case(self, **values: Any) -> EvaluationCaseResultModel:
        async with self.factory() as session:
            row = EvaluationCaseResultModel(**values)
            session.add(row)
            await session.commit()
            return row

    async def list_cases(self, run_id: str) -> list[EvaluationCaseResultModel]:
        async with self.factory() as session:
            return list(
                (
                    await session.scalars(
                        select(EvaluationCaseResultModel).where(
                            EvaluationCaseResultModel.run_id == run_id
                        )
                    )
                ).all()
            )
