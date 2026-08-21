## 上下文

应用程序设置之前分布在 `.env.example` 文件、本地 shell 环境变量、后端提供者 JSON 和 Compose 替换中。user 明确希望这个私有仓库将具体的开发配置保留在受跟踪的文件中，并避免使用本地机器环境变量作为应用程序配置的来源。

代码库已经在后端启动、Alembic、LLM 提供者创建、SQLite 内存仓库、Milvus 向量存储设置、前端 API 客户端配置以及 Docker Compose 中具有配置消费者。因此，该更改需要一个仓库级别的配置边界，而不是独立的每服务加载器。

## Goals / Non-Goals

**目标：**

- 为直接本地启动和Docker Compose启动添加跟踪根项目配置文件。
- 从跟踪的项目配置文件中加载后端应用程序、SQLite、LLM和Milvus设置。
- 从跟踪的项目配置文件中加载前端API基础URL。
- 从应用程序配置中移除`.env.example`、基础设施`.env`、前端`VITE_*`、后端提供者JSON以及本地机器环境回退。
- 仅在官方镜像需要该运行时接口的情况下，在Compose中保留第三方容器环境变量字面量。
- 更新测试、文档和OpenSpec需求，以便未来更改保持相同的配置模型。

**非目标：**

- 无密钥管理器集成。
- 无生产环境部署或按环境配置的系统。
- 未尝试从跟踪文件中隐藏提供的私有仓库开发密钥。
- 除了配置加载外，对聊天、文档索引、Milvus 搜索或身份验证的行为没有更改。

## 决策

### 决策：使用根目录 JSON 项目配置文件

根 `config/project.json` 是规范的直接本地启动配置。根 `config/project.compose.json` 是带有服务内部主机名和路径的 Docker Compose 变体。JSON 已经被 TypeScript 和 Python 支持，无需添加另一个配置解析器依赖项。

考虑过的替代方案：
- 保留 `.env` 文件：被拒绝，因为请求的行为是停止使用本地机器环境变量作为应用程序配置。
- 保留后端专用的提供者 JSON：被拒绝，因为它在前端、Compose 和基础设施设置之外创建了第二个真相来源。

### 决策：通过启动边界传递配置路径

FastAPI 应用创建接受一个项目配置路径，将其存储在应用状态中，并传递到内存、向量存储和 LLM 提供商中。Alembic 通过 `-x project_config=...` 接受相同的配置路径用于 Compose 启动。直接本地启动使用仓库的默认配置路径。

考虑的替代方案：
- 在每个子系统中读取环境变量：被拒绝，因为这会重新引入分散的运行时配置源。
- 在模块导入期间加载外部服务：被拒绝，因为仓库指南要求在导入期间不允许进行 SQLite、Milvus、LLM 或 MCP 的连接尝试。

### 决策：从跟踪的 JSON 导入前端配置

Vue 前端导入根项目配置 JSON，并从 `frontend.apiBaseUrl` 派生 API 基础 URL。TypeScript 启用 JSON 模块解析，以便 typecheck/build 验证导入。

考虑的其他方案：
- 保留 `import.meta.env.VITE_API_BASE_URL`: 被拒绝，因为请求的行为禁止前端环境驱动的应用程序配置。
- 在构建时生成前端配置文件：被拒绝，因为对于这个私有开发仓库来说，这增加了构建的间接性且没有实际价值。

### 决策：使用字面量替换本地环境文件

`infra/compose.yaml` 不再读取 `.env` 或 `env_file`。应用服务使用 compose 项目配置文件，而官方第三方容器仍然接收字面量环境变量，因为它们的运行时接口需要这些变量。

考虑过的替代方案：
- 移除所有 Compose `environment` 块：被拒绝，因为官方 Milvus、MinIO、Attu 和 CLS MCP 服务器镜像需要设置环境变量。
- 保留已签入的基础设施 `.env`：因 user 询问为何存在多个 `.env` 文件并要求提供配置文件而被拒绝。

## Risks / Trade-offs

- [风险] 跟踪的密钥对任何有仓库访问权限的人都可见。 -> 缓解措施：这是一个明确的私有仓库决策；文档和规范将其描述为开发配置，代码仍然避免记录敏感信息。
- [风险] 前端 JSON 从外部 `apps/frontend` 导入的内容可能被工具遗漏。 -> 缓解措施：在 `tsconfig.json` 中包含根配置 JSON 并通过前端类型检查/构建覆盖它。
- [风险] Compose 和直接本地配置可能会出现偏差。 -> 缓解措施：测试断言两个配置文件都存在，并且 Compose 为应用服务引用了 compose 特定的文件。
- [风险] 第三方服务仍在 Compose 中使用环境变量。 -> 缓解措施：值是字面量 Compose 配置，而不是项目代码从本地机器读取的环境变量。

## 迁移计划

1. 添加 `config/project.json` 和 `config/project.compose.json` 并赋予具体的开发值。
2. 删除遗留的 `.env.example`、infra `.env` 和 backend provider JSON 文件。
3. 重构 backend、frontend、Alembic、Dockerfile 和 Compose 以读取跟踪的项目配置文件。
4. 更新文档、测试和 OpenSpec 规范，以反映新的配置源头。
5. 验证 backend、frontend 和 OpenSpec 的检查。
6. 在将 delta 规范同步到 main 规范后归档此更改。

## 开放问题

没有阻塞的开放问题。如果仓库策略发生变化，可以在以后作为单独的更改引入生产级的秘密处理。
