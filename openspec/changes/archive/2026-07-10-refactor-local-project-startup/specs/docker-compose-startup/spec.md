## MODIFIED Requirements

### Requirement: Unified compose startup
项目 SHALL 在 `infra` 下提供一个 Docker Compose 文件，该文件仅管理本地容器化的基础设施服务：etcd，MinIO，Milvus，Attu 和 Alertmanager。后端、前端和官方 CLS MCP Server SHALL 通过本地启动器直接在主机上运行。

#### Scenario: Compose 文件定义了基础设施服务
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST 定义 etcd、MinIO、Milvus、Attu 和 Alertmanager 服务，并 MUST NOT 定义 backend、frontend 或 `cls-mcp-server` 服务。

#### Scenario: Compose startup does not require local env files
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST NOT 需要 `env_file`、`.env.example` 或 `--env-file` 作为项目应用配置输入。

## REMOVED Requirements

### Requirement: CLS MCP Server local service
官方 CLS MCP Server SHALL 直接在运行后端和前端的本机主机上启动。

**迁移**: 使用 `scripts/start-local.sh` 或 `scripts\\start-local.bat`，它们会读取跟踪的 `clsMcpServer` 配置并本地启动官方 MCP 可执行文件。

### Requirement: Startup exclusions
Docker Compose 启动时 SHALL NOT 管理外部日志、监控、追踪、自动文档上传或应用/MCP 进程。它 MAY 管理用于活动警报开发的本地 Alertmanager 适配器所需的固定装置。

#### Scenario: External systems are excluded
- **WHEN** 检查 Compose 服务
- **THEN** 它们 MUST NOT 包括外部日志、追踪、云可观测性后端服务、后端、前端或 CLS MCP 服务。

#### Scenario: Document upload is not automatic
- **WHEN** 检查 Compose 文件和本地启动器命令  
- **THEN** 它们在启动期间 MUST NOT 运行文档上传或摄取命令

### Requirement: Compose documentation and project configuration
该项目将 SHALL 文档 Docker Compose 作为仅基础设施的工作流，提供跨平台的直接本地启动器作为主要开发工作流，并提供具体的私有仓库开发配置值。

#### Scenario: Startup docs distinguish workflows
- **WHEN** 基础设施和根文档被检查  
- **THEN** 它们 MUST 将 Compose 描述为 Milvus 相关和 Alertmanager 组件的来源，并确认本地启动器在主机上直接启动 MCP、后端和前端。

#### Scenario: Project config includes CLS development credentials
- **WHEN** 项目配置文件被检查  
- **THEN** 它们 MUST 包含私有仓库的腾讯云 CLS 开发凭据。
