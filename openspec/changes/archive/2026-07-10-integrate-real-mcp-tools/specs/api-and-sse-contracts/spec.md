## ADDED Requirements

### Requirement: MCP tool lifecycle uses shared SSE contract
MCP 工具发现、调用、完成和失败 SHALL 应由现有的共享 `tool.call` SSE 生命周期形状表示。

#### Scenario: MCP result is visible to the client
- **WHEN** 一个聊天 MCP 工具完成
- **THEN** 客户端 MUST 接收开始和完成的工具调用事件，然后接收最终响应。
