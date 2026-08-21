## MODIFIED Requirements

### Requirement: Developer documentation and project configuration
基础 SHALL 包括针对根、后端、前端和基础设施开发的指导方针和跟踪的项目配置文件。

#### Scenario: Root README documents core workflows
- **WHEN** 开发者打开仓库 README
- **THEN** 它 MUST 描述了单体仓库结构和核心验证命令。

#### Scenario: Project config includes development configuration
- **WHEN** 项目配置文件被检查  
- **THEN** 它们 MUST 使用具体的私有仓库开发值来记录所需的键。

#### Scenario: Application code uses tracked project configuration
- **WHEN** 后端或前端应用程序代码需要项目设置
- **THEN** 它 MUST 读取跟踪的项目配置文件并 MUST NOT 读取本地机器的环境变量。

#### Scenario: Environment examples are absent
- **WHEN** 仓库配置文件被检查  
- **THEN** `.env.example` 文件 MUST NOT 被要求作为应用程序配置源。
