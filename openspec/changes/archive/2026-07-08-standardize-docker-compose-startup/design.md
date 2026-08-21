## 上下文

仓库包含 backend、frontend、shared contracts 和 infra 目录，但启动仍然是一组独立的本地命令。下一层运行时需要一个单一的 Docker Compose 定义，可以同时启动应用服务和向量基础设施，同时将可观测性系统和文档摄入保留在启动路径之外。

Milvus 独立模式需要 etcd 和 MinIO，在通过 Docker Compose 运行时。腾讯云 CLS MCP 服务器作为官方 `cls-mcp-server` npm 包可用，并支持 SSE 模式，包含 `TRANSPORT=sse` 和 `PORT=3000`。

## Goals / Non-Goals

**目标：**

- 提供 `infra/compose.yaml` 作为主本地启动文件。
- 提供 `infra/app.Dockerfile`，该文件使用后端运行时、前端构建产物和 Node 运行时构建一个应用镜像，用于 CLS MCP 服务器。
- 使用该镜像为 `backend`、`frontend` 和 `cls-mcp-server` 服务提供服务特定命令。
- 将 Milvus、etcd、MinIO 和 Attu 作为 Compose 管理的基础设施服务。
- 通过 Compose 环境变量为 CLS MCP 服务器配置本地 SSE 模式。
- 将 Docker Compose 文档作为主要启动流程，并避免使用 bat/sh 启动脚本。

**非目标：**

- 不要运行或管理外部的日志、监控、追踪或云可观测性后端。
- 启动时不要自动上传文档或种子知识库数据。
- 不要实现生产编排、Kubernetes 或云部署清单。
- 不要将真实的腾讯云或模型提供商的密钥嵌入到提交的文件中。

## 决策

### 一个可重用的应用程序镜像

`infra/app.Dockerfile` 将由 Compose 标记为 `agent-py-app`。该镜像包含 Python 后端依赖项、前端 `dist` 输出以及全局安装的官方 `cls-mcp-server` npm 包。Compose 使用不同的命令启动后端、前端静态服务器和 CLS MCP 服务器。

考虑的替代方案：分别使用后端、前端和MCP的Dockerfile。这将改善镜像大小，但会重新创建该更改旨在移除的碎片化启动表面。

### 前端作为静态构建输出

Compose 前端服务提供从应用镜像构建的 Vite 输出。这避免了在容器启动路径中运行 Vite 开发服务器，并使本地 Compose 拓扑更接近打包部署。

考虑的替代方案：在 Compose 中运行 `npm run dev`。这有助于前端迭代，但不太适合作为整个项目的标准启动方式。

### CLS MCP 服务器在 SSE 模式下从官方 npm 包运行

应用镜像安装 `cls-mcp-server`，Compose 服务使用 `TRANSPORT=sse`、`PORT=3000`、`TZ=Asia/Shanghai` 和腾讯云凭证环境变量运行它。凭证从本地 env 文件或 shell 环境中读取，且永远不会被提交。

考虑的替代方案：在镜像构建期间克隆并构建 GitHub 仓库。npm 包是官方发布的运行时包，更容易固定版本和缓存。

### Milvus 堆栈保持独立 Compose 服务

Compose 将 `etcd`、`minio`、`milvus` 和 `attu` 保留为专用服务，并进行 health 检查、卷和端口。后端通过环境变量接收 Milvus 端点设置，但 Milvus 数据平面生命周期仍由 Compose 管理。

考虑的替代方案：将 Milvus 嵌入应用程序镜像中。这会使镜像变大，并放弃官方 Milvus 的独立拓扑。

## Risks / Trade-offs

- [风险] 单个应用程序镜像比单独的镜像更大。 -> 缓解措施：它现在保持启动简单；特定于服务的镜像可以在相同 Compose 服务名称后稍后拆分。
- [风险] Compose 构建需要网络访问权限以获取基础镜像和 npm 包。 -> 缓解措施：Dockerfile 在可行的情况下使用锁文件和固定 ARG。
- [风险] CLS 凭据对于 MCP 服务有用。 -> 缓解措施：env 示例使用占位符，Compose 不嵌入密钥。
- [风险] CI 中的 Docker Compose 验证可能没有 Docker 守护进程访问权限。 -> 缓解措施：为 YAML 结构和 Dockerfile 内容添加静态测试，并在可用时仅使用 `docker compose config`。

## 迁移计划

1. 为预期的 Compose 服务、命令、环境和 Dockerfile 内容添加静态测试。
2. 添加 `infra/app.Dockerfile`、`infra/compose.yaml`、`.dockerignore` 和 Docker 环境示例。
3. 使用启动和验证命令更新 infra 和 root README。
4. 在可用的地方验证测试、OpenSpec 和 Docker Compose 配置。
5. 在规范同步后归档此更改。

## 开放问题

没有阻塞的开放问题。生产部署、云密钥管理以及可观测性堆栈 ownership 被有意推迟。
