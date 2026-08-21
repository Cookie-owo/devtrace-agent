## ADDED Requirements

### Requirement: Chat Agent can use discovered MCP tools
流式聊天 Agent SHALL 使用已发现的 MCP 工具，并通过现有的 SSE 和工具审核路径发出它们的生命周期事件。

#### Scenario: 真实 MCP 查询在聊天中完成
- **WHEN** 一个已认证的 user 请求 CLS 日志，并且本地 MCP 服务器可用
- **THEN** 的 Agent MUST 调用真实 MCP 搜索工具，并将返回的记录包含在最终响应中。
