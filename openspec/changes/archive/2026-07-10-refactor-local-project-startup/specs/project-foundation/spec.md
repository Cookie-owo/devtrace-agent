## MODIFIED Requirements

### Requirement: Developer documentation and project configuration
基础 SHALL 包括适用于根、后端、前端和基础设施开发的中文 README 指导和跟踪的项目配置文件。根 README SHALL 列出当前实现的 user 面产品功能。

#### Scenario: Root README documents core workflows and features
- **WHEN** 开发人员打开仓库 README
- **THEN** 它 MUST 描述了单体仓库结构、核心验证命令、本地启动工作流以及实现的认证、聊天、知识、AIOps、警报、readiness 和可观测性功能。

#### Scenario: Project config includes development configuration
- **WHEN** 项目配置文件被检查  
- **THEN** 它们 MUST 使用具体的私有仓库开发值来记录所需的键。

#### Scenario: Application code uses tracked project configuration
- **WHEN** 后端或前端应用程序代码需要项目设置
- **THEN** 它 MUST 会读取跟踪的项目配置文件，并且 MUST NOT 会读取本地机器的环境变量。

#### Scenario: Environment examples are absent
- **WHEN** 仓库配置文件被检查  
- **THEN** **`.env.example`** 文件 **MUST** **NOT** 被要求作为应用程序配置源。
