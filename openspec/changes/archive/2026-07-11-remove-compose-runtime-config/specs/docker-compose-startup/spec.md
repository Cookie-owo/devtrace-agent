## MODIFIED Requirements

### Requirement: Unified compose startup
项目 SHALL 在 `infra` 下提供一个 Docker Compose 文件，该文件仅管理本地容器化的基础设施服务：etcd、MinIO、Milvus、Attu 和 Alertmanager。后端、前端和官方 CLS MCP Server SHALL 通过本地启动器直接在主机上运行；Compose SHALL NOT 构建或运行应用程序镜像。

#### Scenario: Compose 文件定义了基础设施服务
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST 定义 etcd、MinIO、Milvus、Attu 和 Alertmanager 服务，并且 MUST NOT 定义 backend、frontend 或 `cls-mcp-server` 服务。

#### Scenario: Compose startup does not require local env files
- **WHEN** `infra/compose.yaml` 被检查
- **THEN** 它 MUST NOT 需要 `env_file`、`.env.example` 或 `--env-file` 作为项目应用程序配置输入。

#### Scenario: Compose excludes application image runtime
- **WHEN** 检查 `infra` 中的 Compose 启动资产
- **THEN** 它们 MUST NOT 构建、引用或要求应用程序 Dockerfile 作为本地启动前提。
