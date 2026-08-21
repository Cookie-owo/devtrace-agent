## ADDED Requirements

### Requirement: Tool call audit API contract
共享的 API-contract 包 SHALL 定义了经过身份验证的聊天会话工具调用审计集合及其响应结构，包括父级关联、工具名称、参数、状态、结果摘要、错误信息、时间戳和持续时间。

#### Scenario: Contract describes scoped audit collection
- **WHEN** 前端和后端实现聊天工具审计历史
- **THEN** 两个 MUST 使用相同的导出集合响应类型和 OpenAPI 路径用于 `GET /chat/sessions/{sessionId}/tool-call-audits`。
