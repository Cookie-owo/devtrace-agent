## Context

`LocalMcpClient` 已使用 `langchain-mcp-adapters`，但固定为名为 cls 的单个 SSE Server。配置管理需要保留项目 CLS 作为开箱即用默认值，同时允许每个用户管理更多真实 MCP endpoint。

## Goals / Non-Goals

**Goals:** CRUD、启停、连接检查、工具发现、超时重试、用户隔离、聊天与 AIOps 共用。

**Non-Goals:** 不托管远程 MCP Server 进程，不在数据库保存云厂商 Secret；凭据仍由对应本地/远程 Server 管理。

## Decisions

### 用户连接与默认回退

`mcp_connections` 保存 name、transport、url、enabled、timeout、retries 和最近检查摘要。用户尚未创建连接时，Provider 使用项目配置中的 CLS endpoint 作为只读默认连接；首次编辑时转为用户记录。

### 聚合 MCP Client

扩展现有 Client 接受多连接配置。LangChain 通过 `MultiServerMCPClient` 一次加载所有启用工具；直接工具调用先根据 discovery 结果定位 Server。重复工具名被视为配置错误，不静默覆盖。

### 实时检查

检查接口实时初始化 MCP session 并 list tools，持久化 ok/error、toolCount 和 checkedAt。错误仅返回安全摘要。

### 独立管理工作区

新增 `/mcp` 路由，使用紧凑列表和编辑面板展示连接状态及工具清单；启停使用 switch，检查使用明确命令按钮。

## Risks / Trade-offs

- 用户可配置 endpoint 产生 SSRF 风险；本地优先版本仅允许 http/https，拒绝带用户信息的 URL，并设置严格超时。
- 多 Server 工具重名必须显式报错。
