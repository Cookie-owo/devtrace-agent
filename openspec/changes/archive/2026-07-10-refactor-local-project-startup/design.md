## 上下文

该仓库具有经过验证的本地优先运行时，但 `infra/compose.yaml` 仍包含从前端全栈设计继承的后端、前端和 CLS MCP 服务。平台启动器仅启动部分所需的容器基础设施，根文档未列出完整的已实现产品表面或提供特定于平台的安装步骤。

## Goals / Non-Goals

**目标：**

- 使 Compose 仅拥有本地容器化基础设施：etcd，MinIO，Milvus，Attu 和 Alertmanager。
- 使每个平台启动器启动该精确的基础设施集，然后在主机上直接运行官方的 CLS MCP 服务器，FastAPI 后端和 Vue Vite 前端。
- 提供中文的 Windows、Linux 和 macOS 安装指南，以及一个明确的真实日志和警报上传教程。
- 为实时前端添加完整的 README 功能清单和基于浏览器的验收验证。

**非目标：**

- 不要将项目凭据移出受跟踪的配置，或更改运行时 API 合同。
- 不要添加新的Docker应用程序镜像工作流或完整的Prometheus/Grafana堆栈。
- 不要将日志、警报、文档或诊断作为普通启动副作用进行播种。

## 决策

### Compose 仅限基础设施

`infra/compose.yaml` 将保留 etcd、MinIO、Milvus、Attu 和 Alertmanager。它不会定义 `backend`、`frontend` 或 `cls-mcp-server`。这为容器提供了清晰的持久化和基础设施边界，同时避免了重复的主机端口和配置路径。现有的应用程序 Dockerfile 可以作为未使用的构建资产保留；它不是运行时需求。

### 启动程序统一到一个进程模型

POSIX 和 Windows 启动器都将发出 `docker compose ... up -d etcd minio milvus attu alertmanager`，运行迁移准备，然后使用跟踪的 `clsMcpServer` 配置在主机上启动官方 MCP 可执行文件。它们保留后端/前端端口检测或其原生进程行为，并且从不打印凭据。

### 平台指南描述的是安装，而不仅仅是启动

三个单独的中文指南将说明OS-针对 Git、Docker Desktop/Engine、Node/npm、uv 以及全局官方MCP包的特定软件包安装命令，然后链接到一键启动指南。macOS 和 Linux 指南区分了包管理器示例；Windows 指南使用 winget/PowerShell 和 Docker Desktop。

### 浏览器验证是验收工件

自动化检查后，将作为已认证的操作员使用实时前端：注册/登录状态、运行时 readiness、流式聊天/会话状态、知识文档工作流、活动警报条目、AIOps 流/证据/报告以及导航。浏览器观察结果是对测试套件的补充，而非替代。

## Risks / Trade-offs

- [移除 Compose 应用服务会令 user 对旧命令感到意外] -> 文档明确说明了新的边界，脚本开始托管服务。
- [Windows 没有 POSIX 进程检查] -> 启动器使用其原生的 `start` 行为；安装指南提供停止/重试说明。
- [浏览器实时检查调用付费/远程服务] -> 使用有限的短提示，一个临时拥有文档，以及现有的真实本地警报固定装置。
- [Alertmanager 可能不包含活动警报] -> 在接受验证之前立即发布明确的真实本地数量警报。

## 迁移计划

1. 首先为仅基础设施的 Compose 边界、新指南和完整的 README 清单更新测试。
2. 移除 application/MCP Compose 服务并更新两个启动器。
3. 添加 guides/tutorials 并修改 root/infra 文档。
4. 启动 Compose 基础设施和主机服务，然后通过真实的浏览器操作进行验证。
5. 通过恢复之前的 Compose 服务定义进行回滚；持久化的 Milvus、MinIO 和 Alertmanager 卷保持不变。

## 开放问题

无。user 显式选择了仅基础设施的 Compose 和主机本地应用服务。
