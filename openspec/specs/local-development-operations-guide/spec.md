# local-development-operations-guide Specification

## Purpose
TBD - 由归档更改 create-readme 创建。归档后更新用途。
## Requirements
### Requirement: Local-first developer startup guide
仓库 SHALL 提供了一个中文的根级本地优先开发者指南，该指南从 Compose 管理的 etcd 开始，MinIO、Milvus、Attu 和 Alertmanager 依赖项，并在主机上直接运行后端，Vue 前端和官方本地 CLS MCP 服务器。该指南 MUST 用中文标识本地 URL 和状态，表明应用服务未通过 Compose 启动。

#### Scenario: Developer follows ordinary local startup
- **WHEN** 开发人员从已安装好文档中所述先决条件的全新代码库中遵循中文根 README
- **THEN** 指南 MUST 为前端依赖项、后端依赖项和迁移、基础设施依赖项、本地 MCP、后端和前端提供命令，而无需在 Compose 中使用应用服务。

#### Scenario: Developer needs infrastructure services
- **WHEN** 开发者调用记录在案的 Compose 命令
- **THEN** 它 MUST 仅启动 etcd、MinIO、Milvus、Attu 和 Alertmanager。

### Requirement: Local configuration and operations reference
仓库 SHALL 提供中文操作指南，将 `config/project.json` 和 `config/user.project.json` 定义为被 Git 忽略的本地运行配置，并将 `config/project.template.json` 和 `config/user.project.template.json` 定义为可安全跟踪的无凭据模板。指南 SHALL 为真实 CLS 日志上传和 Alertmanager/AIOps 固定装置提供单独、明确的中文教程。

#### Scenario: Recipient initializes local configuration
- **WHEN** 项目接收方从新克隆开始配置项目
- **THEN** 指南 MUST 提供从两个模板复制本地配置的命令，MUST 指明填写模型与 CLS 配置的位置，并且 MUST 警告不得提交真实凭据

#### Scenario: Developer uses log and monitoring fixtures
- **WHEN** 开发者希望上传真实的 CLS 日志或创建本地 active-alert 演示
- **THEN** 中文操作指南 MUST 链接到一个专用教程，该教程将显式脚本和 Alertmanager 命令与普通应用程序启动分开列出

### Requirement: Cross-platform local launchers
仓库 SHALL 提供了一个 macOS/Linux shell 启动器和一个 Windows 命令启动器，通过 Compose 准备本地依赖项，启动 etcd、MinIO、Milvus、Attu 和 Alertmanager，运行数据库迁移，并在主机上直接启动本地 CLS MCP 服务器、后端和前端，日志写入被忽略的本地运行时存储。启动器 user 面状态和错误文本应为中文，并且 MUST 应 MUST 打印凭证。

#### Scenario: macOS or Linux developer invokes the launcher
- **WHEN** 一名开发者在安装了所需工具的仓库根目录下运行 `scripts/start-local.sh`
- **THEN** 它通过 Compose 启动 etcd、MinIO、Milvus、Attu 和 Alertmanager，然后作为直接主机进程启动 MCP、后端和前端。

#### Scenario: Windows developer invokes the launcher
- **WHEN** 开发人员在安装了所需工具的仓库根目录中运行 `scripts\\start-local.bat`
- **THEN** 它 MUST 启动相同的依赖项和主机进程集，而无需使用 Unix shell。

#### Scenario: Developer reads launcher output
- **WHEN** 启动程序完成进程启动
- **THEN** 它会报告前端、后端和 MCP 的 URL，以及被忽略的本地日志目录，用中文和 MUST NOT 打印凭据。
