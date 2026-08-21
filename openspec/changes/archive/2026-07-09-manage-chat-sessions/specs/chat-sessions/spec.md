## ADDED Requirements

### Requirement: Authenticated chat session lifecycle
系统 SHALL 允许经过身份验证的 user 创建、列出、读取、清除和删除其自己的聊天会话从后端 API。

#### Scenario: 创建聊天会话
- **WHEN** 已认证的 user 可以创建一个可选标题的聊天会话
- **THEN** 后端 MUST 在 SQLite 中持久化会话，并使用当前 user 的 owner ID 并返回已创建的会话。

#### Scenario: List chat sessions
- **WHEN** 已认证的 user 列出聊天会话
- **THEN** 后端 MUST 仅返回该 user 的会话，并按最近更新的顺序排列

#### Scenario: Read chat session history
- **WHEN** 一个已认证的 user 读取其其中一个聊天会话  
- **THEN** 后端 MUST 按照创建顺序返回会话及其持久化的消息

#### Scenario: Clear chat session history
- **WHEN** 已认证的 user 清除其一个聊天会话  
- **THEN** 后端 MUST 删除该会话的消息，同时保持会话记录可访问。

#### Scenario: Delete chat session
- **WHEN** 已认证的 user 删除其聊天会话之一
- **THEN** 后端 MUST 从 user 可访问的会话列表中删除该会话及其消息

### Requirement: Chat message persistence
系统通过后端仓库边界持久化 SHALL 和助手聊天消息，而不是依赖前端仅存储。

#### Scenario: Append user message
- **WHEN** 已认证的 user 应用程序将 user 消息追加到其聊天会话之一
- **THEN** 后端 MUST 以角色 `user` 、内容、元数据、owner ID、会话 ID 和创建时间戳来持久化消息。

#### Scenario: Append assistant message
- **WHEN** 已认证的进程将助手消息追加到 user 的聊天会话中
- **THEN** 后端 MUST 会以角色 `assistant`、内容、元数据、owner ID、会话 ID 和创建时间戳来持久化消息。

#### Scenario: Message metadata preserves citations and tools
- **WHEN** 一条聊天消息会以知识引用参考或工具调用标识符的形式存储在元数据中
- **THEN** 后端 MUST 在查询历史记录时会原样返回这些结构化的元数据值。

### Requirement: Chat title generation
系统 SHALL 从显式的请求数据或第一个已保存的 user 消息中分配可读的聊天标题。

#### Scenario: Explicit title is honored
- **WHEN** 创建一个标题不为空的聊天会话
- **THEN** 后端 MUST 在去除多余空格后保留该标题

#### Scenario: First message generates title
- **WHEN** 一个聊天会话没有有意义的标题，第一个 user 消息被追加
- **THEN** 后端 MUST 从该消息内容生成并保存一个有限标题。

#### Scenario: Empty title fallback
- **WHEN** 既没有显式的标题，也没有 user 消息标题源
- **THEN** 后端 MUST 使用 `New chat` 作为显示标题。

### Requirement: Frontend chat session state
前端 SHALL 从经过身份验证的后端 APIs 和 MUST NOT 管理聊天会话 UI 状态，并使用 localStorage 作为主要的聊天数据源。

#### Scenario: Authenticated user loads chat sessions
- **WHEN** 前端为当前 user 加载受保护的数据
- **THEN** 它使用存储的 bearer 令牌从后端请求聊天会话。

#### Scenario: User selects a chat session
- **WHEN** 本地化助手选择前端的聊天会话
- **THEN** 前端 MUST 从后端响应中加载该会话的历史记录。

#### Scenario: User logs out
- **WHEN** 用户 user 注销
- **THEN** 前端 MUST 清除聊天会话和可见状态中的选定聊天历史记录。
