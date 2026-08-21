# Request Observability Specification

## Purpose

为应用操作定义安全的请求相关日志和本地聚合请求指标。

## Requirements

### Requirement: Correlated safe request completion logs
后端 SHALL 会分配或尊重请求相关标识符，将其作为 `X-Request-ID` 返回，并在请求完成和请求错误时发出结构化的 JSON 生命周期日志，包含请求 ID、方法、路径、状态、延迟和安全错误类别（如适用）。

#### Scenario: Request has no correlation id
- **WHEN** 一个请求省略了 `X-Request-ID`
- **THEN** 后端 MUST 生成一个，将其包含在响应头中，并在该请求发出的完成和错误日志中使用它。

#### Scenario: Request supplies a correlation id
- **WHEN** 一个请求提供 `X-Request-ID`
- **THEN** 后端 MUST 返回相同的 id，并将其包含在所有请求范围内的生命周期日志中。

#### Scenario: Request contains credentials
- **WHEN** 请求具有授权或提供者凭据
- **THEN** 请求生命周期日志 MUST NOT 包括请求头、承载令牌、API 密钥、请求体或原始异常消息。

### Requirement: Local operational request metrics
后端 SHALL 通过轻量级指标端点公开本地聚合的请求总数、失败次数和延迟。

#### Scenario: Requests complete
- **WHEN** 通过应用程序完成的请求
- **THEN** 的指标端点 MUST 会报告汇总的请求次数、失败次数和延迟数据，而不包含敏感的请求内容。

### Requirement: Correlated critical-work lifecycle logs
后端 SHALL 会为文档索引、聊天/AIOps Agent 执行和本地 MCP 工具调用生成结构化、安全的生命周期日志，当可用时使用活动请求 ID。

#### Scenario: Index task runs
- **WHEN** 一个文档索引任务开始、成功或失败
- **THEN** 后端 MUST 在记录其任务/文档标识符、生命周期状态、完成时的持续时间以及失败时的错误类别时，不包含文档内容或嵌入数据。

#### Scenario: Agent execution runs
- **WHEN** 聊天或 AIOps 执行开始、完成或失败
- **THEN** 后端 MUST 记录所属会话或诊断任务的标识符、生命周期状态和持续时间，但不包括 user 消息内容、计划、工具参数或模型输出。

#### Scenario: MCP tool call runs
- **WHEN** 本地 MCP 工具调用开始、完成或失败
- **THEN** 后端 MUST 记录工具名称、生命周期状态、参数键名、持续时间以及错误类别，而不序列化工具参数值、工具输出、提供者密钥或 CLS 凭据。
