from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "202608220002"
down_revision = "202608220001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "evaluation_runs",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("dataset_id", sa.String(120), nullable=False),
        sa.Column("dataset_version", sa.String(80), nullable=False),
        sa.Column("run_name", sa.String(160), nullable=False),
        sa.Column("model", sa.String(160)),
        sa.Column("prompt_version", sa.String(80)),
        sa.Column("workflow_version", sa.String(80)),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("report", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "evaluation_case_results",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column(
            "run_id",
            sa.String(80),
            sa.ForeignKey("evaluation_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("case_id", sa.String(120), nullable=False),
        sa.Column("category", sa.String(60), nullable=False),
        sa.Column("execution_mode", sa.String(40), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("expected_result", sa.JSON(), nullable=False),
        sa.Column("actual_result", sa.JSON(), nullable=False),
        sa.Column("confirmed", sa.Boolean(), nullable=False),
        sa.Column("tool_calls", sa.JSON(), nullable=False),
        sa.Column("evidence_types", sa.JSON(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("latency", sa.Float(), nullable=False),
        sa.Column("token_usage", sa.Integer()),
        sa.Column("error", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("evaluation_case_results")
    op.drop_table("evaluation_runs")
