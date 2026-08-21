## Why

当前的 Compose 堆栈即使在直接主机启动是预期的日常工作流时，仍然运行应用程序服务。开发者需要一个单一且明确的启动边界：Docker 仅负责 Milvus 依赖项和本地 Alertmanager，而后端、前端和官方 CLS MCP 服务器则直接在 Windows、Linux 或 macOS 上运行。

## 什么更改

- **BREAKING** 从 `infra/compose.yaml` 中移除 `backend`、`frontend` 和 `cls-mcp-server` 服务；仅保留与 Milvus 相关的服务和 Alertmanager。
- 更新所有平台启动器，通过 Compose 启动 etcd、MinIO、Milvus、Attu 和 Alertmanager，然后在主机上启动 MCP、FastAPI 和 Vite。
- 为 Windows、Linux 和 macOS 添加单独的中文安装指南，涵盖每个项目的先决条件和命令。
- 添加针对真实 CLS 日志上传和本地 Alertmanager 告警上传的专用中文教程。
- 扩展根 README，包含完整的当前功能清单以及安装、启动和操作指南的链接。
- 通过真实浏览器交互验证前端，覆盖认证、聊天、知识和 AIOps 工作流。

## 功能

### 新功能
- `platform-installation-guides`: 中国平台特定的完整本地项目运行时先决条件和安装说明。
- `frontend-end-to-end-validation`: 可重复的浏览器接受范围，用于认证的前端工作流。

### 修改的功能
- `docker-compose-startup`: 将 Compose 服务限制为与 Milvus 相关的组件和 Alertmanager，移除应用程序和 MCP 服务。
- `local-development-operations-guide`: 为新的运行时边界和日志/警报操作更新启动器和中文教程。
- `project-foundation`: 扩展根开发者文档，包含已实现的产品功能清单。

## 影响

影响的区域包括 `infra/compose.yaml`、本地启动脚本、根目录和操作文档、Compose/文档测试、OpenSpec 规范，以及浏览器接受性证据。不需要 API 合同、数据库模式或提供方凭证源的更改。
