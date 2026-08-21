## MODIFIED Requirements

### Requirement: Tracked configuration and operations reference
仓库 SHALL 提供一份中文操作指南，并仅将 `config/project.json` 列为应用和集成的受跟踪项目配置。项目共享给接收方后，指南中标识为“需要替换”的配置项 MUST 精确为 `llm.apiKey`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId`。该指南 SHALL 为实际 CLS 日志上传和 Alertmanager/AIOps 固定装置提供单独、明确的中文指南。

#### Scenario: Recipient replaces only required shared-project values
- **WHEN** 项目接收方阅读 `docs/operations-and-monitoring.md` 中标识为“需要替换”的配置清单
- **THEN** 清单 MUST 且只能包含 `llm.apiKey`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId`，并且 MUST NOT 将 MCP 来源、Milvus 来源、MinIO 来源、Prometheus/Alertmanager 来源、应用地址、Docker 字段或演示账户设置表述为需要修改的配置项。

#### Scenario: Developer uses log and monitoring fixtures
- **WHEN** 开发者希望上传真实的 CLS 日志或创建本地 active-alert 演示
- **THEN** 中文操作指南 MUST 链接到一个专用教程，该教程将显式脚本和 Alertmanager 命令与普通应用程序启动分开列出。
