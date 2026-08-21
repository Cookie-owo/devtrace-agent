## ADDED Requirements

### Requirement: Real MCP tools are available to AIOps execution
诊断 Executor SHALL 使用发现的本地 MCP 工具定义，根据诊断计划调用实际的 MCP 工具。

#### Scenario: MCP execution failure is surfaced
- **WHEN** 在配置的重试后，AIOps 工具连接或调用失败
- **THEN** 诊断流、审计、持久化结果和最终任务状态 MUST 记录明确的失败，而不伪造证据。
