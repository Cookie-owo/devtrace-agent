## 原因

Compose 现在只启动 etcd、MinIO、Milvus、Attu 和 Alertmanager；后端、前端及官方 CLS MCP Server 均由主机本地启动器直接运行。因此，遗留的 Compose 应用镜像和其专用配置变体不再有运行时消费者，继续保留会造成两套配置来源和错误的容器化应用预期。

## 更改内容

- **破坏性变更**：删除 `config/project.compose.json`、`infra/app.Dockerfile` 及其相关的 `create_compose_app()` 路径；不提供兼容层或回退配置。
- 将应用和工具的受跟踪配置统一为 `config/project.json`。
- 更新 Compose、配置和运维文档的验证，确认 Compose 只管理五个基础设施服务，且文档不再引用 Compose 专用应用运行时或配置。
- 项目共享给接收方后，`docs/operations-and-monitoring.md` 的“需要替换”配置清单仅列出六个实际由接收方提供的字段：`llm.apiKey`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId`。

## 功能

### 新功能

无。

### 修改的功能

- `docker-compose-startup`：移除已废弃的应用镜像要求，明确 Compose 仅承担五个基础设施服务。
- `local-development-operations-guide`：将受跟踪配置和运维说明统一到 `config/project.json`，不再列出 Compose 专用配置文件；面向接收方的替换清单只包含六个必需自备值，不将其他服务来源或运行参数表述为需修改项。

## 影响

受影响的区域包括 `config/project.compose.json`、`infra/app.Dockerfile`、创建 Compose 应用配置的代码路径、相关测试以及本地开发和运维文档。不会改变 Compose 所管理的五个基础设施服务、应用 API 或外部服务凭据的配置值；仅收紧共享后运维指南中向接收方标注的替换字段范围。
