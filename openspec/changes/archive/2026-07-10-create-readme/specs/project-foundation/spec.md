## MODIFIED Requirements

### Requirement: Infrastructure compose assets
仓库 SHALL 在 `infra` 下包含 Docker Compose 启动资源，用于可选的整个项目运行时编排以及必需的本地 Milvus 依赖管理。

#### Scenario: Infra directory contains compose assets
- **WHEN** 检查 `infra` 目录
- **THEN** 它是否包含一个 Docker Compose 文件、应用程序 Dockerfile 以及可选本地 Compose 堆栈的文档。

#### Scenario: Root docs distinguish local and compose startup
- **WHEN** 根 README 将被检查
- **THEN** 它 MUST 会将直接本地启动识别为标准开发工作流，并将 Docker Compose 作为可选的全栈工作流进行链接。
