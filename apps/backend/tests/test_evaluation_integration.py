from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from super_ai.ci_diagnosis.repository import SQLiteCiDiagnosticRepository
from super_ai.evaluation.dataset import load_builtin_dataset
from super_ai.evaluation.executor import EvaluationWorkflowExecutor
from super_ai.evaluation.metrics import aggregate_results, evaluate_case
from super_ai.evaluation.repository import EvaluationRepository
from super_ai.memory.database import create_memory_engine, create_memory_session_factory


@pytest.fixture
def migrated_database_url(tmp_path: Path) -> str:
    database = tmp_path / "evaluation.sqlite3"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{database}")
    command.upgrade(config, "head")
    return f"sqlite+aiosqlite:///{database}"


@pytest.mark.asyncio
async def test_real_workflow_evaluation_two_runs(
    migrated_database_url: str, tmp_path: Path
) -> None:
    engine = create_memory_engine(migrated_database_url)
    try:
        factory = create_memory_session_factory(engine)
        evaluation = EvaluationRepository(factory)
        ci = SQLiteCiDiagnosticRepository(factory)
        executor = EvaluationWorkflowExecutor(ci, tmp_path)
        cases = load_builtin_dataset()
        for suffix in ("baseline", "candidate"):
            run_id = f"eval-{suffix}"
            await evaluation.create_run(
                run_id=run_id,
                dataset_id="builtin",
                dataset_version="builtin-v1",
                run_name=run_id,
                model="deterministic",
                prompt_version=suffix,
                workflow_version="ci-v1",
            )
            results: list[dict[str, object]] = []
            for case in cases:
                trace = await executor.execute(case)
                result = evaluate_case(case, trace)
                results.append(result)
                await evaluation.add_case(
                    id=f"{run_id}-{case.case_id}", run_id=run_id, case_id=case.case_id,
                    category=case.category, execution_mode="controlled_fixture", status="completed",
                    expected_result={
                        "rootCause": case.expected_root_cause,
                        "confirmed": case.should_confirm,
                    },
                    actual_result=trace.get("report", {}),
                    confirmed=bool(trace.get("report", {}).get("confirmed")),
                    tool_calls=trace.get("tool_calls", []),
                    evidence_types=[e.get("type") for e in trace.get("evidence", [])],
                    metrics=result, latency=0, token_usage=None, error=None,
                )
            metrics = aggregate_results(cases, results)
            await evaluation.update_run(
                run_id,
                status="completed",
                metrics=metrics.as_dict(),
                report={"metrics": metrics.as_dict()},
            )
        assert len(await evaluation.list_cases("eval-baseline")) == 20
        assert len(await evaluation.list_cases("eval-candidate")) == 20
        baseline = await evaluation.get_run("eval-baseline")
        assert baseline is not None and baseline.status == "completed"
    finally:
        await engine.dispose()
