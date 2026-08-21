## ADDED Requirements

### Requirement: AIOps execution API contract
共享的 API-contract 包 SHALL 为 AIOps 诊断任务定义了经过身份验证的创建、状态、报告和 SSE 流式传输合约。

#### Scenario: Diagnostic stream path is described
- **WHEN** 检查 OpenAPI 合同
- **THEN** 它 MUST 描述受保护的 `POST /aiops/diagnostics/{diagnosticId}:stream` 操作及其共享的 SSE 响应结构。

#### Scenario: Diagnostic result has evidence state
- **WHEN** 诊断任务响应被序列化
- **THEN** 它 MUST 包含任务状态、查询、输入、结果负载、时间戳和报告数据，足以区分 SOP 支持的计划与通用计划。

### Requirement: AIOps graph stages use shared SSE events
API-合同包 SHALL 记录用于 Planner、Executor、Replanner 和 Report 诊断阶段的共享 SSE 事件有效负载。

#### Scenario: Graph progress is representable
- **WHEN** 诊断节点进行进度更新或重新规划
- **THEN** 共享的 `task.status` 事件 MUST 表示图阶段和安全进度细节。
