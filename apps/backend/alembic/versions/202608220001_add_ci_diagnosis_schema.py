"""add CI diagnosis domain persistence

Revision ID: 202608220001
Revises: 202607110007
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "202608220001"
down_revision: str | None = "202607110007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ci_diagnostic_tasks",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("owner_user_id", sa.String(80), nullable=False),
        sa.Column("tenant_id", sa.String(80), nullable=True),
        sa.Column("repository_path", sa.String(2048), nullable=False),
        sa.Column("failure_summary", sa.Text(), nullable=False),
        sa.Column("test_log", sa.Text(), nullable=False),
        sa.Column("test_name", sa.String(512), nullable=True),
        sa.Column("commit_sha", sa.String(160), nullable=True),
        sa.Column("base_commit_sha", sa.String(160), nullable=True),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("workflow_version", sa.String(80), nullable=False),
        sa.Column("model_name", sa.String(160), nullable=True),
        sa.Column("prompt_version", sa.String(80), nullable=True),
        sa.Column("result_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_ci_diagnostic_tasks_owner_user_id", "ci_diagnostic_tasks", ["owner_user_id"]
    )
    op.create_index(
        "ix_ci_diagnostic_tasks_owner_created",
        "ci_diagnostic_tasks",
        ["owner_user_id", "created_at"],
    )
    op.create_index(
        "ix_ci_diagnostic_tasks_owner_status", "ci_diagnostic_tasks", ["owner_user_id", "status"]
    )

    op.create_table(
        "ci_diagnostic_steps",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("owner_user_id", sa.String(80), nullable=False),
        sa.Column(
            "task_id",
            sa.String(80),
            sa.ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("node", sa.String(60), nullable=False),
        sa.Column("action", sa.String(160), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_ci_diagnostic_steps_owner_user_id", "ci_diagnostic_steps", ["owner_user_id"]
    )
    op.create_index("ix_ci_diagnostic_steps_task_id", "ci_diagnostic_steps", ["task_id"])
    op.create_index(
        "ix_ci_diagnostic_steps_owner_task_sequence",
        "ci_diagnostic_steps",
        ["owner_user_id", "task_id", "sequence"],
    )

    op.create_table(
        "ci_diagnostic_evidence",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("owner_user_id", sa.String(80), nullable=False),
        sa.Column(
            "task_id",
            sa.String(80),
            sa.ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("step_id", sa.String(80), nullable=True),
        sa.Column("tool_call_id", sa.String(80), nullable=True),
        sa.Column("type", sa.String(40), nullable=False),
        sa.Column("source", sa.String(1024), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_ci_diagnostic_evidence_owner_user_id", "ci_diagnostic_evidence", ["owner_user_id"]
    )
    op.create_index("ix_ci_diagnostic_evidence_task_id", "ci_diagnostic_evidence", ["task_id"])
    op.create_index(
        "ix_ci_diagnostic_evidence_owner_task_created",
        "ci_diagnostic_evidence",
        ["owner_user_id", "task_id", "created_at"],
    )
    op.create_index(
        "ix_ci_diagnostic_evidence_owner_task_type",
        "ci_diagnostic_evidence",
        ["owner_user_id", "task_id", "type"],
    )

    op.create_table(
        "ci_tool_calls",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("owner_user_id", sa.String(80), nullable=False),
        sa.Column(
            "task_id",
            sa.String(80),
            sa.ForeignKey("ci_diagnostic_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("tool_name", sa.String(120), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("arguments", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("truncated", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ci_tool_calls_owner_user_id", "ci_tool_calls", ["owner_user_id"])
    op.create_index("ix_ci_tool_calls_task_id", "ci_tool_calls", ["task_id"])
    op.create_index(
        "ix_ci_tool_calls_owner_task_created",
        "ci_tool_calls",
        ["owner_user_id", "task_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_table("ci_tool_calls")
    op.drop_table("ci_diagnostic_evidence")
    op.drop_table("ci_diagnostic_steps")
    op.drop_table("ci_diagnostic_tasks")
