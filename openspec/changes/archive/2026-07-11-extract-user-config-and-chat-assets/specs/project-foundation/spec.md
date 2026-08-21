## MODIFIED Requirements

### Requirement: Developer documentation and project configuration
基础 SHALL 包含适用于根、后端、前端和基础设施开发的中文 README 指导、基础项目配置文件和用户覆盖配置文件。根 README SHALL 列出了当前实现的 user 面向的产品功能。

#### Scenario: Root README documents core workflows and features
- **WHEN** 开发者打开仓库 README
- **THEN** 它 MUST 描述单体仓库结构、核心验证命令、本地启动流程以及实现的认证、聊天、知识、AIOps、警报、readiness 和可观测性功能。

#### Scenario: Project config separates defaults from user overrides
- **WHEN** 项目配置文件会被检查
- **THEN** `config/project.json` MUST 记录通用默认值并将每人不同字段置空，`config/user.project.json` MUST 记录当前开发者的覆盖值。

#### Scenario: Application code uses tracked merged project configuration
- **WHEN** 后端或前端应用程序代码需要项目设置
- **THEN** 它 MUST 读取跟踪的基础项目配置和用户覆盖配置的 merge 结果，并 MUST NOT 读取本地机器的环境变量。

#### Scenario: Environment examples are absent
- **WHEN** 仓库配置文件会被检查
- **THEN** `.env.example` 文件 MUST NOT 会被作为应用程序配置源要求。
