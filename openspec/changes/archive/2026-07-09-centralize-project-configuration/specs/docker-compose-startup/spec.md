## MODIFIED Requirements

### Requirement: Unified compose startup
项目 SHALL 在 `infra` 下提供一个 Docker Compose 文件，该文件是本地整个项目运行时服务的主要启动入口点。

#### Scenario: 组合文件定义了所需的服务
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST 为后端、前端、本地 CLS MCP 服务器、Milvus、etcd、MinIO 和 Attu 定义服务。

#### Scenario: Compose file starts application services from one image
- **WHEN** 检查后端、前端和 CLS MCP 服务器服务
- **THEN** 它们 MUST 使用相同的应用程序镜像构建和不同的服务命令。

#### Scenario: Compose startup does not require local env files
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST NOT 需要 `env_file`、`.env.example` 或 `--env-file` 作为项目应用配置输入。

### Requirement: Application image
项目 SHALL 提供 `infra/app.Dockerfile`，该功能构建一个包含后端运行时、前端构建制品、本地项目配置和本地 MCP 服务器运行时的应用程序镜像。

#### Scenario: Backend runtime is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 安装后端 Python 依赖项并复制后端源代码、Alembic 配置和迁移文件。

#### Scenario: Frontend build output is included
- **WHEN** 检查应用程序的 Dockerfile  
- **THEN** 它 MUST 构建 Vue 前端并将构建输出复制到运行时镜像中。

#### Scenario: Project configuration is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 将根项目配置文件复制到运行时镜像中。

#### Scenario: CLS MCP runtime is included
- **WHEN** 检查应用程序的 Dockerfile
- **THEN** 它 MUST 包含 Node 运行时并安装官方 `cls-mcp-server` 包以用于本地执行。

### Requirement: Compose documentation and project configuration
该项目 SHALL 文档 Docker Compose 启动并提供具体的私有仓库开发配置值。

#### Scenario: Startup docs use compose
- **WHEN** 基础设施文档被检查
- **THEN** 它 MUST 将 Docker Compose 描述为主要的启动流程，并 MUST NOT 要求使用 bat 或 sh 脚本作为主要的启动路径。

#### Scenario: Project config includes CLS development credentials
- **WHEN** 项目配置文件将被检查  
- **THEN** 它们 MUST 将包含私有仓库的腾讯云 CLS 开发凭据
