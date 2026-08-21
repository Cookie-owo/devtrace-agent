## 1. 运行时清理

- [x] 1.1 更新 Compose 基础设施测试，断言 `infra/app.Dockerfile` 和 `config/project.compose.json` 不存在，并删除旧应用镜像内容断言。
- [x] 1.2 先运行 `cd apps/backend && uv run pytest tests/test_infra_compose.py -q`，确认新增的运行时边界测试在旧资产仍存在时失败。
- [x] 1.3 删除 `config/project.compose.json`、`infra/app.Dockerfile` 和 `apps/backend/src/super_ai/api/app.py` 中的 `create_compose_app()`；保留其他仍需要的导入和 `create_app()` 路径。
- [x] 1.4 再次运行 `cd apps/backend && uv run pytest tests/test_infra_compose.py -q`，确认 Compose 仅基础设施边界通过。

## 2. 文档与规格统一

- [x] 2.1 更新本地开发文档测试：断言 `docs/operations-and-monitoring.md` 的接收方“需要替换”清单精确包含 `llm.apiKey`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId`，且不把 MCP、Milvus、MinIO、Prometheus/Alertmanager 来源、应用地址、Docker 字段或演示账户设置列为需修改项。
- [x] 2.2 先运行 `cd apps/backend && uv run pytest tests/test_local_development_docs.py -q`，确认新增文档边界测试在现有指南仍列出额外需修改项时失败。
- [x] 2.3 更新根 README、`infra/README.md` 和 `docs/operations-and-monitoring.md`，删除 Compose 应用运行时及 `project.compose.json` 表述；其中运维指南的接收方替换清单只能列出六个允许字段。
- [x] 2.4 更新主 OpenSpec 规格：将 `docker-compose-startup` 的 Purpose 改为准确说明 Compose 仅管理 etcd、MinIO、Milvus、Attu 和 Alertmanager，后端、前端和官方 CLS MCP Server 在主机上运行；移除 `Application image` 要求，并将运维配置引用收敛为 `config/project.json`。
- [x] 2.5 再次运行 `cd apps/backend && uv run pytest tests/test_local_development_docs.py -q`，确认文档边界通过。
- [x] 2.6 运行 `rg -n -i --hidden --glob '!.git/**' --glob '!apps/**/tests/**' --glob '!docs/superpowers/**' --glob '!openspec/changes/archive/**' --glob '!openspec/changes/remove-compose-runtime-config/**' 'project\.compose\.json|create_compose_app|app\.Dockerfile' README.md apps/backend/src apps/frontend/src scripts config infra docs openspec/specs`，只检索运行时源代码、配置、基础设施、面向用户的文档和主规格；排除测试、内部规划文档及活跃/归档 OpenSpec 变更。确认最终运行时与文档表面无死引用；预期无输出（`rg` exit code 1）。

## 3. 验证与完成

- [x] 3.1 运行 `openspec validate remove-compose-runtime-config --strict`，确认变更制品和 delta spec 有效。
- [x] 3.2 运行 `openspec validate --all`，确认全部 OpenSpec 规格有效。
- [x] 3.3 运行 `cd apps/backend && uv run pytest && uv run ruff check . && uv run pyright`，确认完整后端质量检查通过。
- [x] 3.4 运行 `git diff --check`，并记录验证结果后再归档该变更。
