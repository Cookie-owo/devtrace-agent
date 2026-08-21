## MODIFIED Requirements

### Requirement: Real MCP SSE tools
系统 SHALL 通过当前用户启用的受管理 MCP 连接接入真实 Server，并 SHALL 在用户未配置连接时回退到项目 CLS SSE 配置。

#### Scenario: Agent loads managed tools
- **WHEN** 用户启动聊天或 AIOps 诊断
- **THEN** Agent MUST 只加载该用户启用连接中真实发现的工具。
