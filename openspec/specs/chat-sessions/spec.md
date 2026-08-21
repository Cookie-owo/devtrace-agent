# chat-sessions Specification

## Purpose

定义由后端内存存储、共享契约和tenant作用域的前端状态支持的已认证聊天会话和消息生命周期行为。
## Requirements
### Requirement: Authenticated chat session lifecycle
系统 SHALL 允许经过身份验证的 users 从后端 APIs 创建、列出、读取、清除和删除他们自己的聊天会话。

#### Scenario: 创建聊天会话
- **WHEN** 已认证的 user 可使用可选标题创建聊天会话
- **THEN** 后端 MUST 将会话持久化到 SQLite 中，使用当前 user 的 owner ID 并返回已创建的会话。

#### Scenario: List chat sessions
- **WHEN** 已认证的 user 列出聊天会话
- **THEN** 后端 MUST 仅返回该 user 的会话，并按最近更新的顺序排列。

#### Scenario: Read chat session history
- **WHEN** 已认证的 user 读取其其中一个聊天会话  
- **THEN** 后端 MUST 按照创建顺序返回会话及其持久化的消息。

#### Scenario: Clear chat session history
- **WHEN** 已认证的 user 可清除其聊天会话之一
- **THEN** 后端 MUST 在保留会话记录可访问的同时，删除该会话的消息。

#### Scenario: Delete chat session
- **WHEN** 已认证的 user 删除其其中一个聊天会话  
- **THEN** 后端 MUST 从 user 的可访问会话列表中删除该会话及其消息

### Requirement: Chat message persistence
系统通过后端仓库边界持久化 SHALL 和助手聊天消息，而不是依赖前端仅存储。

#### Scenario: Append user message
- **WHEN** 已认证的 user 应用通过生命周期 API 或流式聊天发送向其聊天会话之一添加 user 消息
- **THEN** 后端 MUST 以角色 `user`、内容、元数据、owner ID、会话 ID 和创建时间戳来持久化消息

#### Scenario: Append assistant message
- **WHEN** 已认证的聊天 Agent 为 user 的聊天会话提供最终答案
- **THEN** 后端 MUST 以角色 `assistant` 、内容、元数据、owner ID、会话 ID 和创建时间戳保存消息。

#### Scenario: Message metadata preserves citations and tools
- **WHEN** 一条聊天消息在元数据中存储了知识引用参考或工具调用标识符
- **THEN** 后端 MUST 在查询历史记录时会原样返回这些结构化的元数据值。

#### Scenario: Streaming failure leaves no partial assistant message
- **WHEN** 流式聊天在最终的助手消息完成前失败
- **THEN** 后端 MUST 保留已持久化的 user 消息和 MUST NOT 持久化部分助手消息。

### Requirement: Chat title generation
系统 SHALL 从显式请求数据或第一个已保存的 user 消息中分配可读的聊天标题。

#### Scenario: Explicit title is honored
- **WHEN** 创建一个标题不为空的聊天会话
- **THEN** 后端 MUST 在去除多余空格后保留该标题。

#### Scenario: First message generates title
- **WHEN** 一个聊天会话没有有意义的标题，第一个 user 消息被追加
- **THEN** 后端 MUST 从该消息内容生成并保存一个有限的标题。

#### Scenario: Empty title fallback
- **WHEN** 既没有显式的标题，也没有 user 消息标题源
- **THEN** 后端 MUST 使用 `New chat` 作为显示标题。

### Requirement: Frontend chat session state
前端 SHALL 从经过身份验证的后端 APIs 和 MUST NOT 管理聊天会话 UI 状态，并使用 localStorage 作为主要的聊天数据源。

#### Scenario: Authenticated user loads chat sessions
- **WHEN** 前端为当前 user 加载受保护的数据
- **THEN** 它使用存储的 bearer 令牌从后端请求聊天会话

#### Scenario: User selects a chat session
- **WHEN** 的 user 在前端选择一个聊天会话
- **THEN** 的前端 MUST 从后端响应中加载该会话的历史记录。

#### Scenario: User sends streamed message
- **WHEN** 的 user 在前端发送聊天消息
- **THEN** 的前端 MUST 使用后端流式聊天端点并渲染来自 SSE 事件的流式进度。

#### Scenario: User logs out
- **WHEN** 退出 user 日志
- **THEN** 前端 MUST 清除聊天会话和可见状态中的选定聊天记录。

### Requirement: Chat session memory state lifecycle
系统 SHALL 将会话记忆状态作为当前 user 聊天会话生命周期的一部分持久化和返回。

#### Scenario: Session responses include memory state
- **WHEN** 已认证 user 创建、列出或读取自己的会话
- **THEN** 每个会话 DTO MUST 包含该会话的模式、上下文占用、压缩消息数和最后压缩时间

#### Scenario: Clearing history resets compression
- **WHEN** user 清空一个聊天会话的消息
- **THEN** 后端 MUST 清空摘要、将压缩消息数重置为零并清除最后压缩时间，同时保留该会话选择的记忆模式
