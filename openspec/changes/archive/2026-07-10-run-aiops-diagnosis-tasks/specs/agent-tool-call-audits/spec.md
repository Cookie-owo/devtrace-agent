## ADDED Requirements

### Requirement: Diagnostic tool calls use the common audit lifecycle
每个 AIOps 诊断工具调用 SHALL 都必须创建并最终确定与该诊断任务相关的 owner 范围的通用工具调用审计。

#### Scenario: Diagnostic MCP call is persisted
- **WHEN** Executor 开始并完成或失败一个 MCP 工具调用
- **THEN** 对应的审核 MUST 存储其稳定 ID、参数、状态、绑定的结果摘要或错误、时间戳和持续时间。
