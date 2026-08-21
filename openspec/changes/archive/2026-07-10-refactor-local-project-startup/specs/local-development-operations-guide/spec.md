## MODIFIED Requirements

### Requirement: Local-first developer startup guide
仓库 SHALL 提供了一个中文的根级本地优先开发者指南，该指南从 Compose 管理的 etcd 开始，MinIO、Milvus、Attu 和 Alertmanager 依赖项，并在主机上直接运行后端，Vue 前端和官方本地 CLS MCP 服务器。该指南 MUST 会以中文标识本地 URL 和状态，表明应用服务不是通过 Compose 启动的。

#### Scenario: Developer follows ordinary local startup
- **WHEN** 开发人员按照已安装文档中要求的 Chinese root README 从全新代码库进行检出
- **THEN** 该指南 MUST 提供了前端依赖项、后端依赖项和迁移命令，以及基础设施依赖项、本地 MCP、后端和前端的命令，而无需在 Compose 中使用应用程序服务

#### Scenario: Developer needs infrastructure services
- **WHEN** 开发者调用记录在案的 Compose 命令
- **THEN** 它 MUST 仅启动 etcd、MinIO、Milvus、Attu 和 Alertmanager。

### Requirement: Tracked configuration and operations reference
仓库 SHALL 提供了一份中文操作指南，该指南记录了所有跟踪的配置部分，并标识了操作员为其他开发环境更改的值，包括 Qwen 凭据/模型、CLS 凭据和区域/日志集/主题、MCP 端点、Milvus URI、告警源以及演示账户设置。它 SHALL 还为实际 CLS 日志上传和 Alertmanager/AIOps 测试用例提供了单独的显式中文指南。

#### Scenario: Developer changes integration settings
- **WHEN** 开发人员需要将项目指向另一个模型，CLS 目标，MCP 端点，Milvus 服务，或警报提供者
- **THEN** 中文操作指南 MUST 需要识别相关的 `config/project.json` 或 `config/project.compose.json` 部分和字段名称，而不应引导开发人员到本地环境变量。

#### Scenario: Developer uses log and monitoring fixtures
- **WHEN** 开发者希望上传真实的 CLS 日志或创建本地的 active-alert 演示
- **THEN** 中国操作指南 MUST 链接到一个专用教程，该教程将显式的脚本和 Alertmanager 命令与普通应用程序启动分开列出。

### Requirement: Cross-platform local launchers
仓库 SHALL 提供了一个 macOS/Linux shell 启动器和一个 Windows 命令启动器，它们通过 Compose 准备本地依赖项，启动 etcd、MinIO、Milvus、Attu 和 Alertmanager，运行数据库迁移，并在主机上直接启动本地 CLS MCP 服务器、后端和前端，日志写入被忽略的本地运行时存储。启动器 user 面向的状态和错误文本 MUST 为中文，并且 MUST NOT 打印凭证。

#### Scenario: macOS or Linux developer invokes the launcher
- **WHEN** 一名开发者在安装了所需工具的仓库根目录中运行 `scripts/start-local.sh`
- **THEN** 它通过 Compose 启动 etcd、MinIO、Milvus、Attu 和 Alertmanager，然后作为直接主机进程启动 MCP、后端和前端。

#### Scenario: Windows developer invokes the launcher
- **WHEN** 开发人员从存储库根目录运行 `scripts\\start-local.bat` 并安装了所需工具
- **THEN** 它 MUST 启动相同的依赖项和主机进程集，而无需使用 Unix shell。

#### Scenario: Developer reads launcher output
- **WHEN** 启动程序完成进程启动
- **THEN** 它会报告前端、后端和 MCP 的 URL，以及被忽略的本地日志目录，用中文和 MUST NOT 打印凭据。
