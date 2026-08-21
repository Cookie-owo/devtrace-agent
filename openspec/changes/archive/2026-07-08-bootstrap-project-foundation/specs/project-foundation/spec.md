## ADDED Requirements

### Requirement: Monorepo foundation layout
仓库 SHALL 暴露一个干净的单体仓库基础，包含根级别的 `apps/backend`、`apps/frontend`、`packages/api-contracts`、`infra`、`openspec` 和 `docs` 目录。

#### Scenario: Required top-level directories exist
- **WHEN** 开发者检出仓库
- **THEN** 所需的顶级单体仓库目录 MUST 存在。

#### Scenario: Legacy implementation paths are absent
- **WHEN** 基础设施将被检查
- **THEN** 对于历史后端或前端实现，不需要兼容目录 MUST 。

### Requirement: Backend Python project scaffold
后端 SHALL 应该是一个 Python 项目，位于 `apps/backend` 下，使用 `uv`、`pyproject.toml` 和 `src` 布局，并具有可导入的包名称 `super_ai`。

#### Scenario: Backend package imports by package name
- **WHEN** 后端测试从 `apps/backend` 运行
- **THEN** 代码 MUST 将应用程序包导入为 `super_ai` 而不是 `src.super_ai`。

#### Scenario: Backend quality tools are configured
- **WHEN** 后端质量命令将被运行
- **THEN** `ruff`、`pyright`、`pytest` 和 `pytest-asyncio` MUST 应通过后端项目元数据进行配置。

### Requirement: Frontend Vue project scaffold
前端 SHALL 应为在 `apps/frontend` 下使用 Vite 和 TypeScript 的 Vue 3 应用程序。

#### Scenario: Frontend project exposes standard scripts
- **WHEN** 开发人员检查 `apps/frontend/package.json`
- **THEN** 它为 Vue 应用程序提供开发、类型检查、测试和构建脚本。

#### Scenario: Frontend test directory exists
- **WHEN** 前端测试已运行
- **THEN** 测试文件 MUST 位于 `apps/frontend/tests` 下。

### Requirement: Shared API contracts package
单体仓库 SHALL 包含 `packages/api-contracts` 作为 API 合同类型在各个应用程序中的共享位置。

#### Scenario: API contract package has a typed entrypoint
- **WHEN** 消费者导入 contracts 包
- **THEN** 它从 TypeScript 源入口点 MUST 导出类型化的合约定义。

### Requirement: Developer documentation and environment examples
基础 SHALL 包括适用于根、后端和前端开发的 README 指南和环境变量示例。

#### Scenario: Root README documents core workflows
- **WHEN** 开发者打开仓库 README
- **THEN** 它 MUST 描述了单体仓库结构和核心验证命令。

#### Scenario: Environment examples avoid real secrets
- **WHEN** 环境示例文件被检查
- **THEN** 它们 MUST 包含带有占位符值的文档所需密钥，并且 MUST NOT 包含实际的敏感信息。

### Requirement: Foundation verification commands
仓库 SHALL 为 OpenSpec、后端和前端基础检查提供可执行的验证路径。

#### Scenario: OpenSpec validates the change
- **WHEN** `openspec validate --all` 会运行
- **THEN** 的 OpenSpec 配置、活动更改和规范 MUST 验证成功。

#### Scenario: Backend checks pass
- **WHEN** 后端 lint、类型检查和测试命令是从 `apps/backend` 运行的  
- **THEN** 它们在 scaffold 上成功完成。

#### Scenario: Frontend checks pass
- **WHEN** 前端类型、测试和构建命令从 `apps/frontend` 运行  
- **THEN** 它们在模板上成功完成 MUST。
