# project-foundation Specification

## Purpose

为新的后端、前端、共享契约、基础设施、文档和质量工作流定义清洁的单体仓库基础。
## Requirements
### Requirement: Monorepo foundation layout
仓库 SHALL 暴露一个干净的单体仓库基础，包含根级别的 `apps/backend`、`apps/frontend`、`packages/api-contracts`、`infra`、`openspec` 和 `docs` 目录。

#### Scenario: Required top-level directories exist
- **WHEN** 开发者检出仓库
- **THEN** 所需的顶级单体仓库目录 MUST 存在。

#### Scenario: Legacy implementation paths are absent
- **WHEN** 基础结构进行检查
- **THEN** 对于历史后端或前端实现，不需要兼容目录 MUST 。

### Requirement: Backend Python project scaffold
后端 SHALL 应为一个 Python 项目，位于 `apps/backend` 下，使用 `uv`、`pyproject.toml` 和 `src` 布局，并具有可导入的包名称 `super_ai`。

#### Scenario: Backend package imports by package name
- **WHEN** 后端测试从 `apps/backend` 运行
- **THEN** 代码 MUST 将应用程序包导入为 `super_ai` 而不是 `src.super_ai`。

#### Scenario: Backend quality tools are configured
- **WHEN** 后端质量命令将被运行
- **THEN** `ruff`、`pyright`、`pytest` 和 `pytest-asyncio` MUST 应通过后端项目元数据进行配置。

### Requirement: Frontend Vue project scaffold
前端 SHALL 必须是一个在 `apps/frontend` 下的使用 Vite 和 TypeScript 的 Vue 3 应用程序。

#### Scenario: Frontend project exposes standard scripts
- **WHEN** 开发人员检查 `apps/frontend/package.json`
- **THEN** 它 MUST 为 Vue 应用程序提供开发、类型检查、测试和构建脚本。

#### Scenario: Frontend test directory exists
- **WHEN** 前端测试已运行
- **THEN** 测试文件 MUST 位于 `apps/frontend/tests` 下。

### Requirement: Shared API contracts package
单体仓库 SHALL 包含 `packages/api-contracts` 作为 API 合同类型在各个应用程序中的共享位置。前端和后端实现 MUST 使用此包作为 HTTP 响应信封、错误代码、OpenAPI 路径合同和 SSE 事件负载的权威来源。

#### Scenario: API contract package has a typed entrypoint
- **WHEN** 消费者导入 contracts 包
- **THEN** 它 MUST 从 TypeScript 源入口点导出类型化的合约定义。

#### Scenario: 合约包定义了 API 和 SSE 表面
- **WHEN** **`packages/api-contracts`** 被检查
- **THEN** 它 MUST 定义 HTTP 响应、错误、OpenAPI 和 SSE 事件合约导出。

#### Scenario: Applications do not invent event structures
- **WHEN** 前端或后端代码需要聊天流或 AIOps 诊断事件
- **THEN** 它 MUST 应该使用共享的 SSE 事件契约，而不是创建临时的事件有效载荷结构。

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

### Requirement: Foundation verification commands
仓库 SHALL 为 OpenSpec、后端和前端基础检查提供可执行的验证路径，包括后端数据库迁移和仓库测试。

#### Scenario: OpenSpec validates the change
- **WHEN** `openspec validate --all` 会运行
- **THEN** 的 OpenSpec 配置、活动更改和规范 MUST 已成功验证。

#### Scenario: Backend checks pass
- **WHEN** 后端 lint、类型、迁移和测试命令是从 `apps/backend` 运行的
- **THEN** 它们在 scaffold 上成功完成。

#### Scenario: Frontend checks pass
- **WHEN** 前端类型、测试和构建命令从 `apps/frontend` 运行
- **THEN** 它们在模板上成功完成 MUST。

### Requirement: Infrastructure compose assets
仓库 SHALL 在 `infra` 下包含 Docker Compose 启动资源，用于可选的全项目运行时编排和必需的本地 Milvus 依赖管理。

#### Scenario: Infra directory contains compose assets
- **WHEN** 检查 `infra` 目录
- **THEN** 它 MUST 包含一个 Docker Compose 文件、应用程序 Dockerfile 以及可选本地 Compose 堆栈的文档。

#### Scenario: Root docs distinguish local and compose startup
- **WHEN** 根 README 将被检查
- **THEN** 它 MUST 会将直接本地启动识别为标准开发工作流，并将 Docker Compose 作为可选的全栈工作流进行链接。

