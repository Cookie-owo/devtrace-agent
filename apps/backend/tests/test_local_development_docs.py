from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_root_readme_documents_local_first_startup_and_optional_compose() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "## 本地开发" in readme
    assert (
        "docker compose -f infra/compose.yaml up -d etcd minio milvus attu alertmanager"
        in readme
    )
    assert "scripts/start-local.sh" in readme
    assert "scripts\\start-local.bat" in readme
    assert "Docker Compose **只**负责" in readme
    assert "## 当前功能" in readme
    for feature in ("用户认证", "流式聊天", "知识库", "AIOps", "活跃告警", "运行状态检查"):
        assert feature in readme


def test_operations_guide_covers_local_configuration_and_real_fixture_workflows() -> None:
    guide = (REPO_ROOT / "docs" / "operations-and-monitoring.md").read_text(encoding="utf-8")

    for expected in (
        "config/project.json",
        "config/user.project.json",
        "config/project.template.json",
        "config/user.project.template.json",
        "Git 忽略",
        "apiKey",
        "secretId",
        "secretKey",
        "region",
        "logsetId",
        "topicId",
    ):
        assert expected in guide

    for forbidden in (
        "config/project.compose.json",
        "vectorStore",
        "mcp",
        "prometheusAlerts",
        "aiopsDemo",
        "minio",
    ):
        assert forbidden not in guide


def test_cross_platform_launchers_start_only_milvus_compose_dependencies() -> None:
    shell_launcher = REPO_ROOT / "scripts" / "start-local.sh"
    windows_launcher = REPO_ROOT / "scripts" / "start-local.bat"

    shell = shell_launcher.read_text(encoding="utf-8")
    windows = windows_launcher.read_text(encoding="utf-8")

    assert "up -d etcd minio milvus attu alertmanager" in shell
    assert "uvicorn super_ai.api.app:create_app" in shell
    assert "cls-mcp-server" in shell
    assert "npm run dev" in shell
    assert "</dev/null" in shell
    assert "up -d etcd minio milvus attu alertmanager" in windows
    assert "uvicorn super_ai.api.app:create_app" in windows
    assert "cls-mcp-server" in windows
    assert "npm run dev" in windows


def test_posix_launcher_has_valid_shell_syntax() -> None:
    shell_launcher = REPO_ROOT / "scripts" / "start-local.sh"

    result = subprocess.run(
        ["bash", "-n", str(shell_launcher)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_platform_installation_guides_and_log_alert_tutorial_exist() -> None:
    for guide_name, command in (
        ("macos.md", "brew install"),
        ("linux.md", "apt"),
        ("windows.md", "winget"),
    ):
        guide = (REPO_ROOT / "docs" / "setup" / guide_name).read_text(encoding="utf-8")
        assert "cls-mcp-server" in guide
        assert "scripts" in guide
        assert command in guide

    tutorial = (REPO_ROOT / "docs" / "tutorials" / "real-log-and-alert.md").read_text(
        encoding="utf-8"
    )
    for expected in (
        "generate_and_upload_cls_logs.py",
        "publish_java_ecommerce_alerts.py",
        "seed_java_ecommerce_aiops_sops.py",
        "SearchLog",
    ):
        assert expected in tutorial
