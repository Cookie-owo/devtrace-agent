## Why

该项目现在具有一个可工作的本地后端、前端、MCP 服务器、Milvus 依赖项、Alertmanager fixture 和真实的 CLS 工作流，但根文档仍然将完整的 Docker Compose 堆栈作为主要路径。开发人员需要一条清晰的以本地优先的路径和操作指南，明确标识出每个必须更改的跟踪配置值，以便用于其他环境。

## 哪些更改

- 为后端、前端、本地 CLS MCP 服务器以及 Docker 管理的 Milvus 依赖项，围绕本地直接启动重写根 README。
- 为 CLS 日志上传、Alertmanager 固定装置和 AIOps 示范数据添加单独的操作指南，而不是将这些副作用放在普通启动中。
- 记录所有跟踪的配置部分和环境特定值，包括模型密钥、CLS 凭据和目标 ID、MCP 端点、Milvus、警报源和示范账户设置。
- 为 macOS/Linux 和 Windows 添加仓库根目录的一键启动程序，这些程序在依赖项安装后仅启动本地应用服务。
- 明确记录完整的项目 Docker Compose 堆栈不属于本地优先工作流。

## 功能

### 新功能
- `local-development-operations-guide`: 一个经过测试的本地优先的入门和操作指南，包含跨平台应用程序启动命令。

### 修改后的功能
- `project-foundation`: 使根开发指南以本地优先的方式进行，同时保留记录在案的可选完整 Compose 工作流。
- `docker-compose-startup`: 使直接的本地启动器成为主要的开发路径，并保留 Compose 用于 Milvus 依赖项和可选的全栈使用。

## 影响

受影响的文件包括根目录的 README、本地操作文档、仓库根目录的启动脚本以及文档验证测试。应用程序运行时、提供者集成和 Compose 服务保留其现有行为。
