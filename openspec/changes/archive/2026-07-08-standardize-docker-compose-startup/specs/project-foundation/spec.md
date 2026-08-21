## ADDED Requirements

### Requirement: Infrastructure compose assets
仓库 SHALL 在 `infra` 下包含 Docker Compose 启动资源，用于本地整个项目的运行时编排。

#### Scenario: Infra directory contains compose assets
- **WHEN** 检查 `infra` 目录
- **THEN** 它 MUST 包含 Docker Compose 文件、应用程序 Dockerfile 以及本地 Compose 堆栈的文档。

#### Scenario: Root docs point to compose startup
- **WHEN** 检查根 README  
- **THEN** 它 MUST 将 Docker Compose 识别为启动完整本地项目堆栈的标准方式。
