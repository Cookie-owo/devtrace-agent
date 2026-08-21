# shared-user-project-configuration Specification

## Purpose
TBD - created by archiving change extract-user-config-and-chat-assets. Update Purpose after archive.
## Requirements
### Requirement: Merged user project configuration
系统 SHALL 将基础项目配置文件与用户项目配置文件合并为运行时项目配置，基础文件提供通用默认值，用户文件只覆盖每个使用者不同的字段。

#### Scenario: User config overrides nested fields
- **WHEN** 基础配置包含通用 `llm`、`clsMcpServer` 和 `clsLogUpload` 对象，用户配置只包含这些对象中的部分字段
- **THEN** 配置加载器 MUST 递归合并对象，并让用户配置中的字段覆盖基础配置中的同路径字段。

#### Scenario: Arrays and scalar values are replaced
- **WHEN** 用户配置覆盖数组、字符串、数字或布尔值
- **THEN** 配置加载器 MUST 使用用户配置值整体替换基础配置值。

#### Scenario: Missing user config keeps base defaults
- **WHEN** 用户配置文件不存在或不包含某个字段
- **THEN** 配置加载器 MUST 使用基础配置中的值，并且 MUST NOT 从本机环境变量补充项目配置。

### Requirement: Personal configuration field extraction
本地基础配置 SHALL 提供通用默认值，本地 user 配置 SHALL 提供每个使用者不同的实际开发值，两个运行时配置文件均不得被版本控制跟踪。

#### Scenario: Extracted personal fields are empty in templates
- **WHEN** 检查 `config/project.template.json` 和 `config/user.project.template.json`
- **THEN** API key、云凭据、密码和真实 CLS 资源 ID MUST 为空字符串

#### Scenario: Runtime loads personal fields from ignored user config
- **WHEN** 应用默认加载项目配置
- **THEN** 运行时配置 MUST 从被忽略的本地 `config/project.json` 和 `config/user.project.json` 合并读取，MUST NOT 从环境变量或受版本控制模板直接读取实际凭据

#### Scenario: Local configuration is missing
- **WHEN** 新克隆尚未创建本地配置
- **THEN** 启动文档 MUST 提供从两个模板复制并填写配置的明确命令
