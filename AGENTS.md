# AGENTS.md

本文档面向在本仓库中工作的编码 Agent。它描述的是当前已实现的系统与约束，不是早期规划。修改前先阅读与任务相关的源码、测试、OpenSpec 主规格和文档；当它们不一致时，以可执行代码与测试为事实，并在同一变更中修正文档漂移。

## 项目概览

Agent Py 是一个本地优先的 AIOps 工作台：

- Vue 3 前端提供认证、聊天、知识库、智能诊断和 MCP 管理界面。
- FastAPI 后端负责认证、SSE、Agent、RAG、AIOps、后台任务和外部集成。
- SQLite + SQLAlchemy/Alembic 保存用户归属的业务数据和后台任务状态。
- Milvus 保存带 owner/user/tenant 元数据的知识向量。
- `langchain` `create_agent` 驱动聊天 Agent，LangGraph 驱动 AIOps Plan-Execute-Replan。
- 腾讯云官方 CLS MCP Server 提供真实日志工具；不得用 mock 日志或虚构诊断替代。

## 仓库结构

```text
apps/backend/           Python 3.10+、FastAPI、Pydantic v2、SQLAlchemy、uv、pytest
  src/super_ai/         后端业务代码（src 布局）
  alembic/              SQLite schema 迁移
  tests/                后端测试
  var/                  本地数据库与运行日志（不提交）
apps/frontend/          Vue 3、Vite、TypeScript、Pinia、Vitest
  src/                  页面、组件、stores、API/SSE clients
  tests/                前端单元和组件测试
packages/api-contracts/ 前后端共享的 TypeScript HTTP、错误码、OpenAPI、SSE 契约
config/                 可提交模板和被忽略的本地 JSON 配置
infra/                  etcd、MinIO、Milvus、Attu、Alertmanager 的 Compose 资产
scripts/                macOS/Linux 与 Windows 本机启动器、文档图生成器
openspec/               主规格、活动变更和归档
docs/                   VitePress 文档、安装指南、教程与 OpenSpec WIKI
```

不要在仓库中另建平行的后端包、前端应用或重复契约目录。后端模块必须位于 `apps/backend/src/super_ai/`，并使用 `from super_ai...` 导入，绝不能使用 `from src.super_ai...`。

## 事实来源与变更范围

- 当前功能概览和启动方式见 `README.md`。
- 行为要求见 `openspec/specs/<capability>/spec.md`。
- 正在开发的变更位于 `openspec/changes/<change-id>/`；已归档内容只用于追溯，不是编辑目标。
- 配置字段以 `config/*.template.json` 和配置加载代码为准。
- HTTP/SSE 的 TypeScript 公共类型以 `packages/api-contracts/src/` 为准。
- 不要顺手重构无关代码，不要覆盖用户已有改动，不要提交缓存、构建产物、本地数据库或凭据。

## 常用命令

除特别说明外，从仓库根目录执行：

```bash
# 安装 Node workspace 依赖
npm install

# 前端
npm run frontend:dev
npm run frontend:typecheck
npm run frontend:test
npm run frontend:build

# 共享契约
npm run contracts:typecheck
npm --workspace packages/api-contracts run test

# 文档
npm run docs:dev
npm run docs:build

# OpenSpec
openspec validate --all

# 本地基础设施
docker compose -f infra/compose.yaml up -d etcd minio milvus attu alertmanager
docker compose -f infra/compose.yaml down

# 完整本机启动（基础设施 + 迁移 + CLS MCP + 后端 + 前端）
./scripts/start-local.sh
```

后端命令在 `apps/backend/` 中执行：

```bash
uv sync
uv run alembic upgrade head
uv run ruff check .
uv run pyright
uv run pytest
uv run uvicorn super_ai.api.app:create_app --factory --host 127.0.0.1 --port 8000
```

Windows 使用 `scripts\start-local.bat`。不要引入 Poetry、PDM、pip-tools、第二套 Node 包管理器或一次性 shell 脚本来绕过现有工作流。

## 后端约定

- Python 必须有完整类型注解，并通过 Ruff 与 strict Pyright；目标版本为 Python 3.10。
- 业务层依赖 Protocol、Repository 或显式注入的服务，不要把 SQLite、Milvus、LLM、MCP 的具体实现散落到领域代码。
- 模块导入不得建立数据库、Milvus、网络、LLM 或 MCP 连接。外部资源应在 FastAPI lifespan、依赖提供者、惰性工厂或显式初始化路径中创建。
- SQLite schema 变更必须新增 Alembic revision；不要只修改 ORM/model，也不要改写已经发布的迁移来伪造新状态。
- API 保持统一成功/错误 envelope 和错误目录；不要在新路由中发明另一种响应格式。
- 长任务使用现有 durable background job runtime，保留任务、事件、租约、重试、超时和取消语义；不要用请求内裸 `asyncio.create_task()` 代替持久任务。
- 聊天流和诊断流保持现有 SSE 事件契约、顺序、终止和错误语义。任何事件字段变更都必须同步共享契约、前端解析器和合同测试。
- LLM 仅使用 `langchain-openai` 的 OpenAI-compatible Qwen/Bailian 配置。聊天沿用 `langchain` `create_agent`，AIOps 图沿用 LangGraph；替换核心编排方式必须先形成明确设计。
- 知识检索沿用 Milvus 向量召回、BM25L、RRF 和 rerank 的现有管线。不要删除可解释排名字段，不能在无命中时伪造引用。
- MCP 必须调用用户启用的真实连接与真实工具，遵守超时、重试、同名工具保护和审计要求。

## 前端与共享契约约定

- TypeScript 保持 `strict`、`exactOptionalPropertyTypes` 和 `noUncheckedIndexedAccess` 兼容；避免 `any`，优先使用共享类型和显式类型守卫。
- Vue 使用 Composition API 与 Pinia 的现有组织方式。网络访问集中在 typed API/SSE client，页面组件不要直接拼接后端协议。
- 新增或修改 API、错误码、OpenAPI 描述或 SSE 事件时，先更新 `packages/api-contracts`，再同步后端和前端，并补充契约测试。
- 认证 token、统一错误转换、全局反馈、loading/empty/error 状态应复用现有 client、store 和 UI 组件。
- 界面默认中文，技术名词可保留英文。当前前端同时支持桌面和响应式窄屏布局；修改布局时必须保留两者，并尊重 `prefers-reduced-motion`。
- 不使用伪数据掩盖缺失的后端能力。涉及 CLS、告警、诊断证据、知识引用的展示必须来自真实 API 数据。

## 配置与凭据

应用配置只从以下本地 JSON 文件加载，不从 `.env` 或机器环境变量读取项目配置：

```text
config/project.json
config/user.project.json
```

首次运行从模板复制：

```bash
cp config/project.template.json config/project.json
cp config/user.project.template.json config/user.project.json
```

必须遵守：

- `project.json` 和 `user.project.json` 被 Git 忽略，绝不能提交。
- 仓库只提交 `*.template.json`，其中密钥、CLS 凭据、日志集/主题 ID 和演示密码必须为空。
- 新增配置字段时同步基础模板、用户覆盖模板（如适用）、加载/校验逻辑、前端类型（如适用）和运维文档。
- 不打印、记录、测试固化或在错误响应中暴露 API key、token、密码和云凭据。
- 启动脚本可把本地 JSON 中的 CLS 凭据传给官方 CLI 进程，但应用代码不得改为读取环境变量作为配置源。

## 数据安全与权限边界

- 密码必须继续使用 Argon2 哈希；认证 token 只持久化不可逆哈希，支持注册、登录、状态恢复和注销撤销。
- 所有聊天、消息、Prompt、Skill、知识库、文档、索引任务、向量、MCP 连接、AIOps 任务、证据、报告、案例、反馈和工具审计访问都必须按当前用户作用域过滤。
- 不接受仅由客户端提交的 `ownerUserId`、`tenantId` 作为授权依据；身份必须来自已认证上下文。
- Milvus 写入和检索必须包含并过滤 `ownerUserId`、`tenantId`、`knowledgeBaseId`、`documentId` 等现有作用域字段。
- 删除数据库记录时同步处理关联向量、任务或审计生命周期；跨存储操作要有可恢复、可重试或明确失败语义。
- 日志、SSE 事件、工具结果摘要和错误信息必须继续脱敏。

## 测试与验证

变更必须使用与风险相称的最小测试集，并在交付时说明实际运行过的命令。

- 后端行为：在 `apps/backend` 运行目标 pytest；提交前通常再运行 `uv run ruff check .`、`uv run pyright`、`uv run pytest`。
- 前端行为：运行相关 Vitest；提交前通常再运行 `npm run frontend:typecheck`、`npm run frontend:test`、`npm run frontend:build`。
- 共享契约：运行 `npm run contracts:typecheck` 和 package 测试。
- 文档或 VitePress 导航：运行 `npm run docs:build`。
- OpenSpec：运行 `openspec validate --all`。
- Compose 或启动流程：至少运行配置检查；能使用本机依赖时再做实际启动/健康检查。

以下修改必须补测试：权限边界、Repository、迁移、API envelope、错误码、SSE 格式与终止行为、后台任务恢复/重试/取消、向量过滤、MCP 审计、前端 store/client 状态转换和关键响应式布局。不要删除测试、放宽断言、关闭 strict 检查或加入无条件 skip 来让构建通过。

## OpenSpec 与 WIKI

- 新功能、用户可见行为变化、API/数据模型调整或跨模块重构，应先创建一个聚焦的 OpenSpec change，再实现其中 tasks。
- 纯拼写修复、说明性文档同步或不改变行为的机械维护可直接修改，但不得借此绕过实际规格变化。
- proposal、design、tasks、delta spec 和相关 WIKI 默认使用简体中文；规范关键标题（如 `Requirement`、`Scenario`）、API 路径、标识符和协议名保留原格式。
- 每项需求必须有可验证的 `Scenario`，tasks 中必须包含测试或验证步骤。
- 创建或归档 change 后，使用仓库的 `wiki-sync` 流程同步 `docs/changes/`，并确保 VitePress 可构建。
- 完成实现后，先核对 tasks、运行验证并确认主规格一致，再归档；不要把未完成 change 标记为完成。

## 文档与 Git

- 代码、配置、README、`docs/`、OpenSpec 和架构图必须表达同一个现状；改变命令、端口、配置字段、路由或架构边界时同步相关文档。
- 不手工编辑生成的 VitePress `docs/.vitepress/dist/`、缓存、前端 `dist/`、`node_modules/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/` 或 `apps/backend/var/`。
- 提交遵循 Conventional Commits，例如 `feat: add ...`、`fix: correct ...`、`test: cover ...`、`docs: update ...`、`chore: ...`。
- PR/交付说明应包含目的、关联 OpenSpec change、验证命令；有可见 UI 变化时附桌面截图，并在响应式布局受影响时补窄屏截图。

## Agent 工作原则

- 先检索再修改：优先使用 `rg`/`rg --files`，确认调用方、测试和文档后再动手。
- 诊断任务只报告根因和证据；用户明确要求修复时才实施。
- 实现任务应完成代码、测试和必要文档，不停在建议或半成品。
- 保留工作区中不属于当前任务的改动；遇到冲突先缩小修改范围，无法安全处理时再请求用户决定。
- 不执行破坏性 Git 操作，不删除用户数据，不上传真实日志/凭据，不调用会产生外部影响的服务，除非用户明确授权且目标清晰。
