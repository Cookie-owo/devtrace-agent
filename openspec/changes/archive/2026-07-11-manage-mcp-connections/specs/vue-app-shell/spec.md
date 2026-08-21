## MODIFIED Requirements

### Requirement: Route-based application shell
认证后的应用 SHALL 提供 `/chat`、`/knowledge`、`/aiops` 和 `/mcp` 工作区，并在桌面侧栏与移动导航中提供一致入口。

#### Scenario: 用户打开 MCP 管理
- **WHEN** 已认证用户访问 `/mcp`
- **THEN** 应用 MUST 在共享工作区框架中显示 MCP 连接管理页面。
