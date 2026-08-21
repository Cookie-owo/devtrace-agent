# agent-tool-call-audits Specification

## Purpose

定义持久化、tenant 范围的 Agent 工具调用审计及其聊天会话 user 体验。

## Requirements

### Requirement: Agent tool calls are durably audited
后端 SHALL 为每个 Agent 工具调用保留一个 SQLite 审计条目，包含稳定的工具调用 ID、工具名称、JSON 安全参数、生命周期状态、有限的结果摘要、安全错误消息、开始时间戳、完成时间戳（如果可用）以及派生的持续时间（以毫秒为单位）。

#### Scenario: Successful chat tool call is finalized
- **WHEN** 一个聊天 Agent 工具调用开始并随后完成
- **THEN** 后端 MUST 存储一条审计记录，包含原始参数、`completed` 状态、结果摘要和非负持续时间。

#### Scenario: Failed tool call is finalized
- **WHEN** 一个 Agent 工具调用失败
- **THEN** 后端 MUST 标记其审计记录 `failed`，存储一个安全的错误摘要，并保留其完成的时间戳和持续时间。

#### Scenario: Interrupted tool call remains observable
- **WHEN** 一个工具会发出一个启动生命周期事件，但不会发出终止生命周期事件
- **THEN** 审计日志 MUST 会保留 `started` 记录，而不会虚构结果或持续时间。

### Requirement: Audit ownership and parent association are enforced
每个审计条目 SHALL 都必须具有一个 owner user ID，并且与一个父资源相关联：一个聊天会话或一个 AIOps 诊断任务。仓库的写入和读取 MUST 必须验证父资源属于提供的 owner 范围。

#### Scenario: Chat audit is scoped to the session owner
- **WHEN** 调用者列出与所属 user ID 关联的聊天会话的审计记录
- **THEN** 仓库 MUST 仅返回该 user 的会话记录

#### Scenario: Cross-tenant audit access is denied
- **WHEN** 当调用者尝试通过另一个 user 的聊天会话或诊断任务创建、更新或列出审核信息时
- **THEN** 仓库或 API MUST 拒绝访问，而不会暴露审核数据。

### Requirement: Chat audit history is available to the frontend
后端 SHALL 通过共享的 API 合同公开经过身份验证的聊天会话审计集合，前端 SHALL 在可用时显示每次调用的名称、状态、参数摘要、结果摘要或错误以及持续时间。

#### Scenario: Historical chat audit trail is displayed
- **WHEN** 已认证的 user 打开他们的一个聊天会话，其中包含已完成的工具调用
- **THEN** 前端 MUST 在页面刷新后检索并渲染持久化的审计记录。

#### Scenario: Active tool call is displayed during streaming
- **WHEN** 聊天流会发出一个 `tool.call` 生命周期事件
- **THEN** 前端 MUST 在不等待聊天流完成的情况下更新可见的工具调用过程。

### Requirement: Diagnostic tool calls use the common audit lifecycle
每个 AIOps 诊断工具调用 SHALL 都必须创建并最终确定与该诊断任务相关的 owner 范围的通用工具调用审计。

#### Scenario: Diagnostic MCP call is persisted
- **WHEN** Executor 启动并完成或失败一个 MCP 工具调用
- **THEN** 对应的审计 MUST 会存储其稳定 ID、参数、状态、绑定的结果摘要或错误、时间戳和持续时间。
