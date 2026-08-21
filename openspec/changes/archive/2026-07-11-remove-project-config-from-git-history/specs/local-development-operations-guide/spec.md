## MODIFIED Requirements

### Requirement: Local configuration and operations reference
仓库 SHALL 提供中文操作指南，将 `config/project.json` 和 `config/user.project.json` 定义为被 Git 忽略的本地运行配置，并将 `config/project.template.json` 和 `config/user.project.template.json` 定义为可安全跟踪的无凭据模板。指南 SHALL 为真实 CLS 日志上传和 Alertmanager/AIOps 固定装置提供单独、明确的中文教程。

#### Scenario: Recipient initializes local configuration
- **WHEN** 项目接收方从新克隆开始配置项目
- **THEN** 指南 MUST 提供从两个模板复制本地配置的命令，MUST 指明填写模型与 CLS 配置的位置，并且 MUST 警告不得提交真实凭据

#### Scenario: Developer uses log and monitoring fixtures
- **WHEN** 开发者希望上传真实的 CLS 日志或创建本地 active-alert 演示
- **THEN** 中文操作指南 MUST 链接到一个专用教程，该教程将显式脚本和 Alertmanager 命令与普通应用程序启动分开列出
