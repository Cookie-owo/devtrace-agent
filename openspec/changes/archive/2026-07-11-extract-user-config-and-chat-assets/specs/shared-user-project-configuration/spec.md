## ADDED Requirements

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
基础配置 SHALL 将每个使用者不同的个人字段保留为空值，并由用户配置文件提供实际开发值。

#### Scenario: Extracted personal fields are empty in base config
- **WHEN** 检查 `config/project.json`
- **THEN** `llm.apiKey`、`llm.chatModel`、`llm.embeddingModel`、`clsMcpServer.secretId`、`clsMcpServer.secretKey`、`clsLogUpload.region`、`clsLogUpload.logsetId` 和 `clsLogUpload.topicId` MUST 为空字符串。

#### Scenario: Runtime loads personal fields from user config
- **WHEN** 应用默认加载项目配置
- **THEN** 运行时配置 MUST 从用户配置文件读取上述个人字段，并保留基础配置中的其它默认配置。
