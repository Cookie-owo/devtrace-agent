## ADDED Requirements

### Requirement: Agent-driven streaming chat
后端 SHALL 进程通过使用配置的 LangChain `create_agent` Agent 以及可用的 LangChain 工具，发送经过身份验证的聊天消息。

#### Scenario: Chat uses configured Agent
- **WHEN** 已认证的 user 向聊天会话发送聊天消息
- **THEN** 后端 MUST 调用从配置的 LLM 提供商和可用聊天工具创建的 Agent

#### Scenario: No custom LangGraph for ordinary chat
- **WHEN** 普通聊天已实现
- **THEN** 后端 MUST NOT 为聊天对话流程使用自定义的 LangGraph 状态图。

#### Scenario: Model chooses tool use
- **WHEN** user 发送一条可能需要或不需要知识上下文的消息
- **THEN** 后端 MUST 让模型决定是否调用知识检索工具，而不是作为无条件的预步骤运行检索。

### Requirement: Unified streaming chat endpoint
后端 SHALL 为发送聊天消息和流式传输聊天过程提供一个经过身份验证的 SSE 端点。

#### Scenario: Stream starts from existing session
- **WHEN** 一个已认证的 user 开始为其某个聊天会话流式传输消息
- **THEN** 后端 MUST 在调用 Agent 之前验证 tenant 范围的会话访问权限

#### Scenario: Stream rejects cross-tenant session
- **WHEN** 已认证的 user 向另一个 user 的会话 ID 发送消息
- **THEN** 后端 MUST 返回统一的授权错误和 MUST NOT 调用 Agent。

#### Scenario: Stream emits contract events
- **WHEN** 聊天流式传输已激活
- **THEN** 每个 SSE 帧 MUST 使用来自共享 SSE 合同的事件类型和有效载荷结构。

### Requirement: Chat stream event sequence
聊天流 SHALL 会根据需要发出令牌增量、工具生命周期事件、参考源事件、完成事件和错误事件。

#### Scenario: Token delta is streamed
- **WHEN** 的 Agent 会发出最终答案文本
- **THEN** 的后端 MUST 按顺序流式传输 `content.delta` 事件

#### Scenario: Tool call lifecycle is streamed
- **WHEN** Agent 启动并完成或失败工具调用  
- **THEN** 后端 MUST 流式传输 `tool.call` 事件，包含 `started`、`completed` 或 `failed` 状态和稳定的工具调用 ID。

#### Scenario: References are streamed
- **WHEN** 知识检索工具返回用于回答的引用来源  
- **THEN** 后端 MUST 流 `reference.source` 从这些引用来源中派生出的事件。

#### Scenario: Completion is streamed
- **WHEN** 最终的助手回答已完全生成并保存
- **THEN** 后端 MUST 流式传输一个 `complete` 事件，其中包含已保存的消息和会话摘要。

#### Scenario: Errors are streamed safely
- **WHEN** 在流式传输期间 Agent 执行、工具执行或持久化失败
- **THEN** 使用统一的错误消息格式，通过 MUST 后端流式传输 `error` 事件，而不会泄露敏感信息。

### Requirement: Streaming chat persistence
后端 SHALL 通过 SQLite 存储库边界保留聊天过程。

#### Scenario: User message is persisted before Agent execution
- **WHEN** 接受流式聊天请求
- **THEN** 在调用 Agent 之前，后端 MUST 将 user 的消息保存到会话中

#### Scenario: Assistant message is persisted after final answer
- **WHEN** 的 Agent 完成最终答案
- **THEN** 的后端 MUST 持久化一条包含最终内容、引用元数据和工具调用 ID 的助手消息。

#### Scenario: Failed stream avoids partial assistant persistence
- **WHEN** 流式传输在最终助手回答完成前失败
- **THEN** 后端 MUST NOT 保留部分助手消息。

### Requirement: Frontend streaming chat consumption
前端 SHALL 通过统一的流式端点发送聊天提示，并从共享的 SSE 事件中渲染流式聊天进度。

#### Scenario: User sends streaming chat message
- **WHEN** 已认证的 user 从前端发送聊天提示
- **THEN** 前端 MUST 使用承载令牌和会话 ID 调用流式聊天端点。

#### Scenario: Frontend renders assistant draft
- **WHEN** `content.delta` 事件到达
- **THEN** 前端 MUST 在不使用 localStorage 作为主要聊天数据源的情况下更新可见的助手草稿。

#### Scenario: Frontend records references and completion
- **WHEN** `reference.source` 和 `complete` 事件到达
- **THEN** 前端 MUST 暴露引用参考并从后端支持的状态中刷新或协调所选会话历史。
