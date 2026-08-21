## ADDED Requirements

### Requirement: MCP server credentials use merged project configuration
本地 CLS MCP Server 启动和后端 MCP 配置检查 SHALL 从 merged 项目配置读取 CLS 凭据和连接参数。

#### Scenario: Base config leaves personal MCP credentials empty
- **WHEN** 检查 `config/project.json`
- **THEN** `clsMcpServer.secretId` 和 `clsMcpServer.secretKey` MUST 为空字符串，并由用户配置文件覆盖。

#### Scenario: Local startup receives merged MCP credentials
- **WHEN** 使用本地启动脚本启动 CLS MCP Server
- **THEN** 脚本 MUST 从 merged 项目配置导出 `TENCENTCLOUD_SECRET_ID`、`TENCENTCLOUD_SECRET_KEY`、`TRANSPORT`、`PORT` 和 `TZ`。
