# Runtime Readiness Checks Specification

## Purpose

为 Vue 工作区定义安全的密钥聚合运行时 readiness 检查和轻量级后端连接。

## Requirements

### Requirement: Aggregate secret-safe readiness check
后端 SHALL 暴露一个类型化的 `/ready` 端点，该端点独立检查 SQLite、Milvus、配置的 LLM 提供商以及本地 MCP 服务器，而不会暴露凭据。

#### Scenario: All required dependencies are ready
- **WHEN** SQLite, Milvus, 配置的 LLM 提供商以及配置的 MCP 服务器可用
- **THEN** `/ready` MUST 在可用时返回成功的 ready 结果，并包含安全组件元数据和延迟或工具计数信息

#### Scenario: A dependency is unavailable
- **WHEN** 一个或多个必需的依赖项无法完成其 readiness 检查
- **THEN** `/ready` MUST 在保留其他组件结果的同时，对每个受影响的组件返回降级结果和安全错误，并返回非成功 HTTP 状态。

#### Scenario: 结果包含提供者配置上下文
- **WHEN** `/ready` 包含 LLM 配置上下文
- **THEN** 它 MUST 仅包含安全的提供者/模型/基础 URL 信息，以及 MUST NOT 包含一个 API 键或其他密钥。

### Requirement: Live lightweight workspace connectivity
前端 SHALL 在工作区挂载时获取轻量级后端 health，并从该结果中渲染标题栏的连接状态。

#### Scenario: Backend health succeeds
- **WHEN** 前端可以获取轻量级 `/health` 端点
- **THEN** 工作区标题 MUST 渲染连接状态，且响应 MUST 不依赖 SQLite、Milvus、Qwen 或 MCP 的可用性。

#### Scenario: Backend health fails
- **WHEN** 前端无法获取成功的轻量级 health 响应
- **THEN** 工作区标题 MUST 会渲染为降级状态，但不会阻止已认证的工作区路由加载。

### Requirement: Safe configuration diagnostics
后端 SHALL 暴露了一个未经身份验证的类型化 `/config/check` 端点，该端点验证跟踪的配置并为 SQLite、Milvus、Qwen 和 MCP 报告安全依赖项诊断信息。

#### Scenario: Configuration and dependencies are valid
- **WHEN** 所有需要跟踪的配置部分都已解析，且每个依赖项都可用
- **THEN** `/config/check` MUST 返回一个成功结果，标识安全的配置上下文和就绪的依赖项结果。

#### Scenario: Configuration or dependency is invalid
- **WHEN** 必需的配置部分无效，或依赖项无法访问  
- **THEN** `/config/check` MUST 返回一个非成功诊断结果，该结果标识受影响的组件，而不会序列化密钥、凭据或原始敏感配置值。
