## Why

本地启动仍然分布在后端、前端、向量基础设施以及未来的 MCP 进程中。需要一个单一的 Docker Compose 入口点，以便开发人员可以一致地启动整个项目，而无需使用临时脚本或手动管理的 Milvus 依赖项。

## 哪些更改

- 将 `infra/compose.yaml` 添加为主要本地启动定义。
- 为一个可重复使用的应用程序镜像添加 `infra/app.Dockerfile`，该镜像包含后端运行时、前端构建输出和本地 MCP 服务器运行时。
- 通过不同的 Compose 命令对后端、前端静态服务和腾讯云 CLS MCP 服务器服务使用相同的应用程序镜像。
- 通过 Docker Compose 管理 Milvus 独立实例、etcd、MinIO 和 Attu。
- 在 SSE 模式下运行腾讯云官方 `cls-mcp-server`，并设置所需的环境变量。
- 将日志、监控和文档上传保持在启动生命周期之外。
- 为 Docker Compose 启动添加基础设施文档和环境示例。
- 不要将 bat/sh 脚本作为主要启动流程。

## 功能

### 新功能

- `docker-compose-startup`: 统一的 Docker Compose 启动，应用程序镜像布局，本地 CLS MCP 服务器，以及 Milvus 堆栈编排。

### 修改的功能

- `project-foundation`: 基础设施目录现在包含可执行的 Docker Compose 资产，而不仅仅是未来的注意事项。

## 影响

- 在 `infra` 下新增的 infra Compose 和 Dockerfile 文件。
- Root/backend/frontend 环境示例和 README 启动指南。
- 验证 Compose 拓扑和 Dockerfile 期望的测试，而无需访问 Docker 守护进程。
- OpenSpec 规范和归档工件。
