## Why

项目目前只从项目配置读取一个 CLS SSE 地址，用户无法查看、检查、启停或扩展 MCP Server。聊天与 AIOps 也应基于同一组受管理连接装配真实工具。

## What Changes

- 增加 owner-scoped MCP connection 模型、CRUD 和默认 CLS 连接回退。
- 支持 SSE 与 streamable HTTP、启停、超时、重试和连接检查。
- 展示工具发现结果、连接错误和最近检查状态。
- 聊天与 AIOps 从当前用户启用的连接加载真实 MCP 工具。
- 增加中文 MCP 连接管理页面。

## Capabilities

### New Capabilities
- `mcp-connection-management`: 定义 MCP 连接、检查、工具发现和管理 UI。

### Modified Capabilities
- `real-mcp-tools`: MCP 工具来源改为用户启用连接。
- `api-and-sse-contracts`: 增加 MCP 管理契约。
- `vue-app-shell`: 增加 MCP 管理路由。

## Impact

- SQLite/Alembic、MCP client/provider、聊天与 AIOps 装配。
- API contracts、新前端页面和导航。
