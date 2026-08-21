# Agent Py

Agent Py 是一个本地优先的 AIOps 工作台。Vue 3 提供操作界面，FastAPI 提供 API 与 Agent 运行时，SQLite 保存用户归属的数据，Milvus 保存受权限控制的知识向量，腾讯云官方 CLS MCP Server 提供真实日志访问。

## 当前功能

以下能力均已在当前代码中实现，不包含尚未落地的规划项。

### 账号、权限与工作台

- **用户认证**：支持注册、登录、登出、认证状态恢复和当前用户信息查询；密码使用 Argon2 安全哈希，不保存明文。
- **用户与 tenant 隔离**：聊天、消息、知识库、文档、向量、索引任务、MCP 连接、AIOps、证据、报告、反馈和工具审计均按当前用户隔离，越权访问返回统一权限错误。
- **中文响应式工作台**：提供对话、知识库、智能诊断和 MCP 连接四个受保护路由，桌面与移动端共用一致导航和状态表达。
- **统一操作反馈**：成功、提示和错误消息使用全局反馈组件展示，支持手动关闭并在 3 秒后自动消失。

### 流式聊天与 Agent

- **持久化会话**：支持创建、切换、倒序查询、自动生成标题、清空和删除会话；SQLite 是会话与消息的主存储。
- **流式聊天**：使用 `langchain` `create_agent`、OpenAI-compatible Qwen 和 SSE 输出内容增量、工具调用、引用、完成与错误事件，前端以可感知的打字机节奏渲染回答。
- **自主工具调用**：模型根据问题自行决定是否调用知识库、当前时间或已启用 MCP 工具，不把 RAG 固定为每次对话的前置流程。
- **Prompt 配置**：用户可以创建、编辑、选择和删除会话使用的系统 Prompt，服务端负责组装最终 system prompt。
- **渐进式 Skill**：支持上传和选择符合 `SKILL.md` 规范的 Skill；初始上下文只注入 `name` 与 `description`，模型需要时再通过 `load_skill` 加载正文。
- **会话级记忆模式**：每个会话可独立选择“每 30 轮压缩”“上下文占用 70% 自动压缩”或“手动压缩”，输入框旁展示上下文窗口占用率；压缩只生成摘要，不删除完整历史。
- **推理与工具过程**：回答可折叠展示推理上下文、工具调用状态和结果摘要，工具调用同时写入 SQLite 审计记录。
- **内容反馈**：用户可对助手回答和单条知识引用点赞、点踩，填写问题类型、评论和纠正内容；反馈可更新、删除并在重新打开会话后恢复。

### 知识库、索引与 RAG

- **文档管理**：支持上传 Markdown 和 PDF，记录文件名、大小、MIME、SHA-256、上传时间与索引状态；支持重复文件检测、明确覆盖和删除时同步清理向量。
- **切分策略与预览**：上传前可选择固定字符、Markdown 标题或段落切分；固定字符支持长度和重叠参数，前端可预览有界 chunk 结果。
- **持久索引任务**：文档索引在后台执行，状态包含排队、执行中、成功、失败和取消；失败原因会持久化，并支持手动重试和重建索引。
- **Embedding 与 Milvus**：调用配置的 Embedding 模型生成向量，写入 Milvus HNSW/COSINE collection；chunk metadata 包含文档、来源、切分参数和 owner/user/tenant 权限字段。
- **混合召回与精排**：Milvus 向量搜索与内存 BM25L 关键词检索并行召回，通过 RRF（`k=60`）融合候选，再调用 Qwen rerank 模型精排。
- **完整检索可解释性**：引用同时展示向量排名与相似度、BM25 排名与分数、RRF 分数、rerank 排名与分数，以及文档来源、chunk 摘要和 metadata。
- **受控知识工具**：知识检索以 LangChain Tool 提供给 Agent，支持 `topK` 和知识库过滤；检索始终附带当前用户权限条件，无命中时返回空结果而不是编造内容。

### AIOps 智能诊断

- **Plan-Execute-Replan**：使用 LangGraph 实现 `Planner -> Executor -> Replanner -> Report`，Planner 先检索 SOP，Executor 调用真实工具，Replanner 决定继续、调整或生成报告。
- **真实告警入口**：聚合 Prometheus v1 和 Alertmanager v2 活跃告警，用户可刷新告警并从某条告警直接创建诊断任务。
- **持久后台执行**：诊断由 SQLite durable job runtime 调度，不阻塞 API；页面展示排队、执行、取消、失败和完成状态，并支持用户取消任务。
- **诊断 SSE**：实时输出计划、步骤、工具调用、证据、重规划、报告、完成和错误事件；断开后可根据持久化事件和任务数据恢复。
- **证据链与报告**：持久化原始输入、计划、执行步骤、工具调用、日志/指标/告警/知识引用证据、checkpoint 和 Markdown 报告，报告结论可追溯到证据。
- **诊断历史与案例库**：支持按用户查询历史任务和完整证据链；成功诊断可自动或手动沉淀为用户知识库中的故障案例并参与后续检索。
- **诊断反馈**：用户可对单个诊断步骤和最终报告提交可恢复的结构化反馈。

### MCP 与外部系统

- **真实 CLS MCP**：本机运行腾讯云官方 `cls-mcp-server`，后端通过 SSE 调用真实 CLS 日志、告警、指标和辅助工具，不提供 mock profile 或伪造结果。
- **用户级 MCP 连接管理**：前端支持创建、编辑、启停和删除多个 MCP Server，配置 SSE 或 Streamable HTTP、URL、超时和重试次数。
- **连接检查与工具发现**：可从页面检查 MCP Server，展示真实连接结果和工具列表；聊天与 AIOps 共用同一份当前用户连接配置。
- **调用治理**：MCP 支持超时、重试、同名工具保护和明确失败；每次调用记录工具名、参数、结果摘要、耗时、状态、错误及关联会话或诊断任务。

### 后台任务、存储与平台能力

- **Durable job runtime**：SQLite 保存后台任务、事件、尝试次数和租约；Worker 支持并发领取、心跳续租、进程重启恢复、指数退避重试、超时和协作式取消。
- **Repository 存储边界**：SQLAlchemy 模型和 Repository 隔离业务层与 SQLite 细节，Alembic 管理迁移，并为后续替换 PostgreSQL 保留边界。
- **统一 API 契约**：`packages/api-contracts` 是前后端共享的 HTTP、错误码、OpenAPI 和 SSE 类型来源，覆盖认证、聊天、知识库、后台任务、反馈、MCP 和 AIOps。
- **运行状态检查与指标**：`/health` 检查存活，`/ready` 检查 SQLite、Milvus、Qwen 与 MCP，`/config/check` 校验项目配置，`/metrics` 暴露本地请求指标。
- **结构化可观测性**：请求日志包含 request id、路径、状态和耗时；敏感字段统一脱敏，Agent/MCP 工具调用有独立审计生命周期。
- **真实演示数据工具**：提供显式脚本上传 Java 电商事故 CLS 日志、发布本地告警和索引 SOP，可完成“告警 -> 诊断 -> 证据 -> 报告 -> 案例知识”的完整演示。
- **本地优先启动**：Docker Compose 仅托管 etcd、MinIO、Milvus、Attu 和 Alertmanager；前端、后端与 CLS MCP Server 使用 macOS/Linux/Windows 本机启动脚本运行。

## 前端入口

| 路径 | 功能 |
|------|------|
| `/login`、`/register` | 登录与注册 |
| `/chat` | 会话、流式 Agent、Prompt、Skill、记忆模式、引用和反馈 |
| `/knowledge` | 文档上传、切分预览、索引、重试、详情和删除 |
| `/aiops` | 活跃告警、实时诊断、执行链、证据、报告和案例库 |
| `/mcp` | MCP 连接配置、启停、检查与工具发现 |

## 项目结构

```text
apps/backend/          FastAPI、LangChain/LangGraph、SQLite、Alembic、uv
apps/frontend/         Vue 3、Vite、TypeScript
packages/api-contracts 共享的 TypeScript HTTP 与 SSE 契约
config/                可提交的配置模板与被 Git 忽略的本地 JSON 配置
infra/                 Milvus 与 Alertmanager 基础设施 Compose 资产
scripts/               本机启动脚本
openspec/              OpenSpec 规格、变更与归档
docs/                  安装、架构与运维文档
```

## 三平台安装

请先按当前操作系统完成完整依赖安装：

- [macOS 安装指南](docs/setup/macos.md)
- [Linux 安装指南](docs/setup/linux.md)
- [Windows 安装指南](docs/setup/windows.md)

三个指南均覆盖 Git、Docker、Node/npm、uv 与官方 `cls-mcp-server`。

## 配置方式

应用只从本地 JSON 配置文件读取项目配置，不读取本机 `.env` 文件或环境变量。首次使用时，从不含密钥的模板创建本地配置：

```bash
cp config/project.template.json config/project.json
cp config/user.project.template.json config/user.project.json
```

- `config/project.json`：基础运行配置，仅保存在本机。
- `config/user.project.json`：个人模型与 CLS 配置，仅保存在本机并覆盖基础配置。
- `config/project.template.json`、`config/user.project.template.json`：可安全提交的配置模板。

两个本地配置文件均被 Git 忽略。请阅读[配置与运维教程](docs/operations-and-monitoring.md)填写模型密钥、CLS 凭据与其他本机配置，禁止将真实凭据加入版本控制。

## 本地开发

Docker Compose **只**负责运行 etcd、MinIO、Milvus、Attu 和 Alertmanager。CLS MCP Server、后端与前端均直接在本机运行，不会通过 Compose 启动。

### 一键启动

在仓库根目录执行：

```bash
./scripts/start-local.sh
```

在 Windows 命令提示符中执行：

```text
scripts\start-local.bat
```

启动脚本会启动基础设施容器、准备项目依赖、执行 SQLite 迁移，并在本机启动 MCP、后端和前端。进程日志写入 `apps/backend/var/`。

### 手动启动

安装前端和后端依赖：

```bash
npm install
cd apps/backend
uv sync
mkdir -p var
uv run alembic upgrade head
```

在仓库根目录启动所有容器基础设施：

```bash
docker compose -f infra/compose.yaml up -d etcd minio milvus attu alertmanager
```

使用 `config/project.json` 中 `clsMcpServer` 的配置启动官方 CLS MCP Server，然后启动后端：

```bash
cd apps/backend
uv run uvicorn super_ai.api.app:create_app --factory --host 127.0.0.1 --port 8000
```

在第二个终端启动前端：

```bash
cd apps/frontend
npm run dev -- --host 127.0.0.1
```

本地地址：

- 前端：`http://127.0.0.1:5173`
- 后端：`http://127.0.0.1:8000`
- 后端就绪检查：`http://127.0.0.1:8000/ready`
- CLS MCP SSE：`http://127.0.0.1:3000/sse`
- Alertmanager：`http://127.0.0.1:9093`
- Milvus：`http://127.0.0.1:19530`
- Attu：`http://127.0.0.1:8001`

## 真实日志与告警教程

上传 CLS 日志、发布本地 Alertmanager 告警、索引 SOP 与从前端执行 AIOps 诊断均为显式操作，不属于日常启动流程。请按照[真实日志与告警教程](docs/tutorials/real-log-and-alert.md)执行。

## 验证命令

在仓库根目录执行 OpenSpec 验证：

```bash
openspec validate --all
```

在 `apps/backend` 执行后端检查：

```bash
uv run ruff check .
uv run pyright
uv run pytest
```

在 `apps/frontend` 执行前端检查：

```bash
npm run typecheck
npm run test
npm run build
```
