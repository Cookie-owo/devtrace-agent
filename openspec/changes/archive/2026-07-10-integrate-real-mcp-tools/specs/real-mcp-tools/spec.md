## ADDED Requirements

### Requirement: Real MCP SSE tools
后端 SHALL 通过 SSE 连接到本地官方 CLS MCP 服务器，发现工具，调用发现的工具，并且从不返回模拟或伪造的数据。

#### Scenario: Tool discovery succeeds
- **WHEN** 本地 MCP SSE 端点可用
- **THEN** readiness MUST 报告成功，并且 Agent MUST 能够使用发现的工具定义。

#### Scenario: MCP failure is explicit
- **WHEN** 连接、发现或调用在有限重试后失败  
- **THEN** 后端 MUST 返回显式的 MCP 错误，而 MUST NOT 静默地生成一个结果。

### Requirement: MCP calls are audited
每个 MCP 工具调用 SHALL 都会使用现有的工具调用审计生命周期，包括工具名称、参数、结果摘要、持续时间、状态和错误信息。

#### Scenario: MCP call completes
- **WHEN** 一个 Agent 调用发现的 MCP 工具
- **THEN** 相应的聊天工具审计 MUST 应完成或失败，并带有真实的 MCP 结果。
