## MODIFIED Requirements

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
