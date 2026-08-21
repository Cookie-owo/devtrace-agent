## MODIFIED Requirements

### Requirement: Chat message persistence
系统通过后端仓库边界持久化 SHALL 和助手聊天消息，而不是依赖前端存储。

#### Scenario: Append user message
- **WHEN** 已认证的 user 应用通过生命周期 API 或流式聊天发送向其聊天会话中添加一个 user 消息
- **THEN** 后端 MUST 以角色 `user`、内容、元数据、owner ID、会话 ID 和创建时间戳来持久化消息

#### Scenario: Append assistant message
- **WHEN** 已认证的聊天 Agent 为 user 的聊天会话提供最终答案
- **THEN** 后端 MUST 以角色 `assistant` 、内容、元数据、owner ID、会话 ID 和创建时间戳保存消息。

#### Scenario: Message metadata preserves citations and tools
- **WHEN** 一条聊天消息在元数据中存储了知识引用参考或工具调用标识符
- **THEN** 后端 MUST 在查询历史记录时会原样返回这些结构化的元数据值。

#### Scenario: Streaming failure leaves no partial assistant message
- **WHEN** 流式聊天在最终助手消息完成前失败
- **THEN** 后端 MUST 保留已持久化的 user 消息和 MUST NOT 持久化部分助手消息。

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
- **THEN** 前端 MUST 清除聊天会话和可见状态中的选定聊天历史记录。
