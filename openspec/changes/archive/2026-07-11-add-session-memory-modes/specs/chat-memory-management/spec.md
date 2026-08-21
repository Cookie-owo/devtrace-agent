## ADDED Requirements

### Requirement: Session-scoped memory mode
系统 SHALL 为每个聊天会话独立持久化记忆模式，支持 `every_30_turns`、`context_70_percent` 和 `manual`，新会话 MUST 默认使用 `every_30_turns`。

#### Scenario: Different sessions use different modes
- **WHEN** 同一 user 为两个会话选择不同的记忆模式
- **THEN** 后端 MUST 分别保存并应用各自的模式，任一会话的修改 MUST NOT 改变另一会话

#### Scenario: New session uses default mode
- **WHEN** user 创建聊天会话且未显式指定记忆模式
- **THEN** 会话 MUST 使用 `every_30_turns`

### Requirement: Context usage measurement
系统 SHALL 使用后端统一 token 估算和当前 `chatModel` 精确匹配的模型能力窗口计算当前会话上下文占用，并在会话响应中返回 token 数、窗口大小和百分比。系统 MUST NOT 将一个全局固定窗口应用于所有模型，且当前模型缺少能力配置时 MUST 明确报告配置错误。

#### Scenario: Session state is returned
- **WHEN** user 创建、列出、读取、更新或完成一个聊天会话
- **THEN** 响应 MUST 包含该会话当前的 `contextTokens`、`contextWindowTokens` 和 `contextUsagePercent`

#### Scenario: Chat model is changed
- **WHEN** 项目把 `chatModel` 切换为具有不同上下文窗口的模型
- **THEN** 后端 MUST 从该模型对应的 `modelCapabilities` 条目解析窗口并重新用于所有会话占用计算

### Requirement: Thirty-turn automatic compression
使用 `every_30_turns` 的会话 SHALL 在自上次压缩边界起完成 30 轮 user-assistant 对话后，在下一次模型调用前自动压缩旧上下文。

#### Scenario: Thirty completed turns trigger compression
- **WHEN** 默认模式会话在压缩边界之后已有至少 30 条 assistant 消息并发送下一条消息
- **THEN** 后端 MUST 生成更新后的摘要、推进压缩边界并使用摘要和剩余消息调用 Agent

### Requirement: Seventy-percent automatic compression
使用 `context_70_percent` 的会话 SHALL 在包含待发送消息的估算上下文达到窗口 70% 时，在模型调用前自动压缩旧上下文。

#### Scenario: Candidate context reaches threshold
- **WHEN** 待发送消息会使会话估算占用达到或超过 70%
- **THEN** 后端 MUST 先压缩可压缩历史、重新计算占用，再决定是否调用 Agent

### Requirement: Manual compression
使用 `manual` 的会话 SHALL 仅在 user 应用该模式或显式请求压缩时执行压缩，不得按轮数或 70% 阈值自动压缩。

#### Scenario: Applying manual mode compresses immediately
- **WHEN** user 将一个会话的记忆模式应用为 `manual`
- **THEN** 后端 MUST 立即压缩该会话当前可压缩的历史并返回刷新后的记忆状态

#### Scenario: Manual mode can be compressed again
- **WHEN** manual 会话在产生更多消息后收到显式压缩请求
- **THEN** 后端 MUST 合并已有摘要和新历史并推进压缩边界

### Requirement: Compression preserves full history
记忆压缩 SHALL 只改变模型上下文的摘要和边界，MUST NOT 删除或改写 SQLite 中的原始聊天消息。

#### Scenario: User reads compressed session
- **WHEN** user 读取已经执行过压缩的会话历史
- **THEN** API MUST 返回压缩前后所有原始消息，模型请求 MUST 只包含摘要和压缩边界后的消息

### Requirement: Context hard limit
系统 SHALL 在候选上下文占用达到或超过 95% 时阻止新增聊天消息，并要求 user 先执行手动压缩。

#### Scenario: Frontend blocks at hard limit
- **WHEN** 当前会话 `contextUsagePercent` 达到或超过 95
- **THEN** 前端 MUST 禁用输入和发送并显示执行手动压缩的中文提示

#### Scenario: Backend rejects bypass attempt
- **WHEN** 客户端绕过界面提交会使上下文占用达到或超过 95% 的消息
- **THEN** 后端 MUST 返回统一上下文上限错误且 MUST NOT 持久化该消息
