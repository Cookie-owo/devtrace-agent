## ADDED Requirements

### Requirement: MCP connection management contracts
共享契约 SHALL 定义 MCP connection CRUD、check 和 discovered tools 响应，并使用统一错误 envelope。

#### Scenario: 前端保存 MCP 连接
- **WHEN** 前端创建或更新连接
- **THEN** 前后端 MUST 使用同一 transport、URL、timeout、retries 和 enabled 字段定义。
