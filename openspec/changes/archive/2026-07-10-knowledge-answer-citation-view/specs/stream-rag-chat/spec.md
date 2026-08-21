## MODIFIED Requirements

### Requirement: Chat stream event sequence
聊天流 SHALL 会根据需要发出令牌增量、工具生命周期事件、详细的参考源事件、完成事件和错误事件。

#### Scenario: Token delta is streamed
- **WHEN** 该 Agent 会发出最终答案文本
- **THEN** 后端 MUST 按顺序流式传输 `content.delta` 事件

#### Scenario: Tool call lifecycle is streamed
- **WHEN** Agent 开始并完成或失败一个工具调用
- **THEN** 后端 MUST 流式传输 `tool.call` 事件，使用 `started`、`completed` 或 `failed` 状态和稳定的工具调用 ID。

#### Scenario: References are streamed
- **WHEN** 知识检索工具返回答案所使用的引用来源  
- **THEN** 后端 MUST 流 `reference.source` 从这些引用来源中生成的事件，包括有界 chunk 摘录、元数据、相关性分数和知识类型（如果可用）。

#### Scenario: Completion is streamed
- **WHEN** 最终的助手回答已完全生成并保存
- **THEN** 后端 MUST 流式传输一个 `complete` 事件，包含已保存的消息和会话摘要。

#### Scenario: Errors are streamed safely
- **WHEN** 在流式传输期间执行、工具执行或持久化失败
- **THEN** 使用统一的错误消息格式，通过后端 MUST 流式传输 `error` 事件，而不会泄露敏感信息。

### Requirement: Streaming chat persistence
后端 SHALL 通过 SQLite 存储库边界保留聊天过程。

#### Scenario: User message is persisted before Agent execution
- **WHEN** 一个流式聊天请求被接受
- **THEN** 在调用 Agent 之前，后端 MUST 将 user 的消息保存到会话中

#### Scenario: Assistant message is persisted after final answer
- **WHEN** 的 Agent 完成最终答案
- **THEN** 的后端 MUST 持久化一个包含最终内容、详细引用元数据和工具调用 ID 的助手消息。

#### Scenario: Failed stream avoids partial assistant persistence
- **WHEN** 流式传输在最终助手回答完成前失败
- **THEN** 后端 MUST NOT 保留部分助手消息
