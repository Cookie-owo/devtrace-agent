## ADDED Requirements

### Requirement: Chat memory API contracts
系统 SHALL 在共享契约中定义会话记忆状态、记忆模式更新请求、显式压缩响应和对应的受保护 OpenAPI 路径。

#### Scenario: Memory mode is updated
- **WHEN** 客户端对 `/chat/sessions/{sessionId}/memory` 提交受支持的记忆模式
- **THEN** 后端 MUST 返回包含刷新后记忆状态的会话 DTO

#### Scenario: Manual compression is requested
- **WHEN** 客户端调用 `/chat/sessions/{sessionId}/memory:compact`
- **THEN** 后端 MUST 执行当前 user 会话的手动压缩并返回统一成功响应

### Requirement: Context limit error contract
统一错误目录 SHALL 定义稳定的 `CHAT_CONTEXT_LIMIT_REACHED` 业务错误，供 HTTP 和聊天 SSE 错误事件共同使用。

#### Scenario: Context limit rejects chat stream
- **WHEN** 聊天流因为 95% 上下文硬上限拒绝消息
- **THEN** SSE `error` 事件 MUST 使用 `CHAT_CONTEXT_LIMIT_REACHED` 并提供执行手动压缩的安全中文消息
