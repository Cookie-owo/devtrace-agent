# OpenSpec 从 0 到 1 项目实战提示词

> 目标：在一个空仓库中，按本文第 01 个提案开始逐段复制提示词，使用 OpenSpec skills 完成“提案 → 实现 → 验证 → 归档”，最终复刻本仓库当前的本地优先 AIOps 工作台。
>
> 本文不是 65 个历史归档 change 的机械重放。历史中已经被推翻的方案会被裁剪，修复类、重构类和 UI polish 类 change 会直接吸收到对应功能的最终态提案中。

## 一、最终要得到什么

最终项目是一个中文、本地优先、以桌面 Web 为验收目标的 AI/AIOps 工作台：

- Vue 3 工作台提供认证、对话、知识库、AIOps 和 MCP 连接页面。
- FastAPI 提供统一 HTTP/SSE API、LangChain Agent 运行时和 LangGraph AIOps 诊断图。
- SQLite + SQLAlchemy + Alembic 保存认证、聊天、文档、任务、MCP、AIOps、反馈和审计数据。
- Milvus 保存带 owner/tenant 元数据的知识向量；关键词检索使用 BM25L，候选经 RRF 和 Qwen rerank。
- OpenAI-compatible Qwen/Bailian 通过 `langchain-openai` 的 `ChatOpenAI`/`OpenAIEmbeddings` 接入。
- 腾讯云官方 CLS MCP Server 提供真实日志工具；Prometheus v1/Alertmanager v2 提供真实告警入口。
- 所有业务数据按当前 user 隔离；不提交真实配置、模型密钥或 CLS 凭据。
- OpenSpec proposal、design、tasks、delta spec、归档和 WIKI 形成完整可追溯链路。

## 二、历史冲突的裁决规则

阅读或执行本文时，以以下优先级判断冲突：

1. 当前可运行代码、当前测试和仓库 `AGENTS.md`。
2. 当前配置模板、基础设施文件和根 README。
3. 当前 `openspec/specs/` 主规格。
4. 较新的 archive change。
5. 已被后续 change 推翻的早期 archive 只作为历史背景。

必须直接采用下表中的最终态，不要先实现旧方案再撤销：

| 冲突主题 | 最终态裁决 |
|---|---|
| 项目配置 | 只提交无密钥的 `config/project.template.json`、`config/user.project.template.json`；本机 `project.json` 和 `user.project.json` 均被 Git 忽略并深合并。后端可读取完整配置；Vite 只能把 `frontend` 公共 allowlist 注入浏览器，禁止直接 import 含 LLM/CLS secret 的完整 JSON。应用不从 OS 环境变量读取项目配置。 |
| Docker Compose | Compose 只运行 etcd、MinIO、Milvus、Attu、Alertmanager；FastAPI、Vite、官方 CLS MCP Server 在主机运行。不创建应用 Dockerfile、`project.compose.json` 或 Compose 应用工厂。 |
| 后台任务 | 文档索引和 AIOps 都使用 SQLite durable job、事件、lease、heartbeat、重试和取消；不能依赖客户端 SSE 连接持续存在，也不使用临时 `asyncio.create_task` 作为最终运行时。 |
| Prompt/Skill | Prompt 和 Skill 是 user-owned 资产。Skill 使用标准 `<skill-name>/SKILL.md` 与 YAML frontmatter；初始 system prompt 只注入 `name`/`description`，正文由 `load_skill` 按需加载。 |
| 知识文档 | 最终只接受 `.md` 和 `.pdf`，最大 10 MiB；使用 `pypdf` 和 `langchain-text-splitters`。只有 fixed-character 策略接收长度和 overlap。 |
| 检索 | owner/tenant 过滤后，向量与 BM25L 并行召回，RRF `k=60` 融合不超过 20 个候选，再由真实 Qwen rerank 输出最多 5 条；保留所有阶段 rank/score，失败必须显式。 |
| Readiness | `/health` 只做进程存活检查；`/ready` 检查 SQLite、Milvus、Qwen、MCP；`/config/check` 输出脱敏 configuration 诊断并同时报告同组真实 dependencies，配置或依赖失败均为 503。 |
| AIOps 案例 | 手动“保存为知识”保留为 legacy 补充；有成功最终报告的诊断自动生成结构化案例并索引，case 保存当时可用的 evidence IDs（允许为空），失败诊断绝不生成案例。 |
| 前端形态 | 以桌面 Web 为验收目标。可以避免窄视口溢出，但不新增移动专用抽屉、底栏或替代业务流程。 |
| Chat 流 | 后端把最终正文拆为单字符 `content.delta`；reasoning、tool、reference 等事件不拆。前端用 `setTimeout` 约每 28 ms 顺序消费正文，每轮引用严格隔离。 |
| MCP/真实数据 | 工具来自当前 user 启用的 MCP connections，支持 SSE/Streamable HTTP。禁止 runtime fake profile、假日志、假工具结果和伪 AIOps 结论。fixture 只能由显式脚本触发。 |
| 可观测性 | 日志只记录关联 ID、状态、错误分类、耗时、工具名和参数键；token、key、query、prompt、工具参数值/输出、用户正文必须不记录或递归脱敏。 |
| Git 历史 | 从零项目不执行 `filter-repo` 或 force push。第一提案就建立 ignore、模板和 secret 检查；发现泄露时停止并轮换凭据，另行处理历史。 |
| 模型接入 | 只使用 `langchain-openai` 的 OpenAI-compatible `ChatOpenAI`/`OpenAIEmbeddings`；不使用 DashScope SDK。Embedding 维度 1024，原始字符串输入，单批最多 10 条；rerank 使用独立 HTTP client。 |

## 三、执行准备

先准备 Git、Python >=3.10、uv、Node.js 20 LTS 或更新的兼容版本、npm、Docker Desktop/Engine + Compose v2，以及 OpenSpec CLI `1.5.0`；P01 会立即使用 Python/uv/Node/npm，P07 会使用 Docker。CLI 未安装时先执行 `npm install -g @fission-ai/openspec@1.5.0`。必须先检查版本，再在空目录初始化 Git/OpenSpec，避免旧 CLI 生成不兼容脚手架。

macOS/Linux（Windows 使用 Git Bash 时也可采用）preflight：

```bash
git --version
python3 --version
uv --version
node --version
npm --version
docker --version
docker compose version
openspec --version
git init
openspec init --tools codex .
```

Windows PowerShell preflight 使用 `py -3`/`python`，不假设存在 `python3` 或 Bash：

```powershell
git --version
py -3 --version
uv --version
node --version
npm --version
docker --version
docker compose version
openspec --version
git init
openspec init --tools codex .
```

确认 Codex 中可以使用以下 skills：

- `$openspec-propose`
- `$openspec-apply-change`
- `$openspec-verify-change`
- `$openspec-archive-change`

执行约定：

1. 严格按 P01 → P27 顺序，一次只复制一个提案提示词。
2. 上一个 change 必须实现、验证并归档后，才能开始下一个。
3. 每个代码块都已经包含完整生命周期要求；不要只创建 artifacts 就停止。archive 阶段通常会要求一次 delta spec 同步确认，选择 `Sync now`，这不是异常阻塞。
4. 所有 OpenSpec Markdown 默认使用简体中文；函数名、API 路径、协议名和规范关键标题可保留英文。
5. 每个 change 都必须先写 delta specs；只有涉及 API、SSE 或跨端 DTO 的 change 才先扩展共享 contracts，再实现后端/前端。
6. 测试可以 fake 外部 provider 边界，但产品运行时和真实验收不能用 mock CLS/MCP/日志/结论代替。
7. 遇到用户或其他会话的无关改动时保留并忽略，不得覆盖、回滚或顺手整理。
8. P27 之前仓库若尚无 `wiki-sync`，不把 WIKI 同步作为阻塞项；P27 会一次性补齐全部历史页。
9. 每次 spec sync 后、archive 后都再次运行 `openspec validate --all`；归档目录和 main specs 都必须可验证。
10. 文中的“已成功索引”“成功报告”“fixtures 已完成”表示对应 change 的代码和自动门禁已完成/归档，不要求无真实凭据的环境执行可选外部 smoke；未执行项必须如实记录。

## 四、累积质量门禁

每个提案运行受影响范围测试，并至少执行 `openspec validate --all` 与 `git diff --check`。P26、P27 必须执行以下全量门禁：

```bash
# 仓库根目录
openspec validate --all
npm --workspace packages/api-contracts run typecheck
npm --workspace packages/api-contracts run test
npm run frontend:typecheck
npm run frontend:test
npm run frontend:build
npm run docs:build
docker compose -f infra/compose.yaml config
# 仅 macOS/Linux 或 Git Bash
bash -n scripts/start-local.sh
git diff --check

# apps/backend
uv run alembic upgrade head
uv run ruff check .
uv run pyright
uv run pytest
```

不要虚构当前仓库不存在的质量设施：本项目没有现成 CI、ESLint、Prettier 或 Playwright。若要新增，应另开独立 OpenSpec change。

## 五、提案总览

| 阶段 | 提案 | 结果 |
|---|---|---|
| 工程底座 | P01–P09 | 技术栈、contracts、SQLite、认证/隔离、Qwen、Milvus、Vue 壳、durable jobs |
| 知识系统 | P10–P13 | 文档、切分、持久索引、混合检索、知识库 UI |
| Chat Agent | P14–P19 | 会话、SSE Agent、Prompt/Skill、记忆、MCP、最终 Chat UI |
| AIOps | P20–P24 | 告警/CLS、诊断图、证据、案例、最终 UI、用户反馈 |
| 交付闭环 | P25–P27 | 真实 fixture、readiness/可观测性/文档、OpenSpec WIKI |

---

## P01：锁定技术栈与安全 Monorepo 骨架

复制下面整个代码块：

```text
请完成第 01 个 OpenSpec change：bootstrap-secure-monorepo-foundation。

请依次使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成完整生命周期。不要只生成 proposal/design/spec/tasks 后停止；若验证发现问题，先修复并重新验证，再同步 delta specs 和归档。所有 OpenSpec 文档使用简体中文。

这是一个全新项目的第一提案。本提案必须先锁定整个项目的技术栈、目录骨架、工程边界和质量基线，但不要实现认证、聊天、知识库、AIOps、MCP 等产品功能。

必须在 design 和项目指南中明确技术栈：
- 后端：Python >=3.10、FastAPI、Pydantic v2、uv、hatchling、src layout、SQLAlchemy 2 async、aiosqlite、Alembic、pytest、pytest-asyncio、Ruff、strict Pyright。pytest 使用 asyncio_mode=auto；Ruff line-length=100、target py310、规则 B/E/F/I/UP。
- Agent/AI：LangChain 1.x create_agent、LangGraph、langchain-openai、langchain-mcp-adapters、MCP、pymilvus 3、rank-bm25、pypdf、langchain-text-splitters、httpx；这些能力由后续提案实现。
- 前端：Vue 3.5、Vite 6、TypeScript 5.6 strict（exactOptionalPropertyTypes、noUncheckedIndexedAccess、isolatedModules、ES2022/Bundler resolution）、Pinia 3、Vue Router 4、Vitest 2、marked、DOMPurify、lucide-vue-next。
- 仓库：npm workspaces、OpenSpec spec-driven workflow、VitePress 文档、Conventional Commits。

建立最终目录：
apps/backend、apps/frontend、packages/api-contracts、config、infra、scripts、openspec、docs。
后端包必须位于 apps/backend/src/super_ai，只允许 from super_ai...，禁止从 src.super_ai 导入。模块 import 期间不得连接 SQLite、Milvus、LLM 或 MCP。

建立最小可运行骨架和质量命令：
- backend pyproject、uv.lock、super_ai 包、最小 /health app factory、pytest/Ruff/Pyright 配置。
- frontend Vue/Vite/TS/Vitest 骨架及 dev/typecheck/test/build scripts；以桌面 Web 为验收目标。
- packages/api-contracts 的 typed entrypoint、typecheck/test scripts，先保留最小 foundation 类型。
- 根 package.json workspaces 和 contracts/frontend/docs scripts。
- openspec/config.yaml 使用 spec-driven schema，并在项目上下文中记录上述技术栈与约束。
- 根 AGENTS.md 固化目录、构建命令、Python import/依赖注入、配置/凭据、tenant、真实 MCP、OpenSpec 简中和桌面前端验收规则。
- 中文 README/各 workspace README 只说明骨架和验证方式，不声称未实现的功能。

从第一天采用最终安全配置边界：
- 只提交 config/project.template.json 与 config/user.project.template.json，所有 key/secret/password 为空。
- .gitignore 必须忽略 config/project.json、config/user.project.json、.env*、.idea、.venv、node_modules、dist、coverage、缓存、docs/.vitepress/cache、docs/.vitepress/dist、apps/backend/var、SQLite 和日志文件。
- 在 foundation 中就实现通用 JSON 配置加载：后端 project_config.py 读取 project.json，再以 user.project.json 做递归深合并；P06 只增加 LLM 的 typed validation/provider。
- 前端不得直接 import 两份完整 JSON。vite.config.ts 可以在构建时读取深合并配置，但只能通过 define/virtual module 向 config.ts 注入 `frontend.title`、`frontend.apiBaseUrl`、明确标记为 public 的 analytics key 等 allowlist 字段；LLM、CLS、MCP、MinIO secret 永远不能进入浏览器 bundle。
- 应用只读取本地 JSON 文件深合并结果，不读取 OS 环境变量作为项目配置。
- 当前 workspace 可从模板复制出 ignored 的空本机配置用于 build；不能 stage。测试必须用临时配置注入，不依赖开发者真实值。
- 从零项目禁止设计 filter-repo/force push 步骤。

基础设施只在本提案锁定边界并创建目录/说明：Compose 最终只托管 etcd、MinIO、Milvus、Attu、Alertmanager；后端、前端、官方 CLS MCP Server 必须在主机运行。不要创建 app.Dockerfile、project.compose.json 或应用 Compose 服务。

为目录、包导入、scripts、ignore、import-safety 和前端 public-config allowlist 编写最小测试；用 sentinel secret 构建后扫描 dist，证明 secret 不存在。P01 生成 package/pyproject 后先执行根 `npm install` 和 backend `uv sync`。验收至少运行：openspec validate --all；backend 的 uv run ruff check .、uv run pyright、uv run pytest；contracts typecheck/test；frontend typecheck/test/build；git diff --check。所有门禁通过后才归档。
```

完成标志：空仓库已经成为可验证的安全 Monorepo，但还没有产品功能。

## P02：统一 HTTP、错误、OpenAPI 与 SSE 契约

```text
请完成第 02 个 OpenSpec change：define-api-and-sse-contracts。前置条件是 bootstrap-secure-monorepo-foundation 已归档。

请依次使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change，连续完成提案、实现、验证、修复、spec sync 和归档。OpenSpec artifacts 使用简体中文，不要只停在 artifacts。

目标：让 packages/api-contracts 成为 HTTP response、错误码、OpenAPI path 和 SSE event 的单一事实来源；后端响应与前端 transport 必须对齐它，后续功能只能扩展，不能自造临时 payload。

实现要求：
- 定义成功 envelope：{ok:true,data,meta:{requestId}}。
- 定义失败 envelope：{ok:false,error:{code,category,httpStatus,message,details?},meta:{requestId}}。
- 建立稳定错误目录：AUTH_*、BUSINESS_*、VALIDATION_*、SYSTEM_*，以及后续可扩展的业务错误；每个错误包含 category、HTTP status 和安全默认消息。
- FastAPI 增加统一 success/error helper、validation/exception handler 和 X-Request-ID 透传/生成。
- 定义判别联合 SSE：content.delta、reasoning.delta、tool.call、reference.source、task.status、report、complete、error；公共字段为 id、type、channel(chat|aiops)、timestamp。tool.call 支持 started/delta/completed/failed，SSE error 复用 HTTP 错误结构。
- 建立机器可读 OpenAPI 合同的组织方式，当前只覆盖 foundation/health，后续每个提案必须先补合同再加 endpoint。
- 前端建立 typed apiClient/sseClient 基础：解 envelope、注入 request id/bearer 的扩展点、正确处理跨 chunk SSE frame；不能复制一份私有 event union。
- 后端无需直接导入 TypeScript，但 Pydantic/序列化形状必须由合同测试证明一致。

测试至少覆盖四类 envelope、验证错误字段路径、request-id、SSE 全事件目录、tool lifecycle、错误复用、分块 frame parser、前后端禁止临时事件结构。运行 contracts typecheck/test、backend pytest/Ruff/Pyright、frontend typecheck/test/build、openspec validate --all、git diff --check。验证通过后同步主规格并归档。
```

## P03：SQLite、Alembic 与 Repository 基础

```text
请完成第 03 个 OpenSpec change：setup-sqlite-repository-foundation。前置 change P01、P02 已归档。

使用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完成完整生命周期；无阻塞时不要在 artifacts 或部分任务处停止。文档用简体中文，验证通过后同步 specs 再归档。

目标：建立可替换、可测试、不会在 import 时产生外部副作用的 SQLite 持久化边界，为认证、Chat、知识、任务、MCP、AIOps、反馈和审计提供统一基础。

实现要求：
- SQLAlchemy 2 async + aiosqlite；数据库 URL 从本地 JSON merge 配置读取。
- Alembic 是 schema 迁移的唯一权威；建立 Base、async engine/session factory、迁移环境和首个基础迁移。
- engine/session 只在 FastAPI lifespan、依赖 provider 或显式初始化路径创建；import super_ai.memory 不得打开数据库或运行迁移。
- 领域服务依赖 Repository Protocol/不可变 record，不得接收 ORM model；SQLite 实现位于 `super_ai.memory.sqlite`/`extended_sqlite`，为未来 PostgreSQL 保留替换边界。
- 统一 JSON 字段序列化、UTC 时间、ID 生成和事务约定；避免把业务状态塞进无结构的大 JSON，后续有查询/关联需求的数据必须建规范化表。
- 提供测试用临时 SQLite 数据库和 migration helper；测试不能依赖开发者本机 var/memory.sqlite3。
- 此 change 只建立 persistence foundation，不提前实现后续领域 CRUD。

测试覆盖 fresh database upgrade、metadata 与迁移一致、并发 async session、回滚、Repository contract、import-safety 和配置注入。执行 alembic upgrade head、pytest、Ruff、strict Pyright、openspec validate --all、git diff --check，全部通过后归档。
```

## P04：用户认证

```text
请完成第 04 个 OpenSpec change：add-user-authentication。依赖 P02 contracts 和 P03 persistence。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完整完成 change；先写验收测试，再实现，修复所有 CRITICAL 后同步 specs/归档。OpenSpec 文档使用简体中文。

实现注册、登录、登出、认证恢复和当前用户查询：
- 新增 users、auth_sessions Alembic migration、owner-safe Repository、AuthService 和 FastAPI dependency。
- 邮箱规范化且唯一；密码用 pwdlib[argon2] 哈希，绝不保存或记录明文。
- 登录生成高熵 opaque bearer token；客户端拿 raw token，SQLite 只保存 64 位 SHA-256 token hash。session 保存 createdAt/lastSeenAt/revokedAt，登出可撤销；当前版本不虚构未实现的自动过期策略。
- 用户不存在和密码错误返回同一个 AUTH_INVALID_CREDENTIALS；未知账号也执行 dummy Argon2 校验，避免明显枚举/时序差异。
- API：POST /auth/register、POST /auth/login、POST /auth/logout、GET /auth/me；全部使用统一 envelope/error/requestId。
- contracts 同步增加 Auth DTO、请求/响应、bearer security scheme、401 错误；CORS 允许本机前端 127.0.0.1:5173。
- 前端先实现可复用 authClient/auth state：token 是唯一允许保存在 localStorage 的认证凭据；initialize 时调用 /auth/me；失效和 logout 清除本地受保护 store，但不得删除服务端业务数据。完整页面在 P08 实现。

测试覆盖 migration、注册、重复邮箱、正确/错误登录、hash 不是明文、数据库无 raw token、lastSeen、撤销、/auth/me、统一错误、恢复与清理。运行受影响的 backend/contracts/frontend 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P05：Authorization 与 tenant 隔离基线

```text
请完成第 05 个 OpenSpec change：enforce-tenant-isolation。依赖用户认证已归档。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行，不要只写规格。所有 artifacts 用简体中文；验证问题必须修复后再同步主规格和归档。

目标：把当前 user id 作为本地单租户模型中的 tenant id，为之后所有资源建立强制 owner scope，禁止“先按资源 id 查询、再在 service 层补检查”的不安全模式。

实现要求：
- 定义 CurrentUser/OwnerScope/tenant 上下文和 scoped Repository 约定；所有受保护 Repository 方法都必须显式接收 owner_user_id。
- 当前 user id 与 tenant id 等价，但两个语义字段在向量 metadata/filter 中都要保留。
- 资源不存在与跨用户访问不得泄漏另一个用户的资源细节；受保护父资源的越权访问统一返回 AUTH_FORBIDDEN 403。
- contracts/OpenAPI 为所有未来受保护 path 建立 bearer、401、403 复用模式。
- 提供可复用的 SQLite scope helper 和未来 Milvus filter builder 约定：tenantId 等于当前 user id；Milvus 搜索 filter 只使用 tenantId + allowedKnowledgeBaseIds，空 KB 列表直接返回空结果且不连接 Milvus；可选 document/metadata filter 在 retrieval tool 召回后执行。删除文档向量必须带 tenantId + knowledgeBaseId + documentId。ownerUserId 仍写入标量/metadata 供归属追溯；空 tenant/delete scope 禁止操作。
- 登出只撤销认证并清客户端可见状态，不删除用户持久数据。
- 在 AGENTS/架构文档中声明 chat、knowledge、index jobs、vector、MCP、AIOps、evidence、reports、cases、feedback、audit、background jobs 都必须遵守该边界。

用两个用户编写跨租户合同测试，覆盖读取、更新、删除、父子资源和不可枚举错误语义；为后续 Repository 提供参数级失败测试。运行 backend/contracts/frontend 相关门禁、openspec validate --all、git diff --check，通过后归档。
```

## P06：Qwen/OpenAI-compatible 模型提供者

```text
请完成第 06 个 OpenSpec change：configure-qwen-model-providers。依赖项目配置骨架、Repository 基础和共享 contracts。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 连续完成提案到归档；不要在 artifacts 后停止。OpenSpec 文档简体中文，验证通过后同步 specs。

目标：只通过 P01 已建立的本地 JSON 深合并配置接入 OpenAI-compatible Qwen/Bailian，提供 chat、embedding、rerank 三类可注入边界，且 import 时不联网、错误不泄密。

实现要求：
- 复用并完善 P01 project_config loader：文件缺失/JSON 非对象时给出安全明确错误；本提案增加 LLM section 的 typed validation。应用代码不得读取 OS 环境变量作为项目配置。
- 模板包含 app/backend/frontend、llm、modelCapabilities、vectorStore、mcp、clsMcpServer、prometheusAlerts、clsLogUpload、aiopsDemo 等最终需要的 section；aiopsDemo 至少含 backendBaseUrl/email/displayName/password/pollIntervalSeconds/indexWaitSeconds，所有 password/secret 为空并只在 ignored user config 填写。本机文件从模板复制且保持 ignore。
- LlmProvider Protocol 与 QwenOpenAIProvider；chat 只用 langchain-openai ChatOpenAI，embedding 只用 OpenAIEmbeddings。禁止引入 DashScope SDK。
- Embedding 使用 text-embedding-v4、dimensions=1024、原始字符串输入、check_embedding_ctx_length=false、chunk_size/单批最多 10，并保证多批次结果顺序不变。
- chat model capability profile 提供 contextWindowTokens；默认可配置 qwen3.7-max，temperature=0.2、timeout=120、retries=2。
- rerank 使用独立可注入 HTTP client，默认 qwen3-vl-rerank endpoint；不要伪造 fallback 分数。
- provider readiness 发起最小异步请求并返回 provider/model/baseUrl/latency；任何 apiKey 必须从异常中替换为 [redacted]。
- 外部 client 只在 factory/显式调用中创建，模块导入不连接网络。

测试使用注入 fake transport/config，不要求真实凭据；覆盖深合并、缺失字段、provider 参数、embedding >10 分批、顺序、rerank payload、timeout/retry、readiness 脱敏和 import-safety。另记录有真实凭据时的手动 smoke，但未执行时不得声称通过。运行 backend 全门禁、contracts 相关检查、openspec validate --all、git diff --check 后归档。
```

## P07：本地基础设施与 Milvus 向量边界

```text
请完成第 07 个 OpenSpec change：setup-local-infrastructure-and-milvus。依赖 P01、P05、P06。

使用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完成完整生命周期。OpenSpec artifacts 用简体中文；不要复刻早期全栈 Compose，验证通过后同步 specs 并归档。

目标：建立最终的本地优先运行边界和 tenant-safe Milvus adapter。

基础设施要求：
- infra/compose.yaml 只包含 alertmanager、etcd、minio、milvus、attu 五个服务及持久卷/healthcheck。
- 与当前项目终态一致：etcd v3.5.18、MinIO RELEASE.2024-12-18T13-15-44Z、Milvus v3.0-beta、Attu v2.5.12、Alertmanager v0.28.1；Compose 是镜像版本唯一事实来源。当前模板里的 docker.appImageTag/clsMcpServerVersion/milvusImage 是未消费遗留，本从零实践有意删除这一段，避免 v3.0.0 与 Compose 冲突。
- Milvus standalone 依赖 etcd/MinIO；Attu 依赖 Milvus；Alertmanager 挂载只读配置并暴露 9093。
- Compose 不得包含 backend、frontend、cls-mcp-server、env_file、${...}、应用镜像、应用 Dockerfile、日志上传或 SOP seed。
- MinIO 只是 Milvus 依赖，不是应用文档对象存储。

Milvus adapter 要求：
- 使用 pymilvus 官方 client，但 import super_ai.vector_store 不得创建 client、连网或初始化 collection。
- 提供显式 initialize/connect、health、insert、search、delete-document 生命周期和可注入 fake client；当前 adapter 不虚构 public close API。
- collection 使用 1024 维 float vector、HNSW/COSINE、M=16、efConstruction=200、search ef=64。
- 字段至少包括 chunkId 主键、documentId、knowledgeBaseId、ownerUserId、tenantId、content、source、createdAt、metadata、vector；为可过滤标量建立索引。
- search 必须由结构化 scope 生成 tenantId + allowedKnowledgeBaseIds；KB 列表为空时直接返回 [] 且不连接 Milvus。document/metadata 条件由 retrieval tool 对 owner-scoped 粗召回结果后过滤，不写入 Milvus search expression。delete-document 必须生成 tenantId + knowledgeBaseId + documentId。ownerUserId 同时保存在标量/metadata 供追溯，但不重复加入 Milvus filter。空 tenant 或 delete 的 KB/document scope 直接拒绝。
- 配置来自本地 JSON merged vectorStore；不从 env 读取。

测试覆盖 compose service 白名单和废资产黑名单、docker compose config、lazy lifecycle、schema/index、幂等 initialize、tenant filter escaping、空 KB 搜索不连接/空 tenant 或删除 scope 拒绝、跨用户 search/delete、health、import-safety。运行 backend 全门禁、compose config、openspec validate --all、git diff --check；真实 Milvus smoke 只在服务可用时执行并如实记录。通过后归档。
```

## P08：中文桌面 Vue 工作台壳

```text
请完成第 08 个 OpenSpec change：build-chinese-vue-app-shell。依赖认证、contracts 和基础技术栈。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成 artifacts、代码、验证、修复、spec sync 和归档。不要只做静态 mock 页面；OpenSpec 文档用简体中文。

目标：建立可承载后续真实功能的 Vue Router + Pinia 认证工作台壳和统一交互基础。本提案以桌面浏览器为验收目标，不新增移动专用抽屉、底部导航或替代流程。

实现要求：
- 路由：/login、/register 为 publicOnly；受保护 WorkspaceLayout 下预留 /chat、/knowledge、/aiops、/mcp；/ 重定向 /chat，未知路由回 /chat。
- router guard 首次导航只执行一次 auth.initialize()；未登录保留 redirect，已登录访问登录/注册页回 /chat。
- 登录/注册表单使用 P04 真实 API；刷新通过 /auth/me 恢复；logout 撤销服务端 session 后清除本地受保护 store。
- WorkspaceLayout 提供左侧 rail 导航、仅 Chat 路由可用的会话区域插槽、账号/登出、顶栏标题和服务状态；业务页面使用 edge-to-edge 路由画布。
- 建立 Pinia stores 的清理注册机制、typed apiClient/sseClient、protectedData state；不能用 localStorage 保存 chat/knowledge/AIOps 领域数据。
- 共享 AppLoadingState、AppEmptyState、AppErrorState、AppFeedback、AsyncStatusBadge；状态必须有文字/ARIA，不能只靠颜色。
- 全局反馈支持 success/info/error、手动关闭、3 秒自动消失；新消息重置 timer，unmount 清理 timer。
- 建立安静、专业的中文设计 tokens、Lucide 图标、清晰 focus 和 prefers-reduced-motion。不要声称业务页已经完成。

测试路由保护/redirect/auth 恢复、typed transport、401 清理、store 清理、feedback fake timer、可访问状态、桌面 workspace 布局和 placeholder 路由。运行 frontend typecheck/test/build、contracts test/typecheck、相关 backend tests、openspec validate --all、git diff --check，通过后归档。
```

## P09：Durable Background Job Runtime

```text
请完成第 09 个 OpenSpec change：add-durable-background-job-runtime。依赖 SQLite Repository、认证和 tenant 隔离。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行。所有文档简体中文；实现和验证不可省略，修复 CRITICAL 后同步 specs/归档。

目标：用 SQLite 保存后台任务和事件，让后续文档索引、AIOps 在客户端断开或进程重启后仍可恢复。不得用临时 create_task 作为最终运行时。

实现要求：
- Alembic 增加 background_jobs、background_job_events；任务包含 owner、kind、resourceType/resourceId、status、payload、attempt/maxAttempts、timeoutSeconds、availableAt、leaseOwner/leaseExpiresAt、cancelRequestedAt、retryOfJobId、errorMessage 和 created/updated/started/completed 时间戳。heartbeat 通过续写 leaseExpiresAt 实现，不虚构 heartbeatAt/result 列。
- Repository 所有 list/get/cancel/retry/event 操作显式 owner scoped。
- handler registry 按 kind 注册；worker 在 FastAPI lifespan 启停，默认 concurrency=2、lease=30s、poll≈0.2s。当前 runtime 直接使用 `_utc_now()`/`asyncio.sleep()`，不虚构 clock 构造参数。
- 原子领取、heartbeat 续租、过期 lease 恢复、进程重启恢复、指数退避且最大 30s、最大尝试次数、任务 timeout、协作式取消。
- 状态至少 queued/running/succeeded/failed/cancelled；事件 sequence 单调，Repository 支持 `list_events(after_sequence=...)`。AIOps 重连可从持久事件重放（当前实现可从 sequence=0 重放），不虚构尚未实现的 HTTP Last-Event-ID 协议；SSE 断开不取消任务。
- API：GET /background-jobs、GET /background-jobs/{id}、POST /background-jobs/{id}:cancel、POST /background-jobs/{id}:retry；contracts/OpenAPI 同步。
- 错误和 payload 日志脱敏；worker crash 不能让 lease 永久悬挂。

测试使用临时 SQLite 和 fake handler，覆盖并发唯一领取、lease/heartbeat、过期回收、restart、retry/backoff、timeout、cancel、事件顺序、owner 隔离、断连恢复、lifespan 清理。运行 migration、backend 全门禁、contracts 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P10：知识文档与切分策略

```text
请完成第 10 个 OpenSpec change：manage-knowledge-documents-and-chunking。依赖认证/tenant、SQLite、Milvus 边界和 contracts。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 连续完成。文档使用简体中文；只实现本 change 的文档管理和切分，不提前实现完整检索/UI。验证通过后 sync specs 并归档。

目标：为每个 user 提供一个隐式默认知识库及 owner-scoped 文档管理，采用最终 `.md`/`.pdf` policy，并让预览和索引未来复用同一个 splitter service。

实现要求：
- API：GET /knowledge-bases；GET/POST /knowledge-bases/{kb}/documents；GET/DELETE /knowledge-bases/{kb}/documents/{document}; GET .../{document}/chunk-preview。
- 每个 user 的知识库 id 稳定且不可访问其他 user；当前范围不提供创建/删除多个知识库。
- 只允许 UTF-8 Markdown 和 PDF，最大 10 MiB；后端权威校验扩展名、MIME、大小，使用 pypdf 提取 PDF 文本。
- 保存文件名、size、MIME、SHA-256、uploadedAt、index status、chunking config 和可索引正文；应用不把原文放入 MinIO。
- 相同 owner/KB 的重复 hash 默认 BUSINESS_CONFLICT 409；只有显式 overwrite 才软删除旧文档并按 owner scope 清理旧向量。普通删除同样清理向量。
- 三种策略：fixed-character（默认 maxCharacters=1200、overlap=200）、markdown-heading、paragraph。只有 fixed-character 接受 max/overlap，且校验 overlap < max。
- 同一个 `chunk_document_text` 切分入口（可由 DocumentChunkingService 封装）同时供 preview 和后续 indexing；preview 最多 12 段，每段 excerpt 最多 400 字；文档保存实际采用的策略和参数，chunk metadata 可追溯。
- contracts/OpenAPI 先定义 document DTO、upload policy 常量、multipart config、preview、重复/覆盖和 401/403。

测试覆盖 md/pdf 提取、所有 policy 边界、hash 冲突/overwrite、三个 splitter、参数非法、有界 preview、删除向量 scope、跨用户和 import-safety。测试必须使用 tmp 文件/config，不依赖真实密钥。运行 backend/contracts 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P11：持久文档索引流水线

```text
请完成第 11 个 OpenSpec change：run-durable-document-indexing。依赖 P06 Qwen、P07 Milvus、P09 durable jobs、P10 文档/切分。

请用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整完成提案、实现、验证、修复和归档。OpenSpec artifacts 简体中文，不得回退为进程内临时 asyncio 任务。

目标：把文档切分、Qwen embedding、Milvus 写入作为 durable job 执行；上传后由客户端显式创建首次任务，随后支持持久调度、状态恢复、失败重试、重建和取消。

实现要求：
- Alembic 增加 document_index_tasks 领域记录，保存 owner、kb、document、status、failureReason、retryOfTaskId 和时间戳；不新增 jobId 列。底层 background_jobs 通过 resourceType=`document_index_task`、resourceId=taskId 建立关联。
- 文档上传 API 只创建文档；客户端在上传成功后立即显式 POST .../index-tasks 创建任务并入队。API 同时提供 GET .../index-tasks/{task}、POST .../{task}:retry，用于状态、重建/重试。
- handler 流程必须为：重新读取 owner-scoped 文档 → 用 P10 splitter 产生全部 chunks → embedding provider 按每批最多 10 且保持顺序 → 显式 initialize Milvus → owner scoped 删除旧 chunks → 一次批量 insert_chunks 写入全部 chunks → 更新任务/文档状态。SQLite 与 Milvus 之间不宣称跨系统原子事务，失败通过状态和重试恢复。
- chunkId/documentId/knowledgeBaseId/ownerUserId/tenantId/content/source/createdAt/chunking metadata 全部写入。
- 大于 10 chunks 时只有 embedding provider 分批（每批 ≤10）且不丢失、不重排；Milvus 仍一次 insert 全部 chunk records。失败原因安全持久化，失败不能把文档标成功；retry 创建新 attempt 并保留来源。
- 文档领域状态 pending/running/succeeded/failed/cancelled 在 contracts、API、UI-ready DTO 中一致；底层 background job 的 queued 状态映射为领域 pending，客户端断开不影响任务。
- 不静默吞掉 embedding/Milvus/split 错误，不用假向量。

测试覆盖“上传 API 后客户端显式创建首次 index task”、手动重建、>10 embedding 分批且单次 Milvus insert、Milvus 初始化顺序、旧向量清理、完整 metadata、失败/重试/取消、worker 重启、owner 隔离和 API envelope。运行 migration、backend/contracts 全门禁、可用时真实 Qwen+Milvus smoke（无凭据时明确未执行）、openspec validate --all、git diff --check，通过后归档。
```

## P12：混合召回、RRF 与真实 Rerank

```text
请完成第 12 个 OpenSpec change：provide-reranked-hybrid-knowledge-retrieval。依赖已成功索引的知识文档、Qwen provider、Milvus 和 tenant scope。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完整执行；不要只写算法设计。OpenSpec 文档简体中文，修复验证问题后同步 specs 并归档。

目标：提供给 Agent 自主调用的 knowledge_retrieval LangChain Tool，直接实现最终检索形态，不经历“仅向量”或 BM25Okapi 的历史旧方案。

权威流水线：
1. 校验非空 query、topK 默认且最大 5、可选 knowledgeBase/document filters，并先固定当前 owner/tenant scope。
2. 对 query embedding；Milvus 向量召回和当前 tenant 文档语料的内存 BM25L 关键词召回并行执行。
3. 中文 tokenizer 同时产生单字/bigram，保留英文、数字、Java 类名、trace/service 等 ASCII 运维 token；不相交词项得 0，BM25 分数不得为负。
4. 使用 RRF `k=60` 融合并确定性排序，送 rerank 的候选最多 20。
5. 调用真实 Qwen rerank，最终最多 5 条、无最低阈值；rerank 改变顺序时必须保留各阶段原始排名。

每条结果/引用必须包含稳定 chunk/document/kb id、source/excerpt/metadata，以及 vectorRank/vectorScore、bm25Rank/bm25Score、rrfScore、rerankRank/rerankScore；未命中某分支的 rank 为 null，兼容 score 等于 rerankScore。

没有结果返回空 results，不能生成兜底内容。embedding/vector/BM25/rerank 任一必需分支失败时返回安全明确错误，不伪造分数或悄悄改成另一算法。工具调用始终按当前 user 过滤，模型传入的 filter 不能扩大权限。

contracts 增加 Tool input/output/citation 类型，但不需要暴露一个独立搜索产品 API。测试覆盖中英 token、小语料 positive IDF、双分支并行、单路未命中、RRF 公式/稳定 tie、rerank 改序、topK、全部 rank/score、空结果、每类 provider 失败和跨租户。运行 backend/contracts 及相关 frontend contract tests、openspec validate --all、git diff --check；有真实服务时做 smoke 并如实记录。通过后归档。
```

## P13：最终知识库桌面工作区

```text
请完成第 13 个 OpenSpec change：build-knowledge-base-workspace。依赖 P08 Vue 壳、P10 文档、P11 索引和共享 contracts。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整完成；OpenSpec artifacts 简体中文。必须连接真实后端 API，不能用 localStorage 或静态数组模拟领域数据。

目标：实现 /knowledge 的最终桌面工作区和 Pinia knowledge store。

实现要求：
- typed knowledgeClient/store 管理 knowledgeBases、documents、selected detail、chunk preview、index tasks、overwrite confirmation；服务器是事实来源。
- 单知识库时隐藏无意义 selector；上传区只接受 .md/.pdf，前端使用 shared policy 做即时提示，但后端仍是权威。
- fixed-character 显示长度/overlap；markdown-heading、paragraph 不发送这些字段。上传前选择策略；文档上传后通过其 chunk-preview endpoint 查看实际切分结果。
- 上传成功展示 indexing 并跟踪后台任务；活动任务约每 2 秒 poll，支持失败原因、retry 和手动重建；取消由通用 background-job 能力负责，不在知识页自造另一套状态机。
- hash 冲突必须显示明确覆盖确认，不能静默覆盖；删除也要确认并在成功后刷新服务端列表。
- 文档列表在桌面有界区域独立滚动，详情在对应行下默认折叠；展开后 metadata 和 chunk preview 各自有界滚动，长表格可横向滚动，不能撑坏整页。
- loading/empty/error/status 都有中文可访问文字；状态不只靠颜色。不要新增移动专用导航或替代流程。

测试 store 的 auth header/envelope、upload multipart、策略字段、poll/retry/overwrite/delete、owner 数据清理；组件测试上传、行内 detail、preview 和滚动 CSS 约束。运行 frontend typecheck/test/build、contracts 门禁、相关 backend tests、openspec validate --all、git diff --check；用本地桌面浏览器做 MD/PDF 上传→索引→预览→删除 smoke。通过后归档。
```

## P14：持久 Chat 会话

```text
请完成第 14 个 OpenSpec change：manage-chat-sessions。依赖 contracts、SQLite Repository、认证和 tenant isolation。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完整完成；OpenSpec 文档简体中文，先补合同和迁移，再实现，验证通过后同步 specs 并归档。

目标：建立完全由服务端 SQLite 管理的会话与消息生命周期，为下一提案的流式 Agent 提供稳定边界；本提案不调用模型。

实现要求：
- Alembic 增加 chat_sessions、chat_messages；所有记录 owner scoped。message 支持 role/content、序号/时间、结构化 metadata，metadata 可保存 references 和 toolCallIds。
- API：POST /chat/sessions；GET /chat/sessions（按 updatedAt 倒序）；GET /chat/sessions/{id}；POST /chat/sessions/{id}/messages；POST .../messages:clear；DELETE /chat/sessions/{id}。
- 第一条 user message 生成有界标题；后续消息更新 session updatedAt，但不能让列表排序不确定。
- clear 只清消息并重置会话衍生状态；delete 删除当前 user 会话及其子记录；跨 user 一律 AUTH_FORBIDDEN，不能仅凭 id 命中。
- 服务层只用 Repository records，不泄漏 ORM；写消息和更新会话放在一致事务边界。
- contracts/OpenAPI 定义 session/message/metadata/list/detail/create/append/clear/delete 及 401/403。前端可新增 chatClient/store 的非流式基础，但不能以 localStorage 为主存储。

测试两个用户的 CRUD/排序/自动标题/metadata/事务/clear/delete、跨租户、错误 envelope 和前端 store 对账。运行 migration、backend/contracts/frontend 相关门禁、openspec validate --all、git diff --check，通过后归档。
```

## P15：Agentic RAG Chat、SSE 与工具审计

```text
请完成第 15 个 OpenSpec change：stream-agentic-rag-chat-and-audit-tools。依赖 P06 Qwen、P12 knowledge tool、P14 chat sessions、P09 durable/observability 基础。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行。不要在 artifacts 后停止；OpenSpec 文档简体中文，验证通过后同步主规格并归档。

目标：用 LangChain create_agent 实现模型自主选工具的持久流式聊天，而不是每轮固定先做 RAG。先接 knowledge_retrieval 和 get_current_time；MCP 在 P18 扩展。

实现要求：
- POST /chat/sessions/{sessionId}/messages:stream 接收 user content/metadata，调用前先校验 session owner。
- Agent tools 至少包含 tenant-scoped knowledge_retrieval 与 get_current_time；由模型判断是否调用。禁止在 Agent 前无条件检索知识库。
- 使用共享 SSE union 发 content.delta、可选 reasoning.delta、tool.call lifecycle、reference.source、complete/error。只有模型真实提供 reasoning 时才发，不能合成“思考过程”。
- 最终回答正文在后端按 Unicode 字符拆成有序 content.delta；tool/reasoning/reference/complete/error 不拆字符。事件 id/sequence 稳定且 complete 只出现一次。
- user message 在开始前按一致语义持久化；assistant message 只在成功完成后一次性持久化，metadata 保存本轮 references/toolCallIds。流失败不得留下半条 assistant 消息。
- 每轮重新初始化 live references；第二轮不能继承第一轮引用，reload 只使用对应 assistant message 的 metadata。
- Alembic/Repository 增加通用 agent tool call audit：owner、二选一的 chatSessionId/diagnosticTaskId parent、toolName、arguments、status、resultSummary、errorMessage、started/completedAt、durationMs。arguments 是 owner-scoped 审计数据；结构化运行日志仍只能记录参数键，不能把参数值复制进日志。当前合同没有 parentCallId。
- GET /chat/sessions/{id}/tool-call-audits 返回 owner-scoped 审计；日志不得记录 prompt、query、完整 args、tool output 或 token。
- tool/provider 错误转成共享 SSE error；不能用假答案掩盖失败。

测试事件顺序、字符拆分、多字节文本、工具 started/completed/failed、引用、模型不调用知识工具、模型自主调用、两轮引用隔离、失败无半消息、审计生命周期/父子关系、跨用户和 SSE parser。运行 backend/contracts/frontend 相关门禁、openspec validate --all、git diff --check；有真实 Qwen/Milvus 时做一次对话 smoke。通过后归档。
```

## P16：用户 Prompt 与渐进式 Skill

```text
请完成第 16 个 OpenSpec change：manage-prompts-and-progressive-skills。依赖持久 Chat Agent、SQLite、认证和 contracts。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完整完成，OpenSpec artifacts 简体中文。直接实现最终 progressive Skill 语义，不复刻静态项目 catalog 或全文预注入旧方案。

目标：允许每个 user 管理系统 Prompt 和标准 Agent Skill，并在每次请求中由服务端装配当前选择。

实现要求：
- Alembic 增加 user_chat_configurations、user_chat_prompts、user_chat_skills；Prompt 单选、Skill 多选，全部 owner scoped。
- API：GET/PUT /chat/configuration；POST /chat/prompts；PUT/DELETE /chat/prompts/{id}；POST /chat/skills multipart 上传；DELETE /chat/skills/{id}。
- Prompt CRUD 保存 label + content；删除当前选中 Prompt 时采用明确、可测试的 fallback。
- Skill 以 multipart 文件上传，文件名必须严格为 `SKILL.md`；示例和概念目录采用 `<skill-name>/SKILL.md`。校验 YAML frontmatter 中 name、description，name 规范化且 user 内唯一，保存 filename/content/metadata/摘要。
- 初始 system prompt 只列选中 Skill 的 name/description，绝不注入完整正文；为当前 request 创建 owner-scoped `load_skill(name)` LangChain Tool，只有模型调用时返回正文。未选择/其他 user 的 skill 不能加载。
- 最终 system prompt 由平台安全规则 + 当前 Prompt + Skill catalog 组装；不能让用户 Prompt 绕过 tenant/tool 安全边界。
- reasoning 仍只透传模型真实内容。
- 提供 5 个标准示例 Skill：knowledge-search、log-analysis、incident-report、api-troubleshooting、change-risk-review，目录均为 `<name>/SKILL.md`。
- contracts 和前端 configuration store 支持可编辑资产及 selectedPromptId/selectedSkillIds；最终侧栏在 P19 完成。

测试 migration、Prompt/Skill CRUD、frontmatter/路径非法、跨 user、catalog 只含摘要、正文不预注入、模型调用 load_skill、未选中拒绝、删除 fallback、5 个样例规范。运行 backend/contracts/frontend 门禁、openspec validate --all、git diff --check；可用模型时验证一次按需加载。通过后归档。
```

## P17：会话级记忆模式与上下文预算

```text
请完成第 17 个 OpenSpec change：add-session-memory-modes。依赖 Chat sessions、streaming、Qwen modelCapabilities 和 Prompt/Skill assembly。

请用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完成全部工作；OpenSpec 文档简体中文。验证发现设计偏差时同步更新 artifacts，再修复代码并归档。

目标：每个会话独立配置记忆压缩策略，在不删除完整历史的前提下控制送给模型的上下文，并在 95% 硬上限前安全拒绝。

实现要求：
- session memory mode：every_30_turns、context_70_percent、manual；数据库保存 memory_mode、memory_summary、compacted_message_count、context_tokens、last_compacted_at；DTO 计算并返回 contextTokens、contextWindowTokens、contextUsagePercent、compactedMessageCount、lastCompactedAt、canCompact。
- 把 token 估算集中在纯函数 `estimate_context_tokens`，内部使用 LangChain `count_tokens_approximately`；阈值测试可 monkeypatch/注入确定结果，才能稳定验证 69%/70%/95% 边界。
- 每 30 个完整 user/assistant turn 自动压缩，或预计上下文达到 model capability 70% 时自动压缩；manual 只在显式 API 请求时压缩。
- 压缩调用 LLM 生成可追溯摘要，但绝不删除或改写完整 chat_messages；组装上下文为历史摘要 + 未压缩消息 + 当前 Prompt/Skill catalog。
- 在持久化新 user message 和调用模型之前计算候选预算；达到 95% 时返回 CHAT_CONTEXT_LIMIT_REACHED（HTTP/SSE 共用），提示手动压缩，且不写入该消息。
- API：PUT /chat/sessions/{id}/memory；POST /chat/sessions/{id}/memory:compact；session DTO 包含刷新后的 memory state。
- 每个会话互不影响、全部 owner scoped；模型 capability 缺失时明确配置错误，不猜窗口。
- 前端 store 先支持读取/更新/compact，P19 放入 composer。

测试三模式触发边界、29/30 turn、69/70/95%、摘要不删历史、压缩边界、失败回滚、拒绝前不持久化、跨 user、API/SSE 同错误和 capability config。运行 migration、backend/contracts/frontend 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P18：用户级真实 MCP 连接与工具治理

```text
请完成第 18 个 OpenSpec change：manage-real-mcp-connections-and-tools。依赖认证/tenant、Chat Agent、工具审计、项目配置和 Vue 壳。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完整执行；OpenSpec artifacts 简体中文。产品运行时禁止 mock MCP profile、假工具列表或假调用结果。

目标：每个 user 管理自己的 MCP Servers，真实发现并调用工具，Chat 与后续 AIOps 共用同一连接来源。

实现要求：
- Alembic 增加 mcp_connections：owner、name、transport(sse|streamable_http)、url、enabled、timeoutSeconds(1..300)、retries(0..5)、lastCheck、lastError、discoveredTools、时间戳。
- URL 只允许 http/https、有 host、拒绝 userinfo；当前模型不支持自定义 headers，完整 URL（包括 query）会持久化并返回，因此文档必须明确禁止把 token/secret 放进 URL query。
- API：GET/POST /mcp/connections；PUT/DELETE /mcp/connections/{id}；POST /mcp/connections/{id}:check。check 必须真实连接并返回实际工具列表/错误。
- 使用 langchain-mcp-adapters/MCP client；按当前 user 的 enabled connections 聚合工具。不同 server 的同名工具直接报明确冲突，不随机选择。
- timeout/retry 有界，失败显式；默认 CLS 配置只能作为真实回退连接来源，不能产生 fake profile/result。
- 把真实 MCP tools 注入 Chat request-scoped Agent，并复用 tool.call SSE 和统一 audit；只记录工具名、参数键、状态、耗时和安全摘要。
- 实现 /mcp 的 typed client、Pinia store 和桌面管理页：连接列表、编辑、启停、SSE/Streamable HTTP、检查状态、真实工具发现。服务器是事实来源。
- README 只说明官方 cls-mcp-server 在主机运行；启动/凭据细节在 P26 完成。

测试 CRUD/owner、URL/范围校验、check/discovery、timeout/retry、disabled、不重复调用、同名冲突、Chat 注入、审计/脱敏和 UI store。单测可 fake transport；另用真实官方 CLS MCP 做 smoke，无凭据/服务时明确未执行，绝不声称 mock 等于真实。运行全相关门禁、openspec validate --all、git diff --check，通过后归档。
```

## P19：最终 Chat 工作区、引用与打字机

```text
请完成第 19 个 OpenSpec change：build-final-chat-workspace-and-citations。依赖 Vue 壳、Chat sessions/stream、Prompt/Skill、memory、MCP 和 retrieval contracts。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行。OpenSpec 文档简体中文；必须连接真实 API/SSE，修复所有验证问题后 sync specs/归档。

目标：实现 /chat 当前最终桌面体验，把此前所有 Chat 后端能力组合成一致工作区。

布局与交互：
- 会话列表/新建/切换/删除放入全局 Workspace 左栏，仅 /chat 显示；Chat 主区不再嵌套第二个历史侧栏。
- 主区域 conversation-first，消息区局部滚动，composer 保持可见；右侧 Prompt 与 Skill 为独立 sidebar/disclosure，记忆模式和占用率放在 composer 邻近位置。
- 空会话 transcript 保持真正空白，不渲染醒目的空状态图标/绿色占位。
- Enter 发送、Shift+Enter 换行、IME composing 不误发；textarea 不允许用户 resize。user/assistant 气泡保持专业、宽度适应正文。
- 正文经 marked + DOMPurify 安全渲染，禁用不可信 raw HTML。

流与状态：
- Pinia 保存 sessions/active/messages/config/toolAudits/liveToolCalls/references；领域数据不进 localStorage。
- 解析共享 SSE；当前实现按 for-await 顺序处理事件，每个正文字符更新后 `setTimeout` 约 28 ms，再继续读取后续事件；不虚构 requestAnimationFrame/独立队列。complete 后从服务端历史对账。
- 新回合先清空 live reference；reload 从对应 assistant metadata 恢复，不能显示上一轮引用。
- reasoning 和 tool lifecycle 可折叠，tool output 默认折叠，只显示安全摘要，不展示 raw JSON。

引用体验：
- reference 卡片最多 5 条，按 rerankRank/score；显示来源、excerpt、文档/kb、vector/BM25/RRF/rerank rank 与 score。
- detail disclosure 展示 metadata 和检索阶段轨迹，支持导航到 owner 文档；未参与某阶段显示“未命中”而不是伪造 0 排名。
- Prompt 单选/CRUD、Skill 多选/上传/删除、manual compact 和 memory mode 可操作且错误可恢复。

测试 IME/键盘、SSE 断帧、28ms fake timer、complete 对账、两轮引用隔离、安全 Markdown、tool/reasoning、会话左栏、空白 transcript、Prompt/Skill/memory 操作和桌面固定布局。运行 frontend/contracts 全门禁及相关 backend tests、openspec validate --all、git diff --check；用真实模型做“普通问答”和“自主知识/MCP 工具问答”桌面 smoke。通过后归档。
```

## P20：真实告警入口与 CLS 日志输入

```text
请完成第 20 个 OpenSpec change：integrate-active-alerts-and-cls-log-inputs。依赖配置、认证、MCP/CLS 基础、contracts 和 Alertmanager infra。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成完整生命周期。OpenSpec artifacts 简体中文。涉及真实 CLS 写入属于外部副作用，只有用户提供自己的凭据并确认目标后才可执行；不要在普通测试或启动时自动运行。

目标：聚合真实 Prometheus v1/Alertmanager v2 活跃告警，为 AIOps 提供标准化输入，并提供独立、安全、显式的腾讯 CLS 日志生成/上传工具。

实现要求：
- project config 的 prometheusAlerts.sources 支持 prometheus-v1 和 alertmanager-v2，可选 basic auth、timeout；所有凭据只在 ignored local JSON。
- AlertProvider/Aggregator 通过 httpx 异步读取真实 API，把 alertname/service/severity/status/startsAt/labels/annotations/source/raw context 标准化。
- 一个 source 失败时保留其他 source 的真实告警；API 当前只返回标准化 items，不虚构 provider status 字段。所有 source 失败时显式 503，不构造默认告警。
- GET /aiops/alerts/active 是认证 API，contracts/OpenAPI 定义标准告警 DTO（每条含 source/status）和 401/403；不增加聚合 provider 状态集合。
- 新增独立 Python 脚本 generate_and_upload_cls_logs.py，使用官方 tencentcloud-cls-sdk-python；`LogClient` 由 endpoint 决定路由，调用 `put_log_raw(topicId, groups)` 上传有界、无敏感信息的结构化日志。region 作为配置/每条日志字段保留，logsetId 仅供人工关联；支持 count 上限。
- 脚本从本地 JSON 读取凭据，输出不得打印 secret；应用运行时不自动上传日志。
- 当前 change 只提供告警/日志输入，不生成诊断结论；P21 使用这些输入。

测试 Prometheus/Alertmanager payload、单源失败、全失败、认证访问、脱敏、CLS payload/count/endpoint 校验和“import/普通启动无副作用”。告警 source 是 deployment-global 项目配置，不虚构 user-owned source；只有诊断/持久业务数据按 owner 隔离。单测 fake HTTP/SDK 边界；真实 API smoke 需用户确认并如实记录。运行 backend/contracts 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P21：Durable AIOps 诊断、证据链与报告

```text
请完成第 21 个 OpenSpec change：run-aiops-diagnosis-and-store-evidence。依赖 durable jobs、hybrid retrieval、真实 MCP、活跃告警、Qwen、SQLite/tenant 和共享 SSE。

请依次使用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完成所有 artifacts、代码、测试、修复、spec sync 和归档。OpenSpec 文档简体中文；禁止 mock 日志或假证据支撑产品结论。

目标：使用 LangGraph 实现可恢复、证据优先的 Planner → Executor → Replanner → Report 诊断，并规范化持久化所有过程。

图与执行要求：
- StateGraph：START→planner→executor→replanner→(executor|report)→END；计划有明确最大步数/重规划上限，避免无限循环。
- Planner 先调用 owner-scoped knowledge_retrieval 检索 SOP，再发现当前 user enabled MCP tools；基于 alert/query/SOP 生成有界计划。最终计划应包含且只保留一个真实 SearchLog 类步骤，其余步骤只能使用注册工具；当前 user 没有可用 SearchLog 工具时任务必须以明确 SYSTEM_UNAVAILABLE/工具缺失错误失败，不能伪造日志。
- Executor 真实调用知识或 MCP 工具，失败显式；Replanner 依据已有证据决定继续、调整或报告，不能补造成功。
- 整个诊断由 P09 durable job 执行；创建后客户端可断开，worker 持续运行；cancel/restart/retry/timeout 与持久事件一致。

持久化要求：
- Alembic 增加 diagnostic_tasks、diagnostic_steps、diagnostic_evidence、diagnostic_reports、report_evidence_links、graph_checkpoints；复用通用 tool audits。所有数据 owner scoped。
- 保存原始安全输入、计划/版本、步骤、工具调用、日志/指标/告警/知识引用证据、checkpoint、报告和 report→evidence links，不把完整证据塞进一个不可查询 JSON。
- API：POST /aiops/diagnostics；GET /aiops/diagnostics；GET /aiops/diagnostics/{id}；GET .../{id}/evidence-chain；POST .../{id}:stream。流从持久 job events 回放/轮询，发 task.status/tool.call/reference.source/report/complete/error。
- 创建响应包含 backgroundJob；diagnostic status 使用 accepted/running/succeeded/failed/cancelled，job/SSE task status 使用 queued/running/succeeded/failed/cancelled，并定义明确映射。取消/重试复用 POST /background-jobs/{jobId}:cancel 和 :retry，不虚构诊断专用 cancel 路由。
- Planner/Executor/Replanner 的计划、步骤和安全进度通过 typed task.status 的 task.message/progress 表达；证据使用 reference.source，工具使用 tool.call，报告使用 report。前后端不得自造 plan/step/replan 事件类型。

报告要求：
- LLM 只根据 alert、SOP、plan 和真实 evidence 生成固定中文 Markdown 结构：`# 告警分析报告`、`## 📋 活跃告警清单`、每条告警对应的 `## 🔍 告警根因分析N`（详情/症状/日志证据/根因结论）、`## 🛠️ 处理方案执行N`（已执行步骤/建议/预期效果），最后是 `## 📊 结论`（整体评估/关键发现/后续建议/风险评估）。
- 每个关键结论可追溯 report_evidence_link；证据不足必须标注不确定性。
- 模型失败时使用基于已有证据的结构化中文 fallback，绝不编造根因或工具结果。

测试 SOP/no-SOP、真实工具选择约束、重规划上限、工具失败、worker restart/cancel、事件恢复、规范化证据、checkpoint、报告 provenance、诚实 fallback、跨租户和脱敏。单测可 fake provider 边界但断言没有 fake 产品结论；真实 CLS MCP + Qwen smoke 仅在用户具备环境时执行。运行 migration、backend/contracts 门禁、openspec validate --all、git diff --check，通过后归档。
```

## P22：诊断案例自动沉淀与知识闭环

```text
请完成第 22 个 OpenSpec change：persist-and-automate-diagnosis-cases。依赖成功的 AIOps report/evidence、知识文档、durable indexing 和 tenant scope。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成完整生命周期。OpenSpec artifacts 简体中文；验证通过后同步 specs/归档。

目标：保留显式“保存为知识”操作，并在生成成功最终报告的诊断完成时自动、幂等地生成结构化 owner case，使历史故障进入下一轮 RAG。

实现要求：
- Alembic 增加 aiops_diagnostic_cases，保存 owner_user_id、task_id（唯一）、report_id、document_id、index_task_id、alert_name、service、keywords、root_cause、remediation、summary、evidence_ids、created_at。
- POST /aiops/diagnostics/{id}:save-to-knowledge 作为 legacy 手动补充路径保留；只有当前 user 的 succeeded diagnosis 可保存。它直接创建知识文档和索引任务，重复内容返回 BUSINESS_CONFLICT，不创建 structured diagnostic_cases 行。
- Report 成功节点触发自动 case：必须 task succeeded 且 report 存在；case 保存当时查到的 evidence IDs，列表允许为空。失败/取消或没有成功最终报告的诊断绝不创建。
- 从真实 report/evidence 提取结构化字段并生成 knowledgeType=diagnostic-case 的 Markdown 文档；通过 P11 durable indexing 正常入队，不直接绕过文档/权限边界写向量。
- 自动路径由独立 DiagnosisCasePersistor 按 source diagnostic task 幂等创建 structured case、knowledge document 和 index task；它是主路径。不要虚构手动路径与自动路径共享 service 或相同幂等语义。
- API：GET /aiops/diagnostic-cases、GET /aiops/diagnostic-cases/{id}；全部 owner scoped。contracts 同步。
- case 文档参与后续 knowledge_retrieval，并保留 source diagnosis/report/evidence 可追溯 metadata。

测试成功报告自动创建、失败/取消/无最终报告不创建、空 evidence IDs 仍诚实持久化、legacy 手动保存、并发幂等、跨 user、Markdown 内容、索引调度和 case 被下一轮检索命中。运行 migration、backend/contracts 门禁、openspec validate --all、git diff --check；真实链路可用时做一次“诊断→case→索引→再检索”smoke。通过后归档。
```

## P23：最终 AIOps 桌面工作区

```text
请完成第 23 个 OpenSpec change：build-final-aiops-workspace。依赖 Vue 壳、告警、durable diagnosis、证据/报告、案例 contracts 和 MCP connections。

使用 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行；OpenSpec 文档简体中文。页面必须消费真实 API/SSE/持久状态，不使用假历史、假日志或 raw JSON 充当产品 UI。

目标：实现 /aiops 的专业中文桌面诊断控制台。

布局：
- 桌面三栏：左栏为诊断输入、活跃告警和历史；中栏为当前报告与实时 timeline；右栏为证据/执行链和案例库。
- 整页固定在 workspace 可用高度；每栏长内容独立滚动。长 Markdown 报告在中栏内部滚动，不能撑高页面；右栏保持 provenance。
- 允许手工 query + 可选 alert 创建诊断，也能刷新真实告警并从选中告警预填/创建诊断；当前合同没有独立 context 字段。

状态与交互：
- typed aiopsClient/Pinia store 管理 history、activeAlerts、cases、activeTask、liveEvents、evidenceChain；服务器/持久 job 是事实来源。
- 创建任务后订阅持久 SSE；流断开后重新读取持久任务、history、evidence chain 和 cases 恢复页面，当前前端不虚构自动重新订阅 SSE；支持用户通过 background job id 取消 queued/running job。
- 分开显示 diagnostic 状态 accepted/running/succeeded/failed/cancelled 与 background-job 状态 queued/running/succeeded/failed/cancelled；Planner/Replanner 是 timeline phase，不是独立状态。provider/工具失败不得显示为成功。
- timeline 展示 plan、step、tool lifecycle、evidence、replan；工具输出默认折叠，只显示可读安全摘要，不直接渲染 raw JSON。
- 报告用安全 Markdown；固定报告结构、证据引用、不确定性和 fallback 都清晰显示。
- 案例库可查看结构化 case 并打开对应 owner knowledge document。

测试告警预填、create/SSE/断开后持久状态恢复/cancel/history、report、execution chain、evidence/case、失败状态、长内容内滚和无 raw JSON。运行 frontend/contracts 门禁及相关 backend tests、openspec validate --all、git diff --check；桌面浏览器做真实告警→诊断→报告→证据→案例 smoke（环境不可用时明确未执行）。通过后归档。
```

## P24：统一结构化用户反馈

```text
请完成第 24 个 OpenSpec change：collect-user-feedback。依赖 Chat/AIOps 持久目标、认证、contracts 和最终业务页面。

请用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成提案到归档。OpenSpec artifacts 简体中文；所有 target ownership 必须在服务端验证。

目标：允许 user 对 assistant message、单条 citation、diagnostic step 和 diagnostic report 提交可恢复的结构化反馈。

实现要求：
- Alembic 增加 user_feedback：数据库使用 owner_user_id、target_type、target_id、非空 subject_key、rating、reason、comment、correction、时间戳；DTO 把 subject_key 暴露为可空 subjectId。唯一键为 owner+targetType+targetId+subjectKey，无 subject 时用空串归一化。
- GET /feedback?targetType&targetId；POST /feedback 采用 upsert；DELETE /feedback/{id}。统一 contracts/OpenAPI/envelope。
- 服务端根据 targetType 读取真实父记录并验证 owner；不能相信客户端 owner id，也不能用跨 user 的 target 是否存在来帮助枚举。
- 映射固定为：chat_message 的 targetId=assistant message id、subjectId=null；citation 的 targetId=assistant message id、subjectId=citation id；diagnostic_step 的 targetId=step id、subjectId=null；diagnostic_report 的 targetId=report id、subjectId=null。
- targetType/rating 使用允许集合；reason/comment/correction 做 trim 和长度限制；日志不得记录正文。
- 前端 UserFeedbackControl 支持赞同/反对、问题类型、评论、纠正、更新、删除；Chat answer/citation、AIOps step/report 分别接入。
- 重新打开会话/诊断时读取并恢复反馈；提交失败保留可重试输入，不乐观伪造成功。

测试四类目标、upsert 唯一性、delete、恢复、跨租户、父资源删除/不存在、校验、日志脱敏和组件交互。运行 migration、backend/contracts/frontend 全相关门禁、openspec validate --all、git diff --check，通过后归档。
```

## P25：十套相关联的 Java 电商 AIOps Fixtures

```text
请完成第 25 个 OpenSpec change：create-correlated-ecommerce-aiops-fixtures。依赖真实 CLS 上传、Alertmanager、SOP 文档/索引和 AIOps 全链路。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成完整生命周期。OpenSpec 文档简体中文。所有上传、告警发布、SOP seed 都有真实外部副作用，只能由用户显式执行；普通启动和测试不得自动触发。

目标：提供 10 套互不重复、可端到端关联的 Java 电商故障演示，每套都有 CLS logs、Alertmanager alert 和 Markdown SOP。

至少包含以下 incident/service：
1. payment-service 支付网关超时；
2. inventory-service 库存锁等待；
3. order-service 数据库连接池耗尽；
4. cart-service Redis 延迟；
5. api-gateway 结算熔断；
6. promotion-service CPU 饱和；
7. order-event-consumer Kafka lag；
8. product-search-service Elasticsearch timeout；
9. auth-service JWK refresh failure；
10. fulfillment-service 外部供应商 503。

每套固定、唯一地关联 incident_id、trace_id、service、alertname、sop_id、logger、exception、dependency、metric/threshold、symptom、rootCause、investigation/recovery/verification。数据必须合成、安全，不含客户数据、真实 token 或凭据。

实现显式脚本：
- generate_and_upload_cls_logs.py：生成并上传对应 CLS 日志；
- publish_java_ecommerce_alerts.py：向用户明确选择的 Alertmanager 发布 10 条告警；
- seed_java_ecommerce_aiops_sops.py：通过真实认证 API 上传/索引 10 份 SOP，并等待有界时间；
- 保留一个量化服务单场景脚本时，需与十场景命名/配置一致，不能影响主流程。

脚本只通过显式 CLI 调用启动，这一动作本身就是副作用边界；Java profile 固定生成 10 套，quant profile 才支持有界 count；必须错误退出、脱敏日志并使用稳定 incident/trace 标识，不能嵌入密码。P25 扩展 P20 已有的 generate_and_upload_cls_logs.py，保持原 profile/count 调用兼容，不重复创建同名脚本。自动测试断言数量=10、所有关联字段唯一/一致、SOP 内容可索引、脚本无 import 副作用、失败不声称成功；实际“可检索”只在真实 smoke 中验证。真实 smoke 只有用户确认后执行：发布→CLS 查询→SOP 索引→告警发起诊断→证据报告。运行 backend/OpenSpec/脚本语法门禁后归档。
```

## P26：Readiness、可观测性与本地运维交付

```text
请完成第 26 个 OpenSpec change：complete-runtime-readiness-observability-and-operations。依赖全部运行时能力和 fixtures 已完成。

按 $openspec-propose → $openspec-apply-change → $openspec-verify-change → $openspec-archive-change 完整执行。OpenSpec 文档简体中文。本 change 是全平台交付门禁，不得通过删除测试、降低 strict 或使用 fake 外部结论过关。

最终探针：
- GET /health 只证明 FastAPI 进程存活，绝不连接 SQLite/Milvus/LLM/MCP。
- GET /ready 分别检查 SQLite、Milvus、Qwen、MCP；依赖失败返回 503，但响应保留每项结果/latency/safe error，便于定位。
- GET /config/check 返回脱敏的 `configuration` + `dependencies`：先验证本地 JSON/section/字段，再执行与 `/ready` 相同的 SQLite/Milvus/LLM/MCP 真实依赖检查；配置 invalid 或依赖 unreachable 都返回 503，但必须明确区分原因且不输出 secret。
- GET /health/mcp 可保留为聚焦 MCP 诊断。
- GET /metrics 使用当前项目的 JSON envelope 提供本进程请求数、失败数、平均耗时等轻量指标；不要错误宣称为 Prometheus exposition。

可观测性：
- HTTP middleware 透传或生成 X-Request-ID；结构化 JSON completion log 记录 requestId/path/status/duration。
- 扩展 indexing、chat、MCP、AIOps、background jobs 的 lifecycle logs/audits；只记录 ID、状态、分类、耗时、工具名和参数键。
- 对 password/token/key/secret/authorization 等递归脱敏；不记录 header/body、用户 query/prompt、工具参数值/输出、模型正文或凭据。

本地交付：
- scripts/start-local.sh 和 start-local.bat：检查/安装依赖，启动五个 Compose infra，uv sync，Alembic upgrade，再在主机启动官方 CLS MCP、uvicorn factory、Vite；日志写 ignored apps/backend/var。
- 启动脚本可从 JSON 把凭据传给官方 cls-mcp-server 所需进程环境，但应用本身仍不得从 env 读取项目配置。
- 根 README 使用简体中文，准确列出当前已实现功能、目录、模板复制、URL、手动启动、全量验证；不得声称未实现能力。
- docs/setup/macos.md、linux.md、windows.md 覆盖 Git/Docker/Node/npm/uv/官方 CLS MCP 安装。
- docs/operations-and-monitoring.md 和 docs/tutorials/real-log-and-alert.md 明确普通启动与真实 fixture 副作用分离。
- 清理 app.Dockerfile、project.compose.json、create_compose_app 及所有死引用。

最终自动门禁：openspec validate --all；contracts typecheck/test；backend alembic/Ruff/Pyright/pytest；frontend typecheck/test/build；docker compose config；git diff --check；macOS/Linux/Git Bash 另运行 `bash -n scripts/start-local.sh`，Windows 在 cmd/PowerShell 实机验证 start-local.bat，不把 Bash 当作 Windows 前置。测试必须在无真实 secret 的 fresh clone 通过：从模板创建 ignored local JSON，测试用 tmp_path 注入假配置，不能要求把凭据提交。

最终桌面手工链路：注册/登录→持久 Chat/SSE→上传 MD/PDF 并索引→自主知识/MCP 工具→活动告警→真实 CLS 诊断→证据/报告→案例知识→反馈。没有真实凭据时列出未执行项，不把 fake test 写成真实验收通过。全部可执行门禁通过后同步 specs 并归档。
```

## P27：OpenSpec WIKI 与最终规格闭环

```text
请完成第 27 个 OpenSpec change：publish-openspec-wiki。依赖 P01–P26 均已归档且 main specs 已同步。

使用 $openspec-propose、$openspec-apply-change、$openspec-verify-change、$openspec-archive-change 完成完整生命周期，并在本 change 实现后使用/触发 $wiki-sync（若该 skill 在当前 turn 已可用）。若新建 skill 要到下一 turn 才能被发现，则直接运行本 change 新增的 sync_wiki.py 完成同样的 active/archive/all 同步，不要因此阻塞。OpenSpec artifacts 简体中文；不要只创建空文档壳。

目标：用 VitePress 把所有 OpenSpec change 的 proposal/design/tasks/delta specs 以 include 方式发布为可导航 WIKI，并建立之后每次创建/归档的确定性同步机制。

实现要求：
- 根 npm scripts 增加 docs:dev/docs:build/docs:preview，docs/.vitepress/config.mts 提供中文导航、Sidebar。
- docs/openspec 是指向仓库 openspec 的相对符号链接；WIKI 页面不复制 artifacts 正文，使用 VitePress <!--@include: ...-->。Windows 执行前明确要求启用 Developer Mode/Git symlink 支持并验证 checkout 后仍为链接；失败时给出可操作提示，不能静默复制第二份规格制造双事实源。
- docs/changes/active/{change}/index.md 和 docs/changes/archive/{date}-{change}/index.md 使用统一 frontmatter：title、status、createdDate、archivedDate（归档时）。
- 创建 `.codex/skills/wiki-sync/SKILL.md` 和确定性 Python 脚本，支持 active、archive、all；同步页面、docs/changes/index.md、Sidebar，并验证 include 目标。
- archive 模式强制检查 delta specs 存在且已同步；只有用户显式声明时才允许 unsynced。归档页必须引用 archive 路径，禁止保留 active 路径。
- 对 P01–P26 的全部归档运行 all sync；P27 实现脚本后先运行 active sync，再验证/归档，归档后运行 archive sync，最终没有幽灵 active entry。
- `npm run docs:build` 成功不代表 include 有效，必须另行遍历每个 include target 存在。
- WIKI 不修改 OpenSpec 原 artifacts；之后 change 创建/归档均要求调用 wiki-sync。

最后再次运行全量质量门禁：openspec validate --all、backend 全检、contracts 全检、frontend 全检/build、docs build、compose config、git diff --check。对照 27 个 change、main specs、docs index、Sidebar、archive 页面逐一计数，确保无遗漏、无断链、无 active/archive 重复。验证通过后同步 P27 specs、归档 P27、再次运行 wiki-sync archive；归档同步后再完整运行 openspec validate --all、include target audit、docs build 和计数检查。
```

---

## 六、27 个提案与 65 个历史归档的覆盖关系

下表用于审计覆盖度，不要求新项目读取旧 archive 才能执行；上面的 27 个提示词已经自包含最终需求。

| 最终态提案 | 吸收的历史 archive change（日期前缀省略） |
|---|---|
| P01 | bootstrap-project-foundation；ignore-idea-files；centralize-project-configuration（只保留统一 loader 思想）；extract-user-config-and-chat-assets（配置部分）；remove-project-config-from-git-history（只保留预防规则） |
| P02 | define-api-and-sse-contracts |
| P03 | setup-sqlite-memory-repositories |
| P04 | add-user-authentication |
| P05 | add-authorization-and-tenant-isolation |
| P06 | configure-qwen-openai-provider；centralize-project-configuration（安全修正版）；fix-knowledge-indexing-experience（embedding 参数）；add-reranked-knowledge-retrieval（provider）；limit-qwen-embedding-batch-size |
| P07 | standardize-docker-compose-startup（仅 infra 思想）；setup-milvus-vector-store；refactor-local-project-startup（运行边界）；remove-compose-runtime-config |
| P08 | build-vue-app-shell；redesign-chinese-chatgpt-workspace（设计系统）；auto-dismiss-global-feedback；move-chat-history-to-workspace-sidebar（壳层） |
| P09 | durable-background-job-runtime |
| P10 | manage-knowledge-documents；add-document-chunking-strategies；refine-chat-knowledge-aiops-ui（最终 md/pdf policy） |
| P11 | run-document-indexing-jobs；add-document-chunking-strategies（索引部分）；fix-knowledge-indexing-experience；limit-qwen-embedding-batch-size（大文档回归） |
| P12 | provide-knowledge-retrieval-tool；add-reranked-knowledge-retrieval；add-hybrid-knowledge-retrieval；show-retrieval-stage-ranks；use-positive-idf-bm25；knowledge-answer-citation-view（引用数据） |
| P13 | build-knowledge-base-ui；add-document-chunking-strategies（UI）；refine-knowledge-document-layout；fix-knowledge-indexing-experience（状态）；fix-knowledge-document-scrolling；redesign/refine UI 中的知识页最终细节 |
| P14 | manage-chat-sessions |
| P15 | stream-rag-chat；audit-agent-tool-calls；fix-chat-turn-streaming（后端） |
| P16 | configure-chat-prompt-skills；extract-user-config-and-chat-assets（Chat 资产）；adopt-standard-progressive-skills；polish-chat-and-aiops-interactions（5 个 Skill 示例） |
| P17 | add-session-memory-modes |
| P18 | integrate-real-mcp-tools；manage-mcp-connections |
| P19 | build-chat-experience；knowledge-answer-citation-view（UI）；add-reranked-knowledge-retrieval/show-retrieval-stage-ranks（分数 UI）；fix-chat-turn-streaming（前端）；hide-empty-chat-placeholder；move-chat-history-to-workspace-sidebar；pace-chat-typewriter-rendering；polish/refine UI；memory/progressive Skill 控件 |
| P20 | active-alert-subscription-entry（provider/API）；generate-and-upload-cls-logs；create-ecommerce-aiops-fixtures（告警 provider 部分） |
| P21 | run-aiops-diagnosis-tasks；store-aiops-evidence-and-reports；improve-aiops-report-experience（报告生成） |
| P22 | persist-diagnosis-cases-to-knowledge-base；automate-structured-diagnosis-cases |
| P23 | build-aiops-diagnosis-ui；active-alert-subscription-entry（UI）；improve-aiops-report-experience（UI）；redesign/refine/polish UI 中的 AIOps 最终细节 |
| P24 | collect-user-feedback |
| P25 | create-ecommerce-aiops-fixtures；expand-java-ecommerce-aiops-fixtures |
| P26 | add-readiness-and-config-checks；correct-runtime-readiness-checks；observability-baseline；complete-observability-baseline；create-readme；localize-local-development-guides；refactor-local-project-startup；remove-compose-runtime-config（死引用验证） |
| P27 | add-openspec-wiki |

## 七、42 个主规格能力的落点

归档 change 反映演进过程，`openspec/specs/` 的 42 个 capability 反映需要长期保留的产品契约。最终态提案的对应关系如下：

| 主规格 capability | 最终态提案 |
|---|---|
| active-alert-subscription-entry | P20、P23 |
| agent-tool-call-audits | P15、P18、P21 |
| aiops-diagnosis-tasks | P21 |
| aiops-diagnosis-ui | P23 |
| aiops-evidence-chain | P21 |
| api-and-sse-contracts | P02，后续提案持续扩展 |
| authorization-and-tenant-isolation | P05，后续所有受保护提案持续执行 |
| automated-diagnosis-case-library | P22 |
| background-job-runtime | P09 |
| chat-experience | P19 |
| chat-memory-management | P17、P19 |
| chat-prompt-skill-configuration | P16、P19 |
| chat-sessions | P14 |
| chinese-ai-workspace-experience | P08、P13、P19、P23 |
| cls-log-generation | P20、P25 |
| diagnosis-case-knowledge | P22 |
| docker-compose-startup | P07、P26 |
| document-chunking-strategies | P10、P11、P13 |
| document-indexing-jobs | P11 |
| ecommerce-aiops-fixtures | P25 |
| frontend-end-to-end-validation | P26 |
| knowledge-answer-citation-view | P12、P19 |
| knowledge-base-ui | P13 |
| knowledge-documents | P10 |
| knowledge-retrieval-tool | P12 |
| local-development-operations-guide | P26 |
| mcp-connection-management | P18 |
| memory-repositories | P03，后续领域迁移持续扩展 |
| milvus-vector-store | P07 |
| openspec-wiki | P27 |
| platform-installation-guides | P26 |
| project-foundation | P01 |
| qwen-openai-provider | P06 |
| real-mcp-tools | P18、P21 |
| repo-hygiene | P01 |
| request-observability | P02、P15、P21、P26 |
| runtime-readiness-checks | P26 |
| shared-user-project-configuration | P01、P06、P16 |
| stream-rag-chat | P15 |
| user-authentication | P04、P08 |
| user-feedback | P24 |
| vue-app-shell | P08 |

## 八、最终完成判定

只有同时满足以下条件，才算真正从 0 到 1 复刻完成：

- 27 个 change 均存在完整 proposal/design/tasks/delta specs，tasks 全部勾选，verify 无 CRITICAL，并已同步/归档。
- 认证、所有 SQLite 资源、Milvus 搜索/删除、后台任务、MCP、AIOps、反馈和审计都有 owner/tenant 隔离测试。
- Chat 由 Agent 自主调用知识/MCP 工具；SSE、持久消息、引用、审计、Prompt/Skill、记忆和前端对账形成闭环。
- 知识文档只接受 MD/PDF，切分、durable index、Milvus、BM25L、RRF、真实 rerank 和阶段排名可解释。
- AIOps 使用真实告警和真实 MCP 工具，诊断步骤、证据、checkpoint、报告和案例均可恢复/追溯；不存在伪造结论。
- 普通启动没有日志上传、告警发布或 SOP seed 副作用；真实演示只通过显式脚本。
- 本地配置和所有凭据都未进入 Git/日志；fresh clone 可从无密钥模板开始。
- P26 的全量自动门禁通过；有环境时完成桌面真实全链 smoke，无环境项被诚实记录为未执行。
- P27 的 docs build、include 检查、Sidebar/index/archive 计数全部一致。

完成后得到的不是“看起来相似的 demo”，而是一个具备规格、实现、验证、权限、安全、真实集成和可追溯归档的完整项目。
