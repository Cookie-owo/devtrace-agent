## MODIFIED Requirements

### Requirement: Shared API contracts package
单体仓库 SHALL 包含 `packages/api-contracts` 作为 API 合同类型在各个应用程序中的共享位置。前端和后端实现 MUST 将此包作为 HTTP 响应信封、错误代码、OpenAPI 路径合同和 SSE 事件有效负载的真相来源。

#### Scenario: API contract package has a typed entrypoint
- **WHEN** 消费者导入 contracts 包
- **THEN** 它从 TypeScript 源入口点 MUST 导出类型化的合约定义。

#### Scenario: 合约包定义了 API 和 SSE 表面
- **WHEN** `packages/api-contracts` 被检查
- **THEN** 它 MUST 定义 HTTP 响应、错误、OpenAPI 和 SSE 事件合约导出。

#### Scenario: Applications do not invent event structures
- **WHEN** 前端或后端代码需要聊天流或 AIOps 诊断事件
- **THEN** 它 MUST 应该使用共享的 SSE 事件契约，而不是创建临时的事件有效载荷结构。
