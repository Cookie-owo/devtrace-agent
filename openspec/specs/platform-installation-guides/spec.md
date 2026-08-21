# platform-installation-guides Specification

## Purpose
TBD - 由归档更改 refacto-local-project-startup 创建。在归档后更新用途。
## Requirements
### Requirement: Platform-specific installation guides
仓库 SHALL 为 macOS、Linux 和 Windows 提供了单独的中文安装指南，列出了本地开发所需的每个依赖项：Git、Docker、Node/npm、uv 以及官方全局 `cls-mcp-server` 包。

#### Scenario: macOS developer reads setup guidance
- **WHEN** 开发者打开 macOS 安装指南
- **THEN** 它 MUST 提供面向 Homebrew 的安装命令和本地主机项目启动命令。

#### Scenario: Linux developer reads setup guidance
- **WHEN** 开发人员打开 Linux 设置指南
- **THEN** 它 MUST 提供包管理器和 uv 安装命令以及主机本地项目启动命令。

#### Scenario: Windows developer reads setup guidance
- **WHEN** 开发者打开 Windows 安装指南  
- **THEN** 它 MUST 提供 winget 或 PowerShell 安装命令和 Windows 启动器命令。

### Requirement: Real log and alert upload tutorial
仓库 SHALL 提供了一个中文教程，可区分普通启动与显式真实 CLS 日志上传、本地 Alertmanager 警报发布、SOP 索引以及警报驱动的 AIOps 诊断。

#### Scenario: Developer follows the operations tutorial
- **WHEN** 开发人员需要一个真实的电子商务量化事件演示
- **THEN** 教程 MUST 为 CLS 日志、Alertmanager 警报和 SOP 索引脚本提供了确切的显式命令，并描述了预期的 AIOps 证据链。
