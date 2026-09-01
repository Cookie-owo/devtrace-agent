from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from super_ai.memory.models import Base, utc_now


class EvaluationRunModel(Base):
    __tablename__ = "evaluation_runs"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    dataset_id: Mapped[str] = mapped_column(String(120), nullable=False)
    dataset_version: Mapped[str] = mapped_column(String(80), nullable=False)
    run_name: Mapped[str] = mapped_column(String(160), nullable=False)
    model: Mapped[str | None] = mapped_column(String(160))
    prompt_version: Mapped[str | None] = mapped_column(String(80))
    workflow_version: Mapped[str | None] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    report: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EvaluationCaseResultModel(Base):
    __tablename__ = "evaluation_case_results"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey("evaluation_runs.id", ondelete="CASCADE"), index=True, nullable=False
    )
    case_id: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    execution_mode: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    expected_result: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    actual_result: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    confirmed: Mapped[bool] = mapped_column(nullable=False)
    tool_calls: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    evidence_types: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    latency: Mapped[float] = mapped_column(nullable=False, default=0)
    token_usage: Mapped[int | None] = mapped_column()
    error: Mapped[str | None] = mapped_column(Text)
