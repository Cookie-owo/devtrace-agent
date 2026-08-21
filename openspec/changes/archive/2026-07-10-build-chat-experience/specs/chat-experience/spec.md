## ADDED Requirements

### Requirement: Persisted conversation workspace
前端 SHALL 通过共享的后端 API 合同，为当前 user 提供经过身份验证的聊天工作区，用于创建、列出、选择和删除聊天会话。

#### Scenario: User opens the Chat workspace
- **WHEN** 已认证的 user 打开 `/chat`
- **THEN** 前端 MUST 仅从后端加载该 user 的会话，并渲染最近更新的会话。

#### Scenario: User starts and switches conversations
- **WHEN** 一个 user 开始对话或选择现有会话
- **THEN** 前端 MUST 通过后端创建或获取会话并渲染其持久化的消息历史记录。

#### Scenario: User deletes a conversation
- **WHEN** 一个 user 删除所选的聊天会话
- **THEN** 前端 MUST 通过后端删除它，并从可见的会话列表中移除，而不依赖 localStorage。

### Requirement: Streaming chat interaction
前端 SHALL 通过输入的聊天流客户端发送提示，并将共享的 SSE 事件渲染为可见的对话进度。

#### Scenario: Assistant draft streams
- **WHEN** 流式传输端点会发出 `content.delta` 事件
- **THEN** 前端 MUST 在发送进行时，会将每个增量追加到当前的助手草稿中。

#### Scenario: Streaming completes
- **WHEN** 该端点会发出一个 `complete` 事件
- **THEN** 前端 MUST 与后端保存的消息同步活动会话，并刷新其工具调用审计列表。

#### Scenario: Streaming fails
- **WHEN** 端点会发出 `error` 事件或请求失败
- **THEN** 前端 MUST 显示规范化的安全错误信息，并且 MUST NOT 作为已保存的答案显示未完成的助手草稿。

### Requirement: Answer context presentation
聊天工作区 SHALL 会安全地渲染 Markdown 答案，并从共享消息和 SSE 合同中暴露源代码和工具调用上下文。

#### Scenario: Assistant answer contains Markdown
- **WHEN** 一个助手消息包含 Markdown 语法
- **THEN** 前端 MUST 在移除不可信的原始 HTML 的同时渲染支持的格式

#### Scenario: Answer uses knowledge references
- **WHEN** 一个流或持久化消息包含引用参考
- **THEN** 前端 MUST 显示源标题，并将其与工具调用活动区分开来。

#### Scenario: Tool call progresses
- **WHEN** 一个流会发出 `tool.call` 事件，或者活动会话具有工具调用审计
- **THEN** 前端 MUST 显示每个工具名称、生命周期状态以及可用的绑定结果或错误摘要。

### Requirement: Responsive chat feedback states
聊天工作区 SHALL 在桌面和窄布局中提供清晰的会话空状态、历史加载中状态、发送进行中状态和错误状态。

#### Scenario: User has no conversations
- **WHEN** 后端返回一个空的会话集合
- **THEN** 工作区 MUST 渲染一个空的对话状态，并提供一个可用命令以开始新对话。

#### Scenario: Send is in progress
- **WHEN** 一个聊天发送正在进行中
- **THEN** 编辑器 MUST 防止重复发送并显示响应正在流式传输。

#### Scenario: Narrow screen renders chat controls
- **WHEN** 在窄视口下查看工作区时
- **THEN** 会话选择、转录、创作器、源列表和工具活动控件 MUST 在不出现水平溢出的情况下仍可读取和操作。
