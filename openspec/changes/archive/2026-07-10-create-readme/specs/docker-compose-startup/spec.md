## MODIFIED Requirements

### Requirement: Compose documentation and project configuration
该项目将 SHALL 文档 Docker Compose 作为可选的全栈工作流，提供跨平台的直接本地启动器作为主要开发工作流，并提供具体的私有仓库开发配置值。

#### Scenario: Startup docs distinguish workflows
- **WHEN** 基础设施和根文档被检查
- **THEN** 它们 MUST 将直接本地启动描述为常规开发路径，保留完整的 Docker Compose 命令作为可选参考，并指出本地启动器仅在 Milvus 依赖项中使用 Compose。

#### Scenario: Project config includes CLS development credentials
- **WHEN** 项目配置文件被检查
- **THEN** 它们 MUST 包含私有仓库的腾讯云 CLS 开发凭据。
