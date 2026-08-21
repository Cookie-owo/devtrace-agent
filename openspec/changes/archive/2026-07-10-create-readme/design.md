## 上下文

该仓库直接支持本地运行时：`uv` 启动 FastAPI 后端，Vite 启动 Vue 前端，官方的 CLS MCP 包在端口 3000 上运行，Milvus 仅需要其 etcd 和 MinIO 依赖项来自 Compose。根 README 和基础设施 README 当前描述了完整的 Compose 堆栈作为标准路径，而操作设置和跟踪的配置则分布在代码、配置和特定于 fixture 的文档中。

## Goals / Non-Goals

**目标：**

- 建立一个以本地为主的首次使用路径，仅通过 Docker 启动所需的 Milvus 依赖，并在主机上直接启动应用程序进程。
- 使每个可配置的跟踪 JSON 部分和特定环境的凭证 /identifier 可被发现，而无需引入 `.env` 文件。
- 将普通的本地启动与显式的实际 CLS 上传和 Alertmanager/AIOps 测试夹具工作流程分开。
- 提供可工作的 macOS/Linux 和 Windows 启动器，用于准备依赖项，迁移 SQLite，启动本地 MCP 服务器、后端和前端，并在忽略的后端运行时存储下写入日志。

**非目标：**

- 不要移除或重新设计现有的完整 Compose 堆栈。
- 在正常启动期间，不要自动生成日志、警报、知识文档或诊断信息。
- 不要添加完整的 Docker 监控堆栈、服务监督器、安装程序或生产部署流程。

## 决策

### 根 README 是一个索引；操作仍是一个单独的指南

根目录 README 将包含简短的本地优先序列、URL、验证命令和链接。专用的操作指南将描述配置和实际的日志/监控固定装置，以确保正常应用程序启动保持可读且无副作用。因为这会妨碍快速运行UI的路径，所以拒绝在 README 中复制完整的操作说明。

### 仅通过 Compose 启动 Milvus 依赖项

启动器通过 `etcd`、`minio` 和 `milvus` 启动 `infra/compose.yaml`，然后直接运行 MCP、后端和 Vite。Alertmanager 在普通启动中被省略，因为它仅在显式的监控夹具中需要。拒绝启动每个 Compose 服务，因为这忽略了所需的本地优先工作流；要求手动安装 Milvus 被拒绝，因为该项目已经通过 Compose 管理其支持的依赖堆栈。

### 脚本读取跟踪的 JSON 并具有可见的处理日志

macOS/Linux 启动器使用 Python JSON 解析将 `clsMcpServer` 值传递给官方外部 MCP 进程；Windows 启动器使用内置的 PowerShell JSON 解析实现相同目的。这是外部进程配置边界，而应用程序代码继续仅读取跟踪的配置。每个启动器将进程输出写入 `apps/backend/var/`，并作为单独的主机进程启动前端/后端/MCP。

### 文档测试检查的是契约，而不是文字格式

后端文档测试将验证启动器、关键本地命令、配置参考覆盖范围以及显式排除项的存在。Shell 语法通过 `bash -n` 进行检查；由于开发环境是 macOS，Windows 脚本验证为静态验证。

## Risks / Trade-offs

- [缺少先决工具] -> README 在启动前列出精确的`uv`、Node/npm、Docker Desktop和官方MCP安装检查。
- [主机端口已被占用] -> 启动器会识别URL和日志位置；指南包含在重试前停止进程的命令。
- [CLS凭据必须暴露给外部MCP进程] -> 启动器仅从跟踪的私有项目配置中获取它们，且从不打印这些凭据。
- [Windows引号与POSIX shell不同] -> 保持Windows启动器的命令导向性，并仅使用PowerShell进行确定性的JSON提取。

## 迁移计划

1. 添加启动器和文档测试。
2. 将根 README 的“以 Compose 为先”内容替换为“以本地为先”的指南，并链接到专用的操作文档。
3. 将 `infra/README.md` 重新定位为可选的全栈参考，同时保留其 Compose 指令。
4. 运行静态脚本、文档、后端、前端和 OpenSpec 验证。现有的 user 可以继续使用未更改的 Compose 命令。

## 开放问题

无。仓库已具备所需的本地过程命令、跟踪的配置布局、CLS MCP 运行时以及由 Compose 管理的 Milvus 依赖项。
