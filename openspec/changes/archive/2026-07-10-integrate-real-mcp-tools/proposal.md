## Why

当前应用程序启动了官方的 CLS MCP 服务器，但聊天 Agent 无法发现或调用其工具。因此，无法通过对话查询真实的 CLS 数据。

## 什么更改

- 为本地 CLS MCP 端点添加一个具有发现、调用、超时、重试和显式失败结果的 MCP SSE 客户端。
- 将发现的 MCP 工具暴露给 LangChain 聊天 Agent，并通过现有的工具审计存储库持久化每次调用。
- 添加 MCP readiness/configuration 检查并在开发工作流中启动 /verify 本地 CLS MCP 服务。
- 明确拒绝MCP的失败，不使用模拟配置文件或伪造结果。

## 功能

### 新功能
- `real-mcp-tools`: 连接到并调用实际的本地MCP SSE工具。

### 修改的功能
- `stream-rag-chat`: 允许Agent使用发现的MCP工具并报告失败。
- `api-and-sse-contracts`: 添加MCP就绪状态和工具发现结果的形状。

## 影响

后端聊天集成、项目配置、本地 Compose 启动、readiness 检查和测试。CLS MCP 服务器仍然是官方腾讯实现。
