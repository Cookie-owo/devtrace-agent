# stream-rag-chat Specification

## Purpose

定义经过身份验证的、由 Agent 驱动的流式 RAG 聊天流程，该流程允许模型决定是否使用工具，发出共享的 SSE 事件，并将聊天消息持久化到后端内存中。
## Requirements
### Requirement: Agent-driven streaming chat
后端 SHALL 进程通过配置的 LangChain `create_agent` Agent 使用 Qwen 聊天模型和可用的 LangChain 工具进行认证聊天。

#### Scenario: Chat uses configured Agent
- **WHEN** 已认证的 user 向聊天会话发送聊天消息
- **THEN** 后端 MUST 调用从配置的 LLM 提供商和可用聊天工具创建的 Agent

#### Scenario: No custom LangGraph for ordinary chat
- **WHEN** 普通聊天已实现
- **THEN** 后端 MUST NOT 为聊天对话流程使用自定义的 LangGraph 状态图。

#### Scenario: Model chooses tool use
- **WHEN** 的 user 发送一条可能需要或不需要知识上下文的消息
- **THEN** 的后端 MUST 让模型决定是否调用知识检索工具，而不是作为无条件的预步骤执行检索。

### Requirement: Unified streaming chat endpoint
后端 SHALL 为发送聊天消息和流式传输聊天过程提供一个经过身份验证的 SSE 端点。

#### Scenario: Stream starts from existing session
- **WHEN** 已认证的 user 为其某个聊天会话开始流式传输消息
- **THEN** 后端 MUST 在调用 Agent 之前验证 tenant 范围的会话访问权限

#### Scenario: Stream rejects cross-tenant session
- **WHEN** 已认证的 user 向另一个 user 的会话 ID 发送消息
- **THEN** 后端 MUST 返回统一的授权错误和 MUST NOT 调用 Agent。

#### Scenario: Stream emits contract events
- **WHEN** 聊天流处于活动状态
- **THEN** 每个 SSE 帧 MUST 使用来自共享 SSE 合同的事件类型和有效载荷结构。

### Requirement: Chat stream event sequence
聊天流 SHALL 会根据需要发出标记增量、工具生命周期事件、详细参考源事件、完成事件和错误事件。

#### Scenario: Token delta is streamed
- **WHEN** 的 Agent 会发出最终答案文本
- **THEN** 的后端 MUST 按顺序流式传输 `content.delta` 事件

#### Scenario: Tool call lifecycle is streamed
- **WHEN** Agent 启动并完成或失败一个工具调用
- **THEN** 后端 MUST 流式传输 `tool.call` 事件，带有 `started`、`completed` 或 `failed` 状态和稳定的工具调用 ID。

#### Scenario: References are streamed
- **WHEN** 知识检索工具返回答案所使用的引用来源
- **THEN** 后端 MUST 流 `reference.source` 从这些引用来源中派生的事件，包括有限的 chunk 引用片段、元数据、相关性分数和知识类型（如果可用的话）。

#### Scenario: Completion is streamed
- **WHEN** 最终的助手回答已完全生成并保存
- **THEN** 后端 MUST 流式传输一个 `complete` 事件，其中包含已保存的消息和会话摘要。

#### Scenario: Errors are streamed safely
- **WHEN** 在流式传输期间 Agent 执行、工具执行或持久化失败
- **THEN** 使用统一的错误消息格式，通过后端 MUST 流式传输 `error` 事件，而不会泄露敏感信息。

### Requirement: Streaming chat persistence
后端 SHALL 通过 SQLite 存储库边界保留聊天过程。

#### Scenario: User message is persisted before Agent execution
- **WHEN** 接受流式聊天请求
- **THEN** 后端 MUST 在调用 Agent 之前将 user 的消息保存到会话中

#### Scenario: Assistant message is persisted after final answer
- **WHEN** 的 Agent 完成最终答案
- **THEN** 的后端 MUST 持久化一条包含最终内容、详细引用元数据和工具调用 ID 的助手消息。

#### Scenario: Failed stream avoids partial assistant persistence
- **WHEN** 流式传输在最终助手回答完成前失败
- **THEN** 后端 MUST NOT 保留部分助手消息

### Requirement: Frontend streaming chat consumption
前端 SHALL 通过统一的流式传输端点发送聊天提示，并从共享的 SSE 事件中渲染流式聊天进度。

#### Scenario: User sends streaming chat message
- **WHEN** 已认证的 user 从前端发送聊天提示
- **THEN** 前端 MUST 使用承载令牌和会话 ID 调用流式聊天端点。

#### Scenario: Frontend renders assistant draft
- **WHEN** `content.delta` 事件到达
- **THEN** 前端 MUST 在不使用 localStorage 作为主要聊天数据源的情况下更新可见的助手草稿。

#### Scenario: Frontend records references and completion
- **WHEN** `reference.source` 和 `complete` 事件到达
- **THEN** 前端 MUST 暴露引用参考，并从后端支持的状态中刷新或协调选定的会话历史。

### Requirement: Streaming chat tool calls are audited
流式聊天服务 SHALL 为每个 Agent `tool.call` 事件保留一个 owner 范围的审核生命周期，同时继续发出现有的共享 SSE 事件序列。

#### Scenario: 开始事件创建聊天审核记录
- **WHEN** 该聊天 Agent 会发出一个 `tool.call` 事件，状态为 `started`
- **THEN** 该服务 MUST 在发出相应的 SSE 帧之前，会创建与当前聊天会话相关的审核记录。

#### Scenario: Terminal event finalizes chat audit record
- **WHEN** 该聊天 Agent 会发出带有 `completed` 或 `failed` 状态的 `tool.call` 事件
- **THEN** 该服务 MUST 最终确定匹配的审计记录，并带有绑定结果或错误摘要，然后发出相应的 SSE 帧

#### Scenario: Audit persistence does not suppress chat output
- **WHEN** 审计持久化应独立于 Agent 的执行失败
- **THEN** 服务 MUST 应保留聊天 SSE 的生命周期和最终答案处理。

### Requirement: Chat Agent can use discovered MCP tools
流式聊天 Agent SHALL 使用已发现的 MCP 工具，并通过现有的 SSE 和工具审计路径发出它们的生命周期事件。

#### Scenario: 真实 MCP 查询在聊天中完成
- **WHEN** 已认证的 user 请求 CLS 日志，并且本地 MCP 服务器可用
- **THEN** 的 Agent MUST 调用真实 MCP 搜索工具，并将返回的记录包含在最终响应中。

### Requirement: Configured Agent system prompt
流式 RAG 聊天 Agent SHALL 在每次 Agent 调用时使用当前 user 持久化选择的系统提示词正文，并通过 `langchain.agents.create_agent`、轻量 Skill catalog 和 `load_skill` Tool 向模型提供所选 Skill 的渐进式加载能力。

#### Scenario: Agent receives selected user prompt assembly
- **WHEN** 已认证的 user 发送流式聊天消息
- **THEN** 后端 MUST 通过 Repository 加载当前 user 的聊天配置和系统提示词，并将该提示词正文传递给 Agent system prompt。

#### Scenario: Agent discovers selected user Skills
- **WHEN** 已认证的 user 选择一个或多个自己上传的 `SKILL.md` 并发送流式聊天消息
- **THEN** 后端 MUST 通过 user-scoped Repository 加载这些 Skill，使模型先看到 name 和 description，并仅能通过 `load_skill(name)` Tool 在相关时读取完整内容

#### Scenario: Unselected Skill is unavailable
- **WHEN** 当前 user 未选择某个已上传 Skill 或该 Skill 属于另一个 user
- **THEN** 本次 Agent 的 Skill catalog 和 `load_skill` registry MUST NOT 包含该 Skill

#### Scenario: Mandatory system instructions are preserved
- **WHEN** 后端装配用户提示词并创建 Agent
- **THEN** system prompt MUST 同时保留强制性的安全、引用、MCP 查询和当前时间工具调用指令，并且 MUST NOT 包含所选 Skill 的完整 Markdown 正文

### Requirement: Reasoning-aware streaming persistence
流式聊天服务 SHALL 在继续其现有的回答、工具、参考、完成和错误生命周期的同时，将模型提供的推理元数据与完整的助手响应一起持久化。

#### Scenario: Completed response includes available reasoning
- **WHEN** 一个 Agent 在完成前返回答案差异和推理差异
- **THEN** 保存的助手元数据和完整结果 MUST 包括累积的推理过程，而不将其视为最终答案内容。

### Requirement: Character-granularity model content SSE
聊天流 SHALL 将模型最终回答拆分为每个 `content.delta` 只包含一个字符的有序 SSE 事件。

#### Scenario: Multi-character model content is streamed
- **WHEN** Agent runner 产生一个包含多个字符的 `ChatAgentContentDelta`
- **THEN** 后端 MUST 按原顺序发出逐字符 `content.delta`，sequence MUST 逐个递增，持久化 assistant 正文 MUST 与原内容一致

#### Scenario: Non-content events pass through unchanged
- **WHEN** Agent runner 产生 reasoning、tool call 或 reference 事件
- **THEN** 后端 MUST 保持该事件原有负载和粒度，不得按字符拆分
