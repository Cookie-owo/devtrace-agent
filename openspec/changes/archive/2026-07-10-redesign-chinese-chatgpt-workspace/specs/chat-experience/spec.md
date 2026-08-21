## MODIFIED Requirements

### Requirement: Persisted conversation workspace
前端 SHALL 提供一个经过身份验证的中文聊天工作区，通过共享的后端 API 合同创建、列出、选择和删除当前 user 的聊天会话。该工作区 SHALL 优先处理活动对话，同时保持会话控制紧凑且易于访问。

#### Scenario: User opens the Chat workspace
- **WHEN** 已认证的 user 打开 `/chat`
- **THEN** 前端 MUST 仅从后端加载该 user 的会话，并用中文会话控制渲染最近更新的会话。

#### Scenario: User starts and switches conversations
- **WHEN** 一个 user 开始对话或选择现有会话
- **THEN** 前端 MUST 通过后端创建或获取会话，并在聚焦的对话界面中渲染其持久化的消息历史。

#### Scenario: User deletes a conversation
- **WHEN** 一个 user 删除选定的聊天会话
- **THEN** 前端通过后端 MUST 删除它，并从可见的会话列表中移除，而不依赖 localStorage。

### Requirement: Streaming chat interaction
前端 SHALL 通过输入的聊天流式客户端发送提示，并将共享的 SSE 事件渲染为可见的中文对话进度。

#### Scenario: Assistant draft streams
- **WHEN** 流媒体端点会发出 `content.delta` 事件
- **THEN** 前端 MUST 将每个增量附加到当前的助手草稿中，并明显标识出正在生成响应，同时发送仍在进行中。

#### Scenario: Tool activity progresses
- **WHEN** 该流会发出 `tool.call` 事件
- **THEN** 前端 MUST 在不阻塞当前对话的情况下显示工具名称及其中文生命周期状态。

#### Scenario: Streaming completes or fails
- **WHEN** 该端点会发出 `complete` 或 `error` 事件，或者请求失败
- **THEN** 前端 MUST 重新协调已保存的会话，或显示规范化的中文错误，并且 MUST NOT 作为已保存的答案显示未完成的草稿。

### Requirement: Responsive chat feedback states
Chat 工作区 SHALL 在桌面和窄布局中提供中文的会话空状态、历史加载中、发送进行中、来源、工具活动和错误状态。在桌面布局中，对话外壳 SHALL 会使用可用的视口高度，并将消息滚动限制在对话记录区域，同时保持会话控件和创作器可用。

#### Scenario: Long desktop conversation remains contained
- **WHEN** 桌面对话中消息数量足够多，以超出可见工作区的高度
- **THEN** 会话列表、对话标题和创作者 MUST 在仅对话记录区域垂直滚动时仍可用，且页面 MUST NOT 随消息列表增长。

#### Scenario: Narrow screen renders chat controls
- **WHEN** 在窄视口下查看工作区
- **THEN** 会话选择、传记、创作器、源列表和工具活动控件 MUST 在不出现水平溢出的情况下仍可读且可用。
