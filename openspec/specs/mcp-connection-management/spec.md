# mcp-connection-management Specification

## Purpose
TBD - created by archiving change manage-mcp-connections. Update Purpose after archive.
## Requirements
### Requirement: Owner-scoped MCP connection lifecycle
用户 SHALL 能创建、查看、更新、启停和删除自己的 MCP 连接，连接包含名称、transport、URL、timeout 和 retries。

#### Scenario: 用户访问其他用户连接
- **WHEN** 用户读取或修改不属于自己的连接
- **THEN** API MUST 返回统一权限错误。

#### Scenario: 用户提交不安全 URL
- **WHEN** URL 不是 http/https 或包含 userinfo
- **THEN** API MUST 返回参数错误且不得保存。

### Requirement: MCP connection check and tool discovery
用户 SHALL 能显式检查连接并查看真实 Server 返回的工具名称、描述和输入 schema。

#### Scenario: MCP Server 不可用
- **WHEN** 初始化或工具发现失败
- **THEN** 检查 MUST 返回明确失败状态和安全错误，MUST NOT 伪造工具。

### Requirement: Managed MCP runtime assembly
聊天与 AIOps SHALL 从当前用户启用的 MCP 连接装配工具；无用户记录时 SHALL 使用项目 CLS 默认连接。

#### Scenario: 连接被禁用
- **WHEN** 用户禁用连接
- **THEN** 后续 Agent 执行 MUST NOT 加载或调用该连接工具。

### Requirement: Chinese MCP management workspace
前端 SHALL 提供中文 MCP 管理工作区，展示连接状态、endpoint、transport、工具数量、最近检查和错误，并提供完整编辑操作。

#### Scenario: 检查正在执行
- **WHEN** 用户检查连接
- **THEN** 对应连接 MUST 显示检查中，完成后更新真实工具清单或错误。
