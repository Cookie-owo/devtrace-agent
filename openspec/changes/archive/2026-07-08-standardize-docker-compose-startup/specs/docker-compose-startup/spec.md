## ADDED Requirements

### Requirement: Unified compose startup
项目 SHALL 在 `infra` 下提供一个 Docker Compose 文件，该文件是本地整个项目运行时服务的主要启动入口点。

#### Scenario: Compose 文件定义了必需的服务
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST 为后端、前端、本地 CLS MCP 服务器、Milvus、etcd、MinIO 和 Attu 定义服务

#### Scenario: Compose file starts application services from one image
- **WHEN** 检查后端、前端和 CLS MCP 服务器服务
- **THEN** 它们 MUST 使用相同的应用程序镜像构建和不同的服务命令。

### Requirement: Application image
项目 SHALL 提供 `infra/app.Dockerfile`，该功能构建一个包含后端运行时、前端构建工件和本地 MCP 服务器运行时的应用程序镜像。

#### Scenario: Backend runtime is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 安装后端 Python 依赖项并复制后端源代码、Alembic 配置和迁移文件。

#### Scenario: Frontend build output is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 构建 Vue 前端并将构建输出复制到运行时镜像中。

#### Scenario: CLS MCP runtime is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 包含 Node 运行时并安装官方的 `cls-mcp-server` 包以供本地执行。

### Requirement: CLS MCP Server local service
Compose 堆栈 SHALL 在 SSE 模式下本地运行腾讯云官方 CLS MCP 服务器。

#### Scenario: CLS MCP service uses SSE mode
- **WHEN** 检查 `cls-mcp-server` Compose 服务
- **THEN** 它设置 `TRANSPORT=sse`、`PORT=3000`、`TZ=Asia/Shanghai`、`TENCENTCLOUD_SECRET_ID` 和 `TENCENTCLOUD_SECRET_KEY`。

#### Scenario: CLS MCP service exposes SSE port
- **WHEN** 启动 Compose 堆栈
- **THEN** 的 CLS MCP 服务器服务 MUST 为 SSE 客户端公开端口 3000。

### Requirement: Milvus stack managed by compose
Compose 堆栈 SHALL 通过 Docker Compose 管理 Milvus 独立组件及其所需的依赖项。

#### Scenario: Milvus dependencies are compose services
- **WHEN** 检查 Compose 文件  
- **THEN** etcd 和 MinIO MUST 应被声明为 Milvus 所依赖的服务。

#### Scenario: Milvus and Attu ports are exposed
- **WHEN** 检查 Compose 文件
- **THEN** Milvus MUST 暴露端口 19530，并且 Attu MUST 暴露本地 UI 端口。

### Requirement: Startup exclusions
Docker Compose 启动时 SHALL NOT 管理外部日志、监控或自动文档上传工作流。

#### Scenario: External systems are excluded
- **WHEN** 检查 Compose 服务
- **THEN** 它们 MUST NOT 包括日志、监控、追踪或云可观测性后端服务。

#### Scenario: Document upload is not automatic
- **WHEN** 检查应用程序服务命令  
- **THEN** 它们在启动期间 MUST NOT 运行文档上传或摄取命令。

### Requirement: Compose documentation and environment
该项目 SHALL 文档 Docker Compose 启动并提供占位符环境值，而不会提交实际的密钥。

#### Scenario: Startup docs use compose
- **WHEN** 基础设施文档被检查
- **THEN** 它 MUST 将 Docker Compose 描述为主要的启动流程，并且 MUST NOT 要求使用 bat 或 sh 脚本作为主要的启动路径。

#### Scenario: Environment examples include CLS placeholders
- **WHEN** 环境示例文件会被检查
- **THEN** 它们 MUST 包含占位符腾讯云 CLS 凭据和 MUST NOT 包含真实的密钥值。
