## ADDED Requirements

### Requirement: Local-first developer startup guide
仓库 SHALL 提供了一个根级别的本地优先开发者指南，该指南仅启动 Compose 管理的 Milvus 依赖项，并在主机上直接运行后端、Vue 前端和官方本地 CLS MCP 服务器。该指南 MUST 会标识本地 URL，并说明完整的项目 Docker Compose 对于普通开发是可选而非必需的。

#### Scenario: Developer follows ordinary local startup
- **WHEN** 一个开发者从安装了已记录先决条件的全新代码库开始
- **THEN** 该指南 MUST 提供了前端依赖项、后端依赖项和迁移的命令，Milvus 依赖项、本地 MCP、后端和前端，而无需启动完整的项目 Compose。

#### Scenario: Developer needs the full stack
- **WHEN** 开发人员选择可选的完整 Compose 工作流  
- **THEN** 该指南 MUST 链接到基础设施文档，但不将其作为必需的本地开发路径呈现。

### Requirement: Tracked configuration and operations reference
仓库 SHALL 记录所有跟踪的配置部分，并标识操作员在另一个开发环境中更改的值，包括 Qwen 凭据/模型，CLS 凭据和区域/日志集/主题，MCP 端点，Milvus URI，警报源和演示账户设置。它 SHALL 为实际 CLS 日志上传和 Alertmanager/AIOps 布景提供单独的明确指南。

#### Scenario: Developer changes integration settings
- **WHEN** 开发人员需要将项目指向另一个模型，CLS 目标，MCP 端点，Milvus 服务，或警报提供者
- **THEN** 操作指南 MUST 需要识别相关的 `config/project.json` 或 `config/project.compose.json` 部分和字段名称，而不应引导开发人员到本地环境变量。

#### Scenario: Developer uses log and monitoring fixtures
- **WHEN** 开发人员想要上传真实的 CLS 日志或创建本地的 active-alert 演示
- **THEN** 运维指南 MUST 将显式的脚本和先决条件 Alertmanager 命令与普通应用程序启动分开列出

### Requirement: Cross-platform local launchers
仓库 SHALL 提供了一个 macOS/Linux shell 启动器和一个 Windows 命令启动器，用于准备本地依赖项，仅启动 Milvus Compose 依赖项，运行数据库迁移，并在忽略的本地运行时存储下启动本地 CLS MCP 服务器、后端和前端。

#### Scenario: macOS or Linux developer invokes the launcher
- **WHEN** 开发人员在安装了所需工具的仓库根目录下运行 `scripts/start-local.sh`
- **THEN** 它通过 Compose 仅启动 etcd、MinIO 和 Milvus，然后作为直接主机进程启动 MCP、后端和前端。

#### Scenario: Windows developer invokes the launcher
- **WHEN** 开发人员在安装了所需工具的仓库根目录中运行 `scripts\\start-local.bat`
- **THEN** 它 MUST 会启动相同的依赖项和主机进程，而无需使用 Unix shell。

#### Scenario: Developer reads launcher output
- **WHEN** 无论启动程序完成进程启动
- **THEN** 它会报告前端、后端和 MCP 的 URL，以及被忽略的本地日志目录和 MUST NOT 打印凭据。
