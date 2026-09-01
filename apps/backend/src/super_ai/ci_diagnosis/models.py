"""CI diagnosis persistence models kept separate from AIOps models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from super_ai.memory.models import Base, utc_now


class CiDiagnosticTaskModel(Base):
    __tablename__ = "ci_diagnostic_tasks"
    __table_args__ = (
        Index("ix_ci_diagnostic_tasks_owner_created", "owner_user_id", "created_at"),
        Index("ix_ci_diagnostic_tasks_owner_status", "owner_user_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    tenant_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    repository_path: Mapped[str] = mapped_column(String(2048), nullable=False)
    failure_summary: Mapped[str] = mapped_column(Text, nullable=False)
    test_log: Mapped[str] = mapped_column(Text, nullable=False)
    test_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    commit_sha: Mapped[str | None] = mapped_column(String(160), nullable=True)
    base_commit_sha: Mapped[str | None] = mapped_column(String(160), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    workflow_version: Mapped[str] = mapped_column(String(80), nullable=False)
    model_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    result_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CiDiagnosticStepModel(Base):
    __tablename__ = "ci_diagnostic_steps"
    __table_args__ = (
        Index("ix_ci_diagnostic_steps_owner_task_sequence", "owner_user_id", "task_id", "sequence"),
    )

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(
        ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    node: Mapped[str] = mapped_column(String(60), nullable=False)
    action: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )


class CiDiagnosticEvidenceModel(Base):
    __tablename__ = "ci_diagnostic_evidence"
    __table_args__ = (
        Index(
            "ix_ci_diagnostic_evidence_owner_task_created", "owner_user_id", "task_id", "created_at"
        ),
        Index("ix_ci_diagnostic_evidence_owner_task_type", "owner_user_id", "task_id", "type"),
    )

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(
        ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    step_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    tool_call_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    source: Mapped[str] = mapped_column(String(1024), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )


class CiToolCallModel(Base):
    __tablename__ = "ci_tool_calls"
    __table_args__ = (
        Index("ix_ci_tool_calls_owner_task_created", "owner_user_id", "task_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(
        ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tool_name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    arguments: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    result: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    truncated: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
